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