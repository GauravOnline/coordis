"""
Discord Bot - Main Entry Point
"""
import os
from dotenv import load_dotenv
from core.bot import setup_bot

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    # Create and set up the bot
    bot = setup_bot()

    # Get the token from the environment variable
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        raise ValueError("No token found. Please create a .env file with your DISCORD_TOKEN")

    # Run the bot
    bot.run(TOKEN)
