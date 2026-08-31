import os
import discord
from discord import app_commands
from discord.ext import commands

# ==========================================
# CONFIG
# ==========================================

TOKEN = os.getenv("BOT_TOKEN")

IP_MESSAGE = """ExtraCore.shockbyte.xyz
1.9-1.21.11"""

# ==========================================
# TIERS
# ==========================================

TIERS = [
    "LT5", "MT5", "HT5",
    "LT4", "MT4", "HT4",
    "LT3", "MT3", "HT3",
    "LT2", "MT2", "HT2",
    "LT1", "MT1", "HT1"
]

TIER_CHOICES = [
    app_commands.Choice(
        name=tier,
        value=tier
    )
    for tier in TIERS
]

# ==========================================
# DISCORD SETUP
# ==========================================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ==========================================
# BOT READY
# ==========================================

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()

        print("=" * 45)
        print(f"Logged in as: {bot.user}")
        print(f"Commands synced: {len(synced)}")
        print("IP AUTO-REPLY: ONLINE")
        print("TIER SYSTEM: ONLINE")
        print("=" * 45)

    except Exception as e:
        print(f"Sync error: {e}")

# ==========================================
# IP AUTO-REPLY
# ==========================================

@bot.event
async def on_message(message):

    # Ignore bots
    if message.author.bot:
        return

    # Detect "ip" as a separate word
    words = message.content.lower().split()

    if "ip" in words:
        await message.channel.send(IP_MESSAGE)

    # Keep slash/normal commands working
    await bot.process_commands(message)

# ==========================================
# /TIER COMMAND
# ==========================================

@bot.tree.command(
    name="tier",
    description="Add a player to the PvP tier list"
)
@app_commands.describe(
    player="Minecraft username",
    discord_member="Discord member",
    previous_tier="Previous tier",
    earned_tier="Earned tier",
    tiered_by="Person who tiered the player"
)
@app_commands.choices(
    previous_tier=TIER_CHOICES,
    earned_tier=TIER_CHOICES
)
async def tier(
    interaction: discord.Interaction,
    player: str,
    discord_member: discord.Member,
    previous_tier: app_commands.Choice[str],
    earned_tier: app_commands.Choice[str],
    tiered_by: discord.Member
):

    embed = discord.Embed(
        title="🏆 PvP TIER LIST",
        description=f"**{player}** has been tiered!"
    )

    embed.add_field(
        name="Player",
        value=f"**{player}**",
        inline=True
    )

    embed.add_field(
        name="Discord",
        value=discord_member.mention,
        inline=True
    )

    embed.add_field(
        name="Previous Tier",
        value=f"**{previous_tier.value}**",
        inline=True
    )

    embed.add_field(
        name="Earned Tier",
        value=f"**{earned_tier.value}**",
        inline=True
    )

    embed.add_field(
        name="Tiered By",
        value=tiered_by.mention,
        inline=False
    )

    embed.set_footer(
        text="PvP Tier List"
    )

    embed.timestamp = discord.utils.utcnow()

    await interaction.response.send_message(
        embed=embed
    )

# ==========================================
# START BOT
# ==========================================

if not TOKEN:
    raise RuntimeError(
        "BOT_TOKEN environment variable is missing!"
    )

bot.run(TOKEN)
