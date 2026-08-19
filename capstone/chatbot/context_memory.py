"""
Context Memory & Dialogue State Tracker
=======================================
Maintains stateful memory across conversation turns:
- Tracks user name, last topic, turn counter, and previous inputs.
- Provides context-awareness so responses adapt dynamically over time.
"""

from dataclasses import dataclass, field
import datetime
import json
from typing import Any, Dict, List, Optional


@dataclass
class TurnRecord:
    turn_index: int
    user_input: str
    bot_response: str
    intent: str
    timestamp: str = field(
        default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


class ConversationContext:
    """Stateful dialogue context manager."""

    def __init__(self, max_history: int = 100) -> None:
        self.user_name: Optional[str] = None
        self.last_intent: Optional[str] = None
        self.last_topic: Optional[str] = None
        self.turn_count: int = 0
        self.history: List[TurnRecord] = []
        self.custom_slots: Dict[str, Any] = {}
        self.max_history: int = max_history

    def set_user_name(self, name: str) -> None:
        """Saves or updates user's name in memory."""
        self.user_name = name.strip().capitalize()

    def record_turn(self, user_input: str, bot_response: str, intent_name: str) -> None:
        """Records an utterance turn in the dialogue history (bounded to max_history)."""
        self.turn_count += 1
        self.last_intent = intent_name
        record = TurnRecord(
            turn_index=self.turn_count,
            user_input=user_input,
            bot_response=bot_response,
            intent=intent_name,
        )
        self.history.append(record)
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_user_greeting_tag(self) -> str:
        """Returns personalized name tag if user name is known."""
        if self.user_name:
            return f", {self.user_name}"
        return ""

    def export_session_json(self) -> str:
        """Exports the conversation history as a formatted JSON string."""
        data = {
            "user_name": self.user_name,
            "total_turns": self.turn_count,
            "last_topic": self.last_topic,
            "history": [
                {
                    "turn": r.turn_index,
                    "timestamp": r.timestamp,
                    "user": r.user_input,
                    "bot": r.bot_response,
                    "intent": r.intent,
                }
                for r in self.history
            ],
        }
        return json.dumps(data, indent=2)

    def reset(self) -> None:
        """Resets dialogue state."""
        self.user_name = None
        self.last_intent = None
        self.last_topic = None
        self.turn_count = 0
        self.history.clear()
        self.custom_slots.clear()


# Alias for state representation
DialogueState = ConversationContext
