"""
Unit tests for the RockyChatbot class.
"""

import re
import pytest

from rocky_chatbot import (
    RockyChatbot,
    HAPPY_TONES,
    EXCITED_TONES,
    CURIOUS_TONES,
    SAD_TONES,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

ALL_TONES = HAPPY_TONES + EXCITED_TONES + CURIOUS_TONES + SAD_TONES


def contains_tone(text: str) -> bool:
    """Return True if text contains at least one known musical-tone marker."""
    return any(tone in text for tone in ALL_TONES)


# ---------------------------------------------------------------------------
# Basic construction / properties
# ---------------------------------------------------------------------------


class TestRockyChatbotInit:
    def test_name(self) -> None:
        bot = RockyChatbot()
        assert bot.name == "Rocky"


# ---------------------------------------------------------------------------
# greeting / farewell
# ---------------------------------------------------------------------------


class TestGreetingAndFarewell:
    def test_greeting_contains_rocky(self) -> None:
        bot = RockyChatbot()
        greeting = bot.greeting()
        assert "Rocky" in greeting

    def test_greeting_contains_human(self) -> None:
        bot = RockyChatbot()
        assert "human" in bot.greeting().lower()

    def test_greeting_contains_tone(self) -> None:
        bot = RockyChatbot()
        assert contains_tone(bot.greeting())

    def test_farewell_contains_goodbye(self) -> None:
        bot = RockyChatbot()
        farewell = bot.farewell()
        assert re.search(r"goodbye|farewell|miss", farewell, re.IGNORECASE)

    def test_farewell_contains_tone(self) -> None:
        bot = RockyChatbot()
        assert contains_tone(bot.farewell())


# ---------------------------------------------------------------------------
# Empty / blank input
# ---------------------------------------------------------------------------


class TestEmptyInput:
    def test_empty_string(self) -> None:
        bot = RockyChatbot()
        response = bot.respond("")
        assert isinstance(response, str)
        assert len(response) > 0

    def test_whitespace_only(self) -> None:
        bot = RockyChatbot()
        response = bot.respond("   ")
        assert isinstance(response, str)
        assert len(response) > 0


# ---------------------------------------------------------------------------
# Keyword matching: each rule category
# ---------------------------------------------------------------------------


class TestKeywordMatching:

    @pytest.fixture(autouse=True)
    def bot(self) -> None:
        self.bot = RockyChatbot()

    # Greetings
    def test_hello_response(self) -> None:
        response = self.bot.respond("Hello there!")
        assert any(
            keyword in response.lower()
            for keyword in ("hello", "greet", "rocky", "good", "meet")
        )

    def test_hi_response(self) -> None:
        response = self.bot.respond("Hi!")
        assert isinstance(response, str) and len(response) > 0

    # Farewells
    def test_bye_response(self) -> None:
        response = self.bot.respond("Goodbye!")
        assert any(
            keyword in response.lower()
            for keyword in ("goodbye", "miss", "farewell", "sad", "talk")
        )

    # Name / identity
    def test_who_are_you(self) -> None:
        response = self.bot.respond("Who are you?")
        assert "rocky" in response.lower() or "eridian" in response.lower()

    def test_your_name(self) -> None:
        response = self.bot.respond("What is your name?")
        assert "rocky" in response.lower()

    # Science
    def test_science_keyword(self) -> None:
        response = self.bot.respond("Tell me about science.")
        assert "science" in response.lower() or "rocky" in response.lower()

    def test_chemistry_keyword(self) -> None:
        response = self.bot.respond("I love chemistry!")
        assert contains_tone(response)

    def test_molecule_keyword(self) -> None:
        response = self.bot.respond("What is a molecule?")
        assert isinstance(response, str) and len(response) > 0

    # Maths
    def test_math_keyword(self) -> None:
        response = self.bot.respond("Let's talk about math.")
        assert "math" in response.lower() or "number" in response.lower()

    # Food
    def test_food_keyword(self) -> None:
        response = self.bot.respond("I'm hungry. What should I eat?")
        assert any(
            word in response.lower()
            for word in ("ammonia", "food", "human", "eat", "drink", "eridian")
        )

    # Sleep
    def test_sleep_keyword(self) -> None:
        response = self.bot.respond("I am tired and want to sleep.")
        assert "sleep" in response.lower() or "hibernat" in response.lower()

    # Space
    def test_space_keyword(self) -> None:
        response = self.bot.respond("Tell me about space travel.")
        assert any(
            word in response.lower()
            for word in ("space", "star", "rocky", "universe", "ship", "discover", "journey")
        )

    # Happy emotion
    def test_happy_keyword(self) -> None:
        response = self.bot.respond("I am happy today!")
        assert any(
            word in response.lower()
            for word in ("happy", "good", "wonderful", "best", "great")
        )

    # Sad emotion
    def test_sad_keyword(self) -> None:
        response = self.bot.respond("I feel sad.")
        assert "sad" in response.lower() or "rocky" in response.lower()

    # Ammonia / Eridian
    def test_ammonia_keyword(self) -> None:
        response = self.bot.respond("What do you know about ammonia?")
        assert any(
            word in response.lower()
            for word in ("ammonia", "eridian", "alien", "human", "rocky")
        )

    def test_alien_keyword(self) -> None:
        response = self.bot.respond("Are you an alien?")
        assert "eridian" in response.lower() or "rocky" in response.lower()

    # Friendship
    def test_friend_keyword(self) -> None:
        response = self.bot.respond("You are my friend!")
        assert "friend" in response.lower()

    # Questions
    def test_question_mark(self) -> None:
        response = self.bot.respond("Really?")
        assert isinstance(response, str) and len(response) > 0

    def test_how_keyword(self) -> None:
        response = self.bot.respond("How does this work?")
        assert isinstance(response, str) and len(response) > 0

    # Thanks
    def test_thanks_keyword(self) -> None:
        response = self.bot.respond("Thank you, Rocky!")
        assert any(
            word in response.lower()
            for word in ("welcome", "pleasure", "happy", "thanks", "enjoy", "friend")
        )

    # Help
    def test_help_keyword(self) -> None:
        response = self.bot.respond("I need help.")
        assert "help" in response.lower() or "rocky" in response.lower()

    # Astrophage
    def test_astrophage_keyword(self) -> None:
        response = self.bot.respond("The sun is dying. Astrophage!")
        assert "astrophage" in response.lower() or "science" in response.lower() or "rocky" in response.lower()

    # Compliments
    def test_smart_keyword(self) -> None:
        response = self.bot.respond("You are so smart!")
        assert isinstance(response, str) and len(response) > 0


# ---------------------------------------------------------------------------
# Fallback responses
# ---------------------------------------------------------------------------


class TestFallbackResponse:
    def test_unknown_input_returns_string(self) -> None:
        bot = RockyChatbot()
        response = bot.respond("xyzzy plugh frobozz")
        assert isinstance(response, str) and len(response) > 0

    def test_unknown_input_contains_tone(self) -> None:
        bot = RockyChatbot()
        response = bot.respond("xyzzy plugh frobozz")
        assert contains_tone(response)


# ---------------------------------------------------------------------------
# Tone formatting: _format should always resolve placeholders
# ---------------------------------------------------------------------------


class TestFormatMethod:
    def test_no_unresolved_placeholders(self) -> None:
        bot = RockyChatbot()
        # Call respond many times to exercise format paths
        inputs = [
            "hello", "science", "math", "food", "sleep",
            "space", "happy", "sad", "ammonia", "friend", "?",
            "unknown random words here",
        ]
        for inp in inputs:
            response = bot.respond(inp)
            assert "{happy}" not in response
            assert "{excited}" not in response
            assert "{curious}" not in response
            assert "{sad}" not in response


# ---------------------------------------------------------------------------
# Responses are non-deterministic but always valid strings
# ---------------------------------------------------------------------------


class TestNonDeterminism:
    def test_multiple_responses_are_valid(self) -> None:
        bot = RockyChatbot()
        for _ in range(20):
            response = bot.respond("hello")
            assert isinstance(response, str) and len(response) > 0
