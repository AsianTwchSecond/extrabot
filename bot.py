import os
import discord
from discord.ext import commands

# =========================
# CONFIG
# =========================

TOKEN = os.getenv("BOT_TOKEN")

IP_MESSAGE = """ExtraCore.shockbyte.xyz
1.9-1.21.11"""

# =========================
# DISCORD SETUP
# =========================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# =========================
# BOT READY
# =========================

@bot.event
async def on_ready():
    print("=" * 40)
    print(f"Bot: {bot.user}")
    print("IP AUTO-REPLY: ONLINE")
    print("=" * 40)

# =========================
# MESSAGE DETECTION
# =========================

@bot.event
async def on_message(message):

    # Ignore messages from bots
    if message.author.bot:
        return

    # Convert message to lowercase
    content = message.content.lower()

    # Trigger when "ip" is mentioned
    words = content.split()

    if "ip" in words:
        await message.channel.send(IP_MESSAGE)

    # Keep commands working
    await bot.process_commands(message)

# =========================
# START BOT
# =========================

if not TOKEN:
    raise RuntimeError(
        "BOT_TOKEN environment variable is missing!"
    )

bot.run(TOKEN)
