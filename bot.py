import os
import discord
from discord.ext import commands

BOT_TOKEN = os.getenv("BOT_TOKEN")

OLD_IP = "ExtraCore.shockbyte.xyz"
SERVER_VERSION = "1.9-1.21.11"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("IP replacement system is ONLINE")


@bot.event
async def on_message(message):

    # Ignore bots
    if message.author.bot:
        return

    # Check if message contains the IP
    if OLD_IP.lower() in message.content.lower():

        # Replace the IP with IP + version
        new_content = message.content.replace(
            OLD_IP,
            f"{OLD_IP}\n{SERVER_VERSION}"
        )

        try:
            # Delete original
            await message.delete()

            # Send replacement
            await message.channel.send(
                new_content
            )

            print(
                f"Replaced message from {message.author}"
            )

        except discord.Forbidden:
            print("Missing Manage Messages permission.")

        except Exception as e:
            print(f"Error: {e}")

    await bot.process_commands(message)


if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")

bot.run(BOT_TOKEN)
