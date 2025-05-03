# --- Imports ---
import discord
from discord import Message, Intents, Client
from discord.ext import commands
import logging 
from dotenv import load_dotenv
from random import randint
import os
from sqlmodel import Field, Session, SQLModel, create_engine, select
from event import Event, EventList
import datetime
from sqlalchemy.exc import SQLAlchemyError

# --- Initial Setup ---
load_dotenv()
Token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename = 'discord.log',encoding='utf-8', mode='w')
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
sqlite_file_name = "database.db"
engine = create_engine(f"sqlite:///{sqlite_file_name}")
SQLModel.metadata.drop_all(engine) # Drop all data, REMOVE FOR PRODUCTION!
SQLModel.metadata.create_all(engine)
bot = commands.Bot(command_prefix='?', intents=intents)

# assign_1 = Assignment(id = 1, name= "assignment 1", date_due= "05/15/25", date_assign= "04/20/2025", wght= 25)
# student_1 = Student(id = 19, f_name="Desmond", l_name="farrel", age=15, grade=10, disc_name="deadman_2")

# with Session(engine) as session:
#
#     # session.add(assign_1)
#     # session.add(student_1)
#     session.commit()


# ------- Event Listeners --------

# --- Bot Login Confirmation Message
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    get_response('hi')

# --- User Join Message
@bot.event
async def on_member_join(member):
    await member.send(f"Welcome {member.name}")

# --- Bot Main Behavior Block
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    print(f'[{channel}] {username}: {user_message}')

    msglist = user_message.split()
    if msglist[0][0] != '!': #If the message does not start with '!' it is not a command, return early
        print('Not a command')
        return

    if msglist[0] == '!help':
        #TODO Send Usage Information
        return
    elif msglist[0] == '!event':
        # Events need a name and due date, for now due date is mandatory
        if len(msglist) < 3:
            #TODO Send Usage Information
             return
        else:
            event_name = msglist[1]
            date_due = msglist[2]
            now = datetime.datetime.now()
            date_now = now.strftime("%m/%d/%Y")
            event = Event(event_name=event_name, date_due=date_due, date_assigned=date_now)

            try:
                with Session(engine) as sessioninner:
                    sessioninner.add(event)
                    print("Adding Event: ", event)
                    sessioninner.commit()
                await message.channel.send("Event: " + event_name + " due at: " + date_due + " added.")
            except SQLAlchemyError as e:
                print("An error occurred:", e)
            return
    elif msglist[0] == '!listevents':
        events = select_events()
        for event in events:
            await message.channel.send(event.event_name + " due at: " + event.date_due + " assigned at: " + event.date_assigned)

def select_events():
    with Session(engine) as session:
        statement = select(Event)
        events = session.exec(statement).all()
    return events

@bot.event
async def send_message(message: Message, user_message: str, username) -> None:
    if is_private := user_message[0]== '!':
        user_message = user_message[1:]
        
    try:
        response: str = get_response(user_message, username)
        await message.author.send(response) if is_private else await message.channel.send(response)    
        print(f'message: {user_message}')
    except Exception as e:
        print(e)
        return 
    

def get_response(user_input: str, username) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'oof quiet eh'
    elif 'hi' in lowered:
        return f'Hello world nice to meet {username}'
    elif 'roll dice' in lowered:
        return f'you rolled: {randint(1,6)}'
    elif 'event' in lowered:
        with Session(engine) as session:
            statement = select(Event).where(Event.name == 'walk-outside')
            event = session.exec(statement).first()
        return f'finding event on system event: {event}'
    # elif 'assignment 1'in lowered:
    #     with Session(engine) as session:
    #         statement = select(Assignment).where(Assignment.name == 'assignment 1')
    #         assignment = session.exec(statement).first()
    #     return f'finding event on system event: {assignment.name} due date: {assignment.date_due} weight: {assignment.wght}'
    # elif 'assignment'in lowered:
    #     with Session(engine) as session:
    #         statement = select(Assignment).where(Assignment.name == lowered)
    #         assignment = session.exec(statement).first()
    #     return f'finding event on system event: {assignment.name} due date: {assignment.date_due} weight: {assignment.wght}'
    else:
        return 'didnt get that one sorry'

bot.run(Token, log_handler=handler, log_level=logging.DEBUG)

def main() -> None:
    bot.run(Token, log_handler=handler, log_level=logging.DEBUG)


if __name__ == '__main__':
    main()