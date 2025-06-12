import discord


def prompt_for_role():
    return "Please specify your role: `!help student` or `!help teacher`"


def unknown_role_message():
    return "Unknown role. Please use `!help student` or `!help teacher`"


def help_embed(commands, role):
    embed = discord.Embed(
        title=f"📚 {role.capitalize()} Commands",
        description="Here are the commands available to you:",
        color=discord.Color.blue(),
    )

    for cmd in commands:
        help_text = cmd.get_help_text()
        command_name, description = help_text.split(" - ", 1)
        embed.add_field(name=command_name, value=description, inline=False)

    return embed
