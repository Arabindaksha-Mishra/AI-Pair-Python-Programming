"""
Rule-Based Chatbot Engine
=========================
Core orchestrator integrating:
1. Regex pattern matching
2. Context memory tracking
3. Categorized response generators (Greetings, Questions, Farewells, Unknowns)
"""

import datetime
import random
from typing import Any, Dict, Optional, Tuple

from .context_memory import ConversationContext
from .regex_matcher import IntentType, RegexMatcher


class RuleBasedChatbot:
    """Context-aware, rule-based conversational chatbot engine."""

    def __init__(self) -> None:
        self.matcher = RegexMatcher()
        self.context = ConversationContext()

        # Knowledge Base for Senior Python Topics
        self.topic_knowledge = {
            "fibonacci": (
                "The Fibonacci sequence is defined by F(n) = F(n-1) + F(n-2). "
                "In our exercises, we implement it using memoized recursion (O(N)), "
                "iterative pointer swapping (O(1) space), and lazy generator streaming."
            ),
            "anagram": (
                "An anagram is a word formed by rearranging the letters of another word. "
                "We check it in O(N) time using character frequency maps (collections.Counter) "
                "after sanitizing punctuation and case."
            ),
            "perfect number": (
                "A perfect number equals the sum of its proper positive divisors (e.g., 6 = 1+2+3, 28 = 1+2+4+7+14). "
                "Our solver uses an O(sqrt(N)) divisor pair search algorithm."
            ),
            "digit difference": (
                "Digit difference sorts input digits to create the maximum possible and minimum possible numbers, "
                "then calculates their difference (e.g., '213' -> 321 - 123 = 198)."
            ),
            "pizza": (
                "We have two pizza exercises: one interactive toppings prompt with a 'quit' sentinel loop, "
                "and another formatting pizza favorites into statements and summary paragraphs."
            ),
            "movie ticket": (
                "The movie theater pricing model: Under 3 is Free ($0), ages 3-12 are $10, and over 12 are $15. "
                "The module includes full input validation for non-numeric edge cases."
            ),
            "set": (
                "Set operations allow us to combine elements and eliminate duplicates via Set Union (A | B) "
                "or find exclusive items via Symmetric Difference (A ^ B)."
            ),
            "unique elements": (
                "We extract unique elements from lists while strictly preserving insertion order in O(N) time "
                "using Python's dict.fromkeys() method."
            ),
            "square": (
                "Our squaring loop iterates 0 through 9, skips even numbers using 'continue', and prints "
                "the squares of odd numbers (1, 9, 25, 49, 81)."
            ),
        }

    def process_message(self, user_input: str) -> str:
        """
        Processes incoming user message through sanitization, pattern matching,
        context resolution, and response generation.
        """
        cleaned = user_input.strip()
        if not cleaned:
            return "I didn't catch that. Could you please say something?"

        intent, slots = self.matcher.match_intent(cleaned)
        response = self._generate_response(intent, slots, cleaned)

        # Update dialogue state memory
        self.context.record_turn(
            user_input=cleaned,
            bot_response=response,
            intent_name=intent.value,
        )

        return response

    def _generate_response(self, intent: IntentType, slots: Dict[str, Any], raw_text: str) -> str:
        """Dispatches intent to categorized response generators."""
        tag = self.context.get_user_greeting_tag()

        if intent == IntentType.GREETING:
            greetings = [
                f"Hello{tag}! How can I assist you today?",
                f"Hi there{tag}! Great to chat with you. What would you like to explore?",
                f"Greetings{tag}! I'm ready to answer questions about Python, algorithms, or our capstone.",
            ]
            return random.choice(greetings)

        elif intent == IntentType.NAME_PRESENTATION:
            name = slots.get("user_name", "friend")
            self.context.set_user_name(name)
            return (
                f"Nice to meet you, {name}! I have remembered your name in our session memory. "
                "Feel free to ask me anything about the Python exercises or the Capstone project."
            )

        elif intent == IntentType.FAREWELL:
            farewells = [
                f"Goodbye{tag}! Have a fantastic day ahead!",
                f"Farewell{tag}! Thanks for chatting with me. Happy coding!",
                f"See you later{tag}! Best of luck with your Python projects!",
            ]
            return random.choice(farewells)

        elif intent == IntentType.HOW_ARE_YOU:
            return (
                f"I'm operating at 100% efficiency, thank you for asking{tag}! "
                "All rule-based pattern matching and memory systems are running smoothly. How are you doing?"
            )

        elif intent == IntentType.CAPABILITIES:
            return (
                "I am a Context-Aware Rule-Based Chatbot built completely using Python built-in libraries!\n"
                "Here is what I can do:\n"
                "1. Intent Classification: Regex pattern detection for greetings, questions, and commands.\n"
                "2. Context Memory: I remember your name, conversation turn history, and past topics.\n"
                "3. Domain Expert: Ask me about Fibonacci, Anagrams, Perfect Numbers, Data Cleaning, and more.\n"
                "4. Session Export: I can summarize and export our conversation history."
            )

        elif intent == IntentType.GRATITUDE:
            return f"You're very welcome{tag}! Always happy to help."

        elif intent == IntentType.HELP:
            return (
                "--- Available Commands & Topics ---\n"
                "• Tell me your name: 'My name is Alex'\n"
                "• Ask about exercises: 'Explain Fibonacci', 'What is an anagram?', 'How does perfect number work?'\n"
                "• Ask for time: 'What time is it?'\n"
                "• Check capabilities: 'What can you do?'\n"
                "• Exit: 'bye', 'quit', or 'exit'"
            )

        elif intent == IntentType.TIME_QUERY:
            now_str = datetime.datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
            return f"The current system date and time is: {now_str}."

        elif intent == IntentType.EXERCISE_QUERY:
            topic = slots.get("topic", "")
            for key, explanation in self.topic_knowledge.items():
                if key in topic or topic in key:
                    self.context.last_topic = key
                    return f"[Topic: {key.title()}]\n{explanation}"
            return "That's one of our core Python topics! Would you like a code breakdown or algorithmic complexity analysis?"

        elif intent == IntentType.QUESTION_GENERAL:
            # Check if previous context topic exists
            if self.context.last_topic:
                return (
                    f"Regarding our discussion on {self.context.last_topic}: "
                    "All implementations are designed with optimal time complexity and zero external dependencies."
                )
            return (
                f"That's an insightful question{tag}! As a rule-based assistant, I specialize in the "
                "10 Senior Python exercises and Capstone architectures. Try asking: 'Explain Fibonacci' or 'What is an anagram?'"
            )

        else:  # IntentType.UNKNOWN
            # Check if user said 'yes' to previous topic
            if raw_text.lower() in ("yes", "sure", "tell me more", "yep") and self.context.last_topic:
                topic = self.context.last_topic
                return f"Continuing on {topic}: All functions in this project are strictly tested with 100% unit test coverage."

            return (
                f"I'm not quite sure how to answer that yet{tag}. "
                "You can type 'help' to see what topics and commands I recognize, or ask about any of the 10 Python exercises."
            )
