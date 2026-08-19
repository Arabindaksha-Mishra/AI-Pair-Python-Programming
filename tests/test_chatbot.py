"""
Test Suite: Task 1 — Context-Aware Rule-Based Chatbot
======================================================
Unit tests covering regex pattern matching, entity slots, state transitions, and context memory.
"""

import unittest
import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from capstone.chatbot.bot_engine import RuleBasedChatbot
from capstone.chatbot.regex_matcher import IntentType, RegexMatcher


class TestRuleBasedChatbot(unittest.TestCase):
    """Unit tests for Task 1: Context-Aware Rule-Based Chatbot."""

    def setUp(self):
        self.bot = RuleBasedChatbot()
        self.matcher = RegexMatcher()

    def test_regex_matching_intents(self):
        intent, _ = self.matcher.match_intent("Hello there")
        self.assertEqual(intent, IntentType.GREETING)

        intent, _ = self.matcher.match_intent("goodbye")
        self.assertEqual(intent, IntentType.FAREWELL)

        intent, slots = self.matcher.match_intent("My name is John")
        self.assertEqual(intent, IntentType.NAME_PRESENTATION)
        self.assertEqual(slots.get("user_name"), "John")

        intent, slots = self.matcher.match_intent("Can you explain fibonacci?")
        self.assertEqual(intent, IntentType.EXERCISE_QUERY)

    def test_context_memory_retention(self):
        # 1. Present name
        resp = self.bot.process_message("My name is Alice")
        self.assertIn("Alice", resp)
        self.assertEqual(self.bot.context.user_name, "Alice")

        # 2. Greeting should now remember name
        greet_resp = self.bot.process_message("Hello")
        self.assertIn("Alice", greet_resp)

        # 3. Ask question on topic
        topic_resp = self.bot.process_message("What is an anagram?")
        self.assertIn("anagram", topic_resp.lower())
        self.assertEqual(self.bot.context.last_topic, "anagram")

        # 4. Turn count increments
        self.assertEqual(self.bot.context.turn_count, 3)

    def test_context_reset(self):
        self.bot.process_message("My name is David")
        self.assertEqual(self.bot.context.user_name, "David")
        self.bot.reset()
        self.assertIsNone(self.bot.context.user_name)
        self.assertEqual(self.bot.context.turn_count, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
