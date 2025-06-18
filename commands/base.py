from services.user_service import UserService
from db.base import get_session
"""
Base Command Interface

This module defines the base Command class that all other commands should inherit from.
"""


class Command:
    """Interface for all bot commands"""

    def __init__(self, name, description, roles):
        """
        Initialize a new command.

        Args:
            name (str): The name of the command
            description (str): Description of what the command does
            roles (list): List of roles that can use this command
        """
        self.name = name
        self.description = description
        self.roles = roles  # List of roles that can use this command

    async def execute(self, ctx, *args):
        
        """
        Execute the command logic.

        Args:
            ctx: The Discord context
            *args: Additional arguments passed to the command

        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement execute method")

    def get_help_text(self):
        """
        Get help text for this command.

        Returns:
            str: Help text describing the command usage
        """
        return f"!{self.name} - {self.description}"
    
    def check_permission_role(self,ctx):
        with get_session() as session:
            service = UserService(session)


            # get user permisssion level of command operator
            try:
                j = 0
                messenger = service.get_user(ctx.author.name)
                if(ctx == 'test'):
                    return 1
                for role in self.roles:
                    print (f"\n\nrole: {role}\n{self.roles}\n\n")
                    if messenger.user_role != role:
                        print(f"self.roles: {role}  user role: {messenger.user_role}")
                    else:
                        j=1
                        print(f"self.roles: {role}  user role: {messenger.user_role}")
                #if j == 0:
                    #await ctx.send(user_ui.permission_too_low_message(ctx.author.name))
                    
                return j
            except AttributeError:
                print("AttributeError")