# ui/ping_ui.py
import discord

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
