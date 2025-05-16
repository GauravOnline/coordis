"""
Homework Command Implementation

A command that adds homework items and responds with a fun message.
"""
import discord
from commands.base import Command


class HomeworkCommand(Command):
    """Homework command to add new homework items"""

    def __init__(self):
        super().__init__(
            name="hw",
            description="Adds a new homework item",
            roles=["student", "teacher"]  # Available to students and teachers
        )

    async def execute(self, ctx, *args):
        """
        Process the homework command.

        Args:
            ctx: The Discord context
            *args: The homework description
        """
        if args[0] is None:
            await ctx.send("You didn't provide a homework description! Usage: `!homework [description]`")
            return

        # Join all arguments into a single homework description
        homework_description = " ".join(args)

        # Here you would typically save this to a database
        # For example:
        # homework = Homework(description=homework_description, assigned_by=ctx.author.id)
        # session.add(homework)
        # session.commit()

        # Create embed response
        embed = discord.Embed(
            title="📚 New Homework Item",
            description=homework_description,
            color=discord.Color.red()  # Red for urgency!
        )

        # Add footer with author info
        embed.set_footer(text=f"Assigned by {ctx.author.display_name}")

        # Send the embed
        await ctx.send(embed=embed)

        # Send the fun response
        await ctx.send(f"Say goodbye to your weekend! 😭 **{homework_description}**")

    def get_help_text(self):
        """
        Get help text for this command.

        Returns:
            str: Help text describing the command usage
        """
        return f"!{self.name} <description> - {self.description}"
