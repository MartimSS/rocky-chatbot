"""
Entry point for the Rocky Chatbot CLI.

Run with:
    python main.py

Type 'quit', 'exit', or 'bye' to leave the chat.
"""

from rocky_chatbot import RockyChatbot


def main() -> None:
    bot = RockyChatbot()
    print(bot.greeting())
    print()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            print(bot.farewell())
            break

        if not user_input:
            continue

        response = bot.respond(user_input)
        print(f"Rocky: {response}")
        print()

        if any(word in user_input.lower() for word in ("bye", "goodbye", "exit", "quit")):
            print(bot.farewell())
            break


if __name__ == "__main__":
    main()
