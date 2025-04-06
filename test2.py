#
# GET THE TOKEN
#

import jhandler

# Load config
con = jhandler.JHandler("./config/config.json")

# Load token from .env
env_file = open(con["ENV_PATH"], "r")
env_dict = {}
for line in env_file:
        # Skip empty lines and comments
        if line.strip() and not line.startswith("#"):
            key, value = line.strip().split("=", 1)
            env_dict[key] = value
token = env_dict["TOKEN"]

# Load instance data
indat = jhandler.JHandler(con["ID_PATH"])

#
# Basic Bot Setup
#

import discord
from discord.ext import commands

# Setup intents
intents = discord.Intents.default()
intents.message_content = True
desc = """Welcome to Harold-bot V4!
Harold is currently under development in his fourth iteration. As such he has very little functionality and will be offline most of the time. A full release will be announced sometime in the future."""
bot = commands.Bot(command_prefix=con["CMD_PRFX"], intents=intents, description=desc)

#
# Ready Message
#
# Print ready messages
from datetime import datetime
@bot.event
async def on_ready():
      # Log Message
      print(f'Bot activated at {datetime.now().strftime("%H:%M")}')

      # Send message into our log channels
      for channel_id in indat["LOG_CHANNELS"]:
         await bot.get_channel(channel_id).send(f'I have awoken now at {datetime.now().strftime("%H:%M")}')

      # Set up status
      game = discord.Game("with your fate | f!help")
      await bot.change_presence(status=discord.Status.online, activity=game)

      # Save config and instance data jhandlers to the bot
      bot.indat = indat
      bot.con = con

      # Load cogs
      await bot.load_extension("modules.cast")
      await bot.load_extension("modules.fun")

#
# Message Handler
#

@bot.event
async def on_message(message):

    # Confirm we have received the message because our latency is terrible
    print("processing message: \"" + message.content + "\" in " + message.guild.name) # Confirm that we have seen a message

    # Ensure commands are processed
    await bot.process_commands(message)


#
# Command Handler
#

# TODO: Make command description first lines shorter
# TODO: Figure out argument descriptions for f!help
# TODO: Figure out command categories for f!help
# TODO: Transition to slash commands

# Ping command
@bot.command()
async def ping(ctx):
    """Ping pong"""
    await ctx.send('pong')

#
# Start bot
#
bot.run(token)