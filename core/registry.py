"""
Command Registry

Singleton registry that maintains all available bot commands.
"""


class CommandRegistry:
    """Central registry for all bot commands"""
    _instance = None

    def __new__(cls):
        """
        Create a new CommandRegistry instance or return the existing one (singleton pattern).

        Returns:
            CommandRegistry: The singleton instance
        """
        if cls._instance is None:
            cls._instance = super(CommandRegistry, cls).__new__(cls)
            cls._instance.commands = []
        return cls._instance

    def register_command(self, command):
        """
        Register a new command.

        Args:
            command: Command object to register
        """
        self.commands.append(command)

    def get_all_commands(self):
        """
        Get all registered commands.

        Returns:
            list: All registered Command objects
        """
        return self.commands

    def get_commands_by_role(self, role):
        """
        Get commands available for a specific role.

        Args:
            role (str): Role to filter commands by

        Returns:
            list: Command objects available for the specified role
        """
        return [cmd for cmd in self.commands if role in cmd.roles or "all" in cmd.roles]