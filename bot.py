import os
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")
    print("Tier List System ONLINE")


@bot.tree.command(
    name="tier",
    description="Add a player to the PvP tier list"
)
@app_commands.describe(
    player="Minecraft player name",
    discord_name="Discord username",
    previous_tier="Previous tier",
    earned_tier="New earned tier"
)
async def tier(
    interaction: discord.Interaction,
    player: str,
    discord_name: str,
    previous_tier: str,
    earned_tier: str
):

    embed = discord.Embed(
        title="🏆 PvP TIER LIST",
        description=f"**{player}** has earned a new tier!",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="👤 Player",
        value=f"`{player}`",
        inline=False
    )

    embed.add_field(
        name="💬 Discord",
        value=f"`{discord_name}`",
        inline=False
    )

    embed.add_field(
        name="📉 Previous Tier",
        value=f"`{previous_tier}`",
        inline=True
    )

    embed.add_field(
        name="📈 Earned Tier",
        value=f"`{earned_tier}`",
        inline=True
    )

    embed.set_footer(
        text=f"Tiered by {interaction.user.display_name}"
    )

    await interaction.response.send_message(embed=embed)


if not TOKEN:
    raise RuntimeError("BOT_TOKEN is missing!")

bot.run(TOKEN)
