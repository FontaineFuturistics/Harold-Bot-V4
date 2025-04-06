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

      # Set out status
      game = discord.Game("with your fate | f!help")
      await bot.change_presence(status=discord.Status.online, activity=game)


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

# Cast add command
@bot.command()
async def castadd(ctx, new_channel: int):
     """
     Adds a new channel to the cast list
     """
     # Try to find the channel
     channel_ref = bot.get_channel(new_channel)
     if channel_ref:
         indat["CAST_CHANNELS"].append(new_channel)
         indat.save()
         await ctx.send(f"#{channel_ref.name} in {channel_ref.guild.name} added to cast channel list")
     else:
         await ctx.send("Invalid channel id")

# Cast remove command
@bot.command()
async def castremove(ctx, old_channel: int):
     """
     Remove a channel from the cast list.
     """
     # Try to find the channel
     channel_ref = bot.get_channel(old_channel)
     if channel_ref:
         indat["CAST_CHANNELS"].remove(old_channel)
         indat.save()
         await ctx.send(f"#{channel_ref.name} in {channel_ref.guild.name} removed from cast channel list")
     else:
        await ctx.send("Invalid channel id")

# Cast list command
@bot.command()
async def castlist(ctx):
     """
     Prints every channel in the cast list
     """
     message = "```Here are all channels in the cast list:\n"
     for channel_id in indat["CAST_CHANNELS"]:
          channel_ref = bot.get_channel(channel_id)
          message += f"#{channel_ref.name} in {channel_ref.guild.name}\n"
     message += "```"
     await ctx.send(message)

# Cast command
@bot.command()
async def cast(ctx, message: str):
     """
     Broadcast message to cast channels.
     The user's message must be enclosed in quotes. The command is deleted after Harold's message is sent

     Example: f!say "Harold is the coolest bot"
     """
     #final_message = ""
     #for message_part in message:
     #     final_message += message_part + " "
     #final_message = final_message.strip()
     for channel_id in indat["CAST_CHANNELS"]:
          channel_ref = bot.get_channel(channel_id)
          #await channel_ref.send(final_message)
          await channel_ref.send(message)

# Say command
# Allows a user to impersonate harold
@bot.command()
async def say(ctx, message: str):
     """
     Repeats the users message. 
     The user's message must be enclosed in quotes. The command is deleted after Harold's message is sent

     Example: f!say "Harold is the coolest bot"
     """
     # Delete the command
     await ctx.message.delete()

     # Get the message to say
     #final_message = ""
     #for message_part in message:
     #     final_message += message_part + " "
     #final_message = final_message.strip()

     # Say it
     #await ctx.send(final_message)
     await ctx.send(message)

#
# Start bot
#
bot.run(token)