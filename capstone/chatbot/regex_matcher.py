"""
Regex Pattern Matcher & Intent Classifier
==========================================
Implements multi-tiered regular expression matching for intent classification
and entity / slot extraction without external dependencies.
"""

from enum import Enum
import re
from typing import Any, Dict, List, Optional, Tuple


class IntentType(Enum):
    GREETING = "greeting"
    FAREWELL = "farewell"
    NAME_PRESENTATION = "name_presentation"
    HOW_ARE_YOU = "how_are_you"
    CAPABILITIES = "capabilities"
    QUESTION_GENERAL = "question_general"
    EXERCISE_QUERY = "exercise_query"
    TIME_QUERY = "time_query"
    HELP = "help"
    GRATITUDE = "gratitude"
    UNKNOWN = "unknown"


class RegexMatcher:
    """
    Evaluates raw user input against priority-ordered regular expressions
    to extract intent, slots, and match metadata.
    """

    def __init__(self) -> None:
        self._compile_patterns()

    def _compile_patterns(self) -> None:
        """Pre-compiles regex patterns for high-performance matching."""
        # 1. Greetings
        self.re_greeting = re.compile(
            r"^(hi|hello|hey|howdy|greetings|good\s+(morning|afternoon|evening|day))\b",
            re.IGNORECASE,
        )

        # 2. Farewells
        self.re_farewell = re.compile(
            r"\b(bye|goodbye|see\s+ya|see\s+you|exit|quit|farewell|cya|talk\s+to\s+you\s+later)\b",
            re.IGNORECASE,
        )

        # 3. Name introduction (e.g., "My name is John", "I am Alice", "Call me Bob")
        self.re_name = re.compile(
            r"\b(?:my\s+name\s+is|i\s+am|i'm|call\s+me)\s+([A-Za-z]+)\b",
            re.IGNORECASE,
        )

        # 4. Status / How are you
        self.re_how_are_you = re.compile(
            r"\b(how\s+are\s+you|how's\s+it\s+going|how\s+do\s+you\s+do|how\s+are\s+things)\b",
            re.IGNORECASE,
        )

        # 5. Capabilities / Self identity
        self.re_capabilities = re.compile(
            r"\b(who\s+are\s+you|what\s+can\s+you\s+do|what\s+are\s+your\s+skills|features|what\s+is\s+this)\b",
            re.IGNORECASE,
        )

        # 6. Gratitude / Thanks
        self.re_gratitude = re.compile(
            r"\b(thank\s+you|thanks|thx|appreciate\s+it|thank\s+you\s+so\s+much)\b",
            re.IGNORECASE,
        )

        # 7. Help
        self.re_help = re.compile(
            r"^(help|commands|options|\?)$",
            re.IGNORECASE,
        )

        # 8. Exercise Queries (Questions regarding the 10 Python exercises)
        self.re_exercise = re.compile(
            r"\b(fibonacci|anagram|perfect\s+number|digit\s+difference|pizza|movie\s+ticket|set|unique\s+elements|square)\b",
            re.IGNORECASE,
        )

        # 9. Time queries
        self.re_time = re.compile(
            r"\b(what\s+time\s+is\s+it|current\s+time|today'?s\s+date|what\s+day\s+is\s+it)\b",
            re.IGNORECASE,
        )

        # 10. Generic Questions
        self.re_question = re.compile(
            r"^(what|why|how|when|where|who|is|are|can|could|would|will)\b.*\??$",
            re.IGNORECASE,
        )

    def match_intent(self, text: str) -> Tuple[IntentType, Dict[str, Any]]:
        """
        Matches text against compiled regular expressions.

        Returns:
            Tuple of (IntentType, extracted_slots_dict)
        """
        cleaned = text.strip()
        slots: Dict[str, Any] = {}

        if not cleaned:
            return IntentType.UNKNOWN, slots

        # Check for Name Introduction (e.g., "Hi, my name is Alex", "Call me Bob")
        name_match = self.re_name.search(cleaned)
        if name_match:
            candidate_name = name_match.group(1).capitalize()
            # Guard against common adjectives / states when user says "I am happy" / "I'm fine"
            non_name_stoplist = {
                "Happy", "Tired", "Fine", "Good", "Sad", "Ready", "Excited", "Here",
                "Back", "Ok", "Okay", "Sorry", "Curious", "Testing", "Learning",
                "Doing", "Wondering", "Working", "New", "Looking", "Thinking",
            }
            if candidate_name not in non_name_stoplist:
                slots["user_name"] = candidate_name
                return IntentType.NAME_PRESENTATION, slots

        # Farewells
        if self.re_farewell.search(cleaned):
            return IntentType.FAREWELL, slots

        # Gratitude
        if self.re_gratitude.search(cleaned):
            return IntentType.GRATITUDE, slots

        # Help
        if self.re_help.match(cleaned):
            return IntentType.HELP, slots

        # How are you
        if self.re_how_are_you.search(cleaned):
            return IntentType.HOW_ARE_YOU, slots

        # Capabilities
        if self.re_capabilities.search(cleaned):
            return IntentType.CAPABILITIES, slots

        # Time queries
        if self.re_time.search(cleaned):
            return IntentType.TIME_QUERY, slots

        # Greetings
        if self.re_greeting.search(cleaned):
            return IntentType.GREETING, slots

        # Specific Exercise / Domain Queries
        exercise_match = self.re_exercise.search(cleaned)
        if exercise_match:
            slots["topic"] = exercise_match.group(1).lower()
            return IntentType.EXERCISE_QUERY, slots

        # General Questions
        if self.re_question.search(cleaned) or cleaned.endswith("?"):
            slots["raw_question"] = cleaned
            return IntentType.QUESTION_GENERAL, slots

        return IntentType.UNKNOWN, slots
