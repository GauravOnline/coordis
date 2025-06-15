# ui/ping_ui.py
import discord

def permission_too_low_message(name):
    return f"please check permissions level \"{name}\" does not have correct permissions to use this command"


def ping_response(latency_ms: int) -> discord.Embed:
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot latency: {latency_ms}ms",
        color=discord.Color.green()
    )

    embed.add_field(
        name="Status",
        value="✅ Bot is running normally",
        inline=False
    )

    return embed
