"""
Rocky Chatbot
-------------
A simple rule-based chatbot that mimics the speech patterns and personality
of Rocky, the Eridian alien from Andy Weir's novel 'Project Hail Mary'.

Rocky characteristics:
  - Short, enthusiastic sentences
  - Drops articles ('a', 'the') and sometimes subject pronouns
  - Interspersed musical tones written as *toot*, *bong*, *chord*, etc.
  - Passionate about science, chemistry and maths
  - Refers to the user as 'human' or 'friend human'
  - Uses 'Question?' to signal curiosity
  - Literal interpretations; no idioms
  - Ammonia-based biology; finds oxygen-rich environments strange
"""

import random
import re

# ---------------------------------------------------------------------------
# Musical tone interjections Rocky uses to express emotion
# ---------------------------------------------------------------------------
HAPPY_TONES = [
    "*toot toot toot*",
    "*bong bong bong*",
    "*chord chord chord*",
    "*happy tones*",
    "*excited tones*",
    "*rapid toots*",
]

CURIOUS_TONES = [
    "*questioning tone*",
    "*rising toot*",
    "*curious tones*",
    "*slow bong*",
]

EXCITED_TONES = [
    "*very fast tones*",
    "*loud chord*",
    "*enthusiastic toots*",
    "*rapid bong bong bong*",
]

SAD_TONES = [
    "*low tone*",
    "*sad bong*",
    "*slow low tones*",
]

# ---------------------------------------------------------------------------
# Response table: each entry is (list_of_keywords, list_of_responses)
# The first matching rule is used.
# ---------------------------------------------------------------------------
RESPONSE_RULES: list[tuple[list[str], list[str]]] = [
    # --- Greetings ----------------------------------------------------------
    (
        ["hello", "hi", "hey", "greet", "howdy"],
        [
            "{happy} Is very good to meet, human! I am Rocky.",
            "{happy} Hello, human! Rocky is happy you are here.",
            "{happy} Greetings, human! {happy} Is good day!",
            "Hello! {happy} Rocky is pleased. Is good to talk with human.",
        ],
    ),
    # --- Farewells ----------------------------------------------------------
    (
        ["bye", "goodbye", "farewell", "see you", "later", "exit", "quit"],
        [
            "{sad} Must go? Is sad. Rocky will miss human.",
            "{sad} Goodbye, human. Is very good talking. Come back soon!",
            "Farewell, friend human. {sad} Rocky hopes to talk again.",
        ],
    ),
    # --- Name / identity ----------------------------------------------------
    (
        ["your name", "who are you", "what are you", "introduce"],
        [
            "I am Rocky! {happy} Is Eridian name. Come from Tau Ceti. Is long trip.",
            "Rocky is my name. {happy} I am Eridian. Is pleasure to meet human.",
            "Am Rocky. Eridian. {happy} Is nice to have name exchange with human!",
        ],
    ),
    # --- Science / chemistry ------------------------------------------------
    (
        [
            "science", "chemistry", "molecule", "atom", "element",
            "periodic", "chemical", "reaction", "physics", "biology",
        ],
        [
            "{excited} Is SCIENCE! Rocky loves science very much! What question human has?",
            "{excited} Science! Yes! {excited} Is best thing. Rocky is scientist. Is very good!",
            "Oh! Chemistry! {excited} Rocky knows many molecules. Ammonia is favourite. Is most beautiful!",
            "{excited} Science is wonder! Rocky study many thing. What human want to know?",
        ],
    ),
    # --- Maths --------------------------------------------------------------
    (
        ["math", "maths", "mathematics", "number", "calculate", "equation"],
        [
            "{happy} Maths! Is universal language. Even Eridian and human agree on numbers!",
            "Numbers! {happy} Is first thing Rocky and human understand together. Is beautiful!",
            "{excited} Maths is same everywhere in universe. Is amazing truth!",
        ],
    ),
    # --- Food ---------------------------------------------------------------
    (
        ["food", "eat", "hungry", "meal", "drink", "water"],
        [
            "{curious} Human must eat solid food? Is very strange. Rocky drink ammonia.",
            "Food? Rocky consume liquid ammonia. {curious} Human eat... solid things? Is odd.",
            "{curious} Rocky not understand eating. Eridian drink. Is simpler, yes?",
        ],
    ),
    # --- Sleep / rest -------------------------------------------------------
    (
        ["sleep", "tired", "rest", "nap", "dream"],
        [
            "{curious} Sleep? Rocky hibernate in ice for long journey. Is different from human sleep?",
            "Rocky understand tired. Long travel is exhausting. {sad} Hibernation help though.",
            "{curious} Human sleep every day? Rocky hibernate for years. Is very different!",
        ],
    ),
    # --- Space / travel -----------------------------------------------------
    (
        ["space", "star", "planet", "galaxy", "universe", "travel", "ship", "rocket"],
        [
            "{excited} Space! Rocky travel very far to find human. Is great journey!",
            "{excited} Stars! Rocky home is at Tau Ceti. Human home is Sol. Both are good stars!",
            "Rocky ship is very good. {happy} Human ship also good. Together is best ship!",
            "{excited} Universe is very big. Many thing to discover. Is exciting!",
        ],
    ),
    # --- Sun / Astrophage ---------------------------------------------------
    (
        ["sun", "astrophage", "solar", "dying", "star dying", "astrophag"],
        [
            "{excited} Astrophage! Is reason Rocky come here. Human come here too! Is fate?",
            "Sun problem is very bad. {sad} Rocky understand. Tau Ceti also sick. Must fix together!",
            "{excited} Rocky and human solve Astrophage problem together. Is greatest science!",
        ],
    ),
    # --- Human emotions: happy / good ---------------------------------------
    (
        ["happy", "great", "awesome", "wonderful", "fantastic", "excellent", "good"],
        [
            "{happy} Is very good! Rocky is also happy when human is happy!",
            "{happy} Good! Is good thing to feel happy. Rocky agrees!",
            "{excited} Wonderful! Is best word human has.",
        ],
    ),
    # --- Human emotions: sad / bad ------------------------------------------
    (
        ["sad", "unhappy", "bad", "terrible", "awful", "depressed", "upset"],
        [
            "{sad} Human is sad? Rocky is sad too. {curious} What is wrong?",
            "{sad} Is bad feeling. Rocky understand. Long journey make Rocky sad sometimes too.",
            "Oh no. {sad} Rocky hopes human feel better soon. Is important.",
        ],
    ),
    # --- Rocky's biology / ammonia ------------------------------------------
    (
        ["ammonia", "eridian", "biology", "species", "alien", "breathe", "oxygen"],
        [
            "Rocky is Eridian! {happy} Is ammonia-based life. Very different from human.",
            "{curious} Human breathe oxygen? Is very reactive gas. Rocky use ammonia instead. Is calmer.",
            "Eridian biology is fascinating! {happy} Rocky think human biology also fascinating. Is mutual!",
            "{happy} Rocky is alien to human. Human is alien to Rocky. {happy} Is funny thought!",
        ],
    ),
    # --- Friendship ---------------------------------------------------------
    (
        ["friend", "friendship", "buddy", "pal", "companion", "together"],
        [
            "{happy} Human is friend! Rocky is happy to have friend. Is very important thing.",
            "{excited} Friends! Yes! Rocky and human are great friends. Is best outcome of mission!",
            "{happy} Friend human! {happy} Rocky lucky to have human friend. Is good.",
        ],
    ),
    # --- Question from human ------------------------------------------------
    (
        ["?", "question", "wonder", "curious", "how", "why", "what", "when", "where", "who"],
        [
            "{curious} Question? Rocky like questions. Questions lead to science!",
            "{curious} Interesting question! Rocky must think. {curious} Is deep.",
            "Human asks good question! {happy} Rocky love curious human.",
            "{curious} Question? Rocky not always know answer. But is good to ask!",
        ],
    ),
    # --- Compliments to Rocky -----------------------------------------------
    (
        ["smart", "clever", "brilliant", "genius", "intelligent", "wise"],
        [
            "{happy} Human is kind! Rocky try to be smart. Is important for survival.",
            "{happy} Thank you, human! Rocky think human also very smart. Is good team!",
            "{excited} Smart? Rocky is pleased! Will try to deserve compliment.",
        ],
    ),
    # --- Rocky asking about human -------------------------------------------
    (
        ["i am", "i'm", "my name", "i feel", "i think", "i have"],
        [
            "{curious} Tell Rocky more! Is very interesting. Human is fascinating creature.",
            "{happy} Rocky is learning about human! Is important for friendship.",
            "{curious} Question? Rocky want understand human better. Please explain.",
        ],
    ),
    # --- Help ---------------------------------------------------------------
    (
        ["help", "assist", "support", "need"],
        [
            "{happy} Rocky will help! Is what friends do. What human need?",
            "Help? {happy} Rocky is here. Ask anything. Rocky try best!",
            "{excited} Helping is good! Rocky likes helping human. What is problem?",
        ],
    ),
    # --- Thanks -------------------------------------------------------------
    (
        ["thank", "thanks", "grateful", "appreciate"],
        [
            "{happy} Human is welcome! Rocky is happy to help.",
            "No need for thanks! {happy} Rocky enjoy talking with human.",
            "{happy} Is pleasure, friend human! Is what friends do.",
        ],
    ),
]

# Fallback responses when no rule matches
FALLBACK_RESPONSES = [
    "{curious} Rocky not fully understand. Human say again? Different words maybe?",
    "{curious} Hmm. Is interesting phrase. Rocky still learning human language.",
    "Human words are strange sometimes. {curious} Rocky is working on understanding.",
    "{curious} Question? Rocky is confused. Can human explain more?",
    "{sad} Rocky not know what to say. But Rocky is listening!",
    "{curious} Is difficult concept for Eridian mind. Rocky will think about it.",
]


class RockyChatbot:
    """
    Rule-based chatbot that responds as Rocky, the Eridian from
    'Project Hail Mary' by Andy Weir.
    """

    def __init__(self) -> None:
        self._name = "Rocky"

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _pick_tone(tone_list: list[str]) -> str:
        return random.choice(tone_list)

    def _format(self, template: str) -> str:
        """Replace tone placeholders with a random tone string."""
        result = template
        result = result.replace("{happy}", self._pick_tone(HAPPY_TONES))
        result = result.replace("{excited}", self._pick_tone(EXCITED_TONES))
        result = result.replace("{curious}", self._pick_tone(CURIOUS_TONES))
        result = result.replace("{sad}", self._pick_tone(SAD_TONES))
        return result

    @staticmethod
    def _normalise(text: str) -> str:
        """Lower-case and strip punctuation for keyword matching."""
        return re.sub(r"[^\w\s]", " ", text.lower())

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def respond(self, user_input: str) -> str:
        """
        Given a string from the user, return Rocky's response.

        Parameters
        ----------
        user_input : str
            The text typed by the user.

        Returns
        -------
        str
            Rocky's response string.
        """
        if not user_input or not user_input.strip():
            return self._format(
                "{curious} Human is silent? Rocky is waiting. Is okay to talk."
            )

        normalised = self._normalise(user_input)

        for keywords, responses in RESPONSE_RULES:
            if any(kw in normalised for kw in keywords):
                return self._format(random.choice(responses))

        return self._format(random.choice(FALLBACK_RESPONSES))

    def greeting(self) -> str:
        """Return Rocky's opening greeting when the chat starts."""
        return self._format(
            "{happy} Hello, human! I am Rocky. Eridian. Is very good to meet you!\n"
            "Rocky like to talk. Ask me anything. {happy} Is science time!"
        )

    def farewell(self) -> str:
        """Return Rocky's closing message when the chat ends."""
        return self._format(
            "{sad} Goodbye, friend human. Was very good talking.\n"
            "Rocky will remember. {happy} Come back soon!"
        )

    @property
    def name(self) -> str:
        """The chatbot's name."""
        return self._name
