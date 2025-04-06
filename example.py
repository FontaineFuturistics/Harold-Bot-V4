import discord
from discord.ext import commands
from datetime import datetime # To get time
import jhandler

# Documentation link: https://discordpy.readthedocs.io/en/stable/quickstart.html

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

# Setup intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.message_content = True

# Setup bot
client = discord.Client(intents=intents) # For use in reading messages and handling events
bot = commands.Bot(command_prefix=con["CMD_PRFX"], intents=intents) # For f! command
print("Prefix is: \"" + con["CMD_PRFX"] + "\"")

# Print ready messages
@client.event
async def on_ready():
    print(f'I have awoken now at {datetime.now().strftime("%H:%M")}')

# Respond to $hello
@client.event
async def on_message(message):

    # Confirm we have received the message because our latency is terrible
    print("processing message: \"" + message.content + "\" in " + message.guild.name) # Confirm that we have seen a message
    # Ignore our messages
    if message.author == client.user:
        return
    # Respond to $hello
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    # Ensure commands are processed
    await bot.process_commands(message)

#
# Commands
#
@bot.command()
async def foo(ctx, arg):
    print("foo received")
    await ctx.send(arg)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def ctest(ctx):
    print("yep")
    await ctx.message.channel.send("This is a test")

# Run the bot
client.run(env_dict["TOKEN"])
