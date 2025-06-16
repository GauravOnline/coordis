import discord
from discord import Intents

from commands.base import Command
from services.user_service import UserService
from db.base import get_session
from datetime import datetime
from ui import user_ui
from core.constants import USAGE_MESSAGE_DISPLAY_TIME, FEEDBACK_MESSAGE_DISPLAY_TIME

class UserCommand(Command):
    def __init__(self):
        super().__init__(name="role", description="change Permissions level",
                         roles=['teacher'])

    async def execute(self, bot, ctx, *args):
        if not args:
            await ctx.send(user_ui.usage_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)
            return
        
        try:
            args = args[0]
            action = args[0].lower()
            print(f"act: {args}\n")
        except IndexError:
            print("INDEX ERROR")
            await ctx.send(user_ui.usage_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)
            return
        
        with get_session() as session:
            service = UserService(session)
            try:
                messenger = service.get_user(ctx.author.name)
                print(f"mess:{messenger.user_role}")
            except AttributeError:
                print("AttributeError")
            '''
            # get user permisssion level of command operator
            try:
                j = 0
                messenger = service.get_user(ctx.author.name)
                for role in self.roles:
                    print (f"\n\nrole: {role}\n{self.roles}\n\n")
                    if messenger.user_role != role:
                        print(f"self.roles: {role}  user role: {messenger.user_role}")
                    else:
                        j=1
                        print(f"self.roles: {role}  user role: {messenger.user_role}")
                if j == 0:
                    await ctx.send(user_ui.permission_too_low_message(ctx.author.name))
                    return
            except AttributeError:
                print("AttributeError")
            '''
            #print(self.roles)
            #UserCommand.check_permission_role(self,ctx)
            
            if (UserCommand.check_permission_role(self,ctx) == 0):
                print("\n\nits a 0\n\n")
                await ctx.send(user_ui.permission_too_low_message(ctx.author.name), delete_after=FEEDBACK_MESSAGE_DISPLAY_TIME)
                return
            else:
                print("\n\nits a 1\n\n")
                
                
            # add a new user to the server someone who entered after bot creation can add automation
            if action == "add":
                if len(args) < 2 or len(args) > 3:
                    print(f"length: {len(args)}")
                    await ctx.send(user_ui.add_usage_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)
                    return
                users = discord.Client.get_all_members(bot)
                name = args[1]
                assigned = datetime.now()
                if len(args) <=2:
                    role = "student"
                else:
                    role = args[2]

                for x in users:
                    if(x.name == name or name == 'test'):
                        list = service.list_users()
                        for x in list:
                            if x.user_name == 'test':
                                return
                            if x.user_name == name:
                                await ctx.send(user_ui.user_already_on_list(x))
                                return
                        user = service.add_user(name, assigned, role)
                        if name == 'test':
                            return
                        await ctx.send(user_ui.user_added_message(user), delete_after=FEEDBACK_MESSAGE_DISPLAY_TIME)
                        return
                await ctx.send(user_ui.user_not_found_message(name), delete_after=FEEDBACK_MESSAGE_DISPLAY_TIME) 

            #list users on server
            elif action == "list":
                users = service.list_users()
                await ctx.send(user_ui.list_user_message(users))

            #alter someones permission raise or lower
            #no check values could be a non role currently
            elif action == "alter":
                if len(args) < 3 or len(args) > 3:
                    await ctx.send(user_ui.alter_usage_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)
                    return
                name = str(args[1])
                role = str(args[2])
                print(name)
                alter = service.set_permissions(name, role)
                await ctx.send(user_ui.role_altered_message(alter), delete_after=FEEDBACK_MESSAGE_DISPLAY_TIME)
            

            # create the tree with all users currently in server
            elif action == "create":
                guild = ctx.guild
                i=0
                users = service.list_users()
                if not users:
                    for member in guild.members:
                            if member.bot !=True:
                                if(member.id == ctx.guild.owner.id):
                                    user = service.add_user(member.name, datetime.now(), "teacher")
                                else:
                                    user = service.add_user(member.name, datetime.now(), "student")
                                print(f"user {i}: {member.name}")
                                i+=1
                            else:
                                print(f"bot {i}: {member.name}")
                                i+=1
            
            else:
                await ctx.send(user_ui.usage_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)

    def get_help_text(self):
        return f"!{self.name} [add|list|alter] <username> <role> - {self.description}"
