import os
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

# Help message as a separate variable
HELP_MESSAGE = (
    "Hello! I'm your friendly bot. Here are some commands you can use:\n"
    "`!help` - Displays this message with usage information.\n"
    "`New Homework Item` - Sends a fun reminder about homework.\n"
    "Enjoy using the bot!"
)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# this is the code we will use first to test the connection
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!help'):
        await message.channel.send(HELP_MESSAGE)

    if message.content.startswith("New Homework Item"):
        await message.channel.send("Say goodbye to your weekend!")


# start the bot
client.run(TOKEN)
