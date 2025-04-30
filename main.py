import discord
from discord import Message, Intents, Client
from discord.ext import commands
import logging 
from dotenv import load_dotenv
from random import randint
import os


from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select


load_dotenv()
Token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename = 'discord.log',encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class Assignment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    date_due: str = None
    date_assign: str
    wght: int

class AssignmentResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    stu_id: int
    stu_mark: float
    wght: int

class AssignmentList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    class_id : Optional[int]
    name: str



class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_name: str
    class_name: str
    class_id: str
    date_due: Optional[str] = None
    date_assigned: int

class EventAttendence (SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    stu_id: int
    class_id: int
    attend: bool

class EventList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    class_id: int
    name: str



class ClassInfo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    grade: int
    tea_id: int
    tea_name: str

class ClassList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class ClassAttendence(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    stu_id: int
    attend:bool



class StudentList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    grade: Optional[int] = None

class StudentGrades(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    class_id:int
    curr_mark:int

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    f_name: str
    l_name: str 
    age: Optional[int] = None
    grade: int
    disc_name: str

class TeacherList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Teacher(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    f_name: str
    l_name: str
    #classes_teaching: list[int] 
    age: Optional[int] = None
    disc_name: str


assign_1 = Assignment(id = 1, name= "assignment 1", date_due= "05/15/25", date_assign= "04/20/2025", wght= 25)
assign_2 = Assignment(id = 2, name= "assignment 2", date_due= "05/20/25", date_assign= "04/30/2025", wght= 15)
assign_3 = Assignment(id = 3, name= "assignment 3", date_due= "06/10/25", date_assign= "05/15/25", wght= 10)
assign_4 = Assignment(id = 4, name= "assignment 5", date_due= "07/01/25", date_assign= "06/22/25", wght= 15)
assign_5 = Assignment(id = 5, name= "assignment 4", date_due= "06/20/25", date_assign= "05/30/25", wght= 5)


student_1 = Student(id = 19, f_name="Desmond", l_name="farrel", age=15, grade=10, disc_name="deadman_2")
student_2 = Student(id = 11, f_name="Alexander", l_name="Macedon", age=14, grade=10, disc_name="alex_raider2516")
student_3 = Student(id = 13, f_name="Issac", l_name="Newton", age=15, grade=10, disc_name="IssacPhysics12")
student_4 = Student(id = 14, f_name="Martin", l_name="Luther", age=16, grade=10, disc_name="king_of_scripts")
student_5 = Student(id = 15, f_name="Joey", l_name="Stalin", age=15, grade=10, disc_name="WintersScorn111")
student_6 = Student(id = 17, f_name="Edward", l_name="Windosr", age=15, grade=10, disc_name="Eddy_num3")

engine = create_engine("sqlite:///database.db")

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    
    session.add(assign_1)
    session.add(assign_2)
    session.add(assign_3)
    session.add(assign_4)
    session.add(assign_5)

    session.add(student_1)
    session.add(student_2)
    session.add(student_3)
    session.add(student_4)
    session.add(student_5)
    session.add(student_6)
    session.commit()

bot = commands.Bot(command_prefix='?', intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is starting {bot.user.name}")
    get_response('hi')

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    print(f'[{channel}] {username}: {user_message}')
    await send_message(message, user_message, username)

@bot.event  
async def send_message(message: Message, user_message: str, username) -> None:
    if is_private := user_message[0]== '?':
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
    elif 'assignment 1'in lowered:
        with Session(engine) as session:
            statement = select(Assignment).where(Assignment.name == 'assignment 1')
            assignment = session.exec(statement).first()
        return f'finding event on system event: {assignment.name} due date: {assignment.date_due} weight: {assignment.wght}'
    elif 'assignment'in lowered:
        with Session(engine) as session:
            statement = select(Assignment).where(Assignment.name == lowered)
            assignment = session.exec(statement).first()
        return f'finding event on system event: {assignment.name} due date: {assignment.date_due} weight: {assignment.wght}'
    else:
        return 'didnt get that one sorry'

bot.run(Token, log_handler=handler, log_level=logging.DEBUG)

def main() -> None:
    bot.run(Token, log_handler=handler, log_level=logging.DEBUG)


    if __name__ == '__main__':
        main()