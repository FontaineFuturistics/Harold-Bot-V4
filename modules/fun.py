from discord.ext import commands

# Cog class to hold the fun commands
class FunCommands(commands.Cog):
    """A collection of commands that serve no useful purpose besides entertainment"""

    # Init override
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Say command
    # Allows a user to impersonate harold
    @commands.command()
    async def say(ctx, message: str):
        """
        Repeats the users message. 
        The user's message must be enclosed in quotes. The command is deleted after Harold's message is sent

        Example: f!say "Harold is the coolest bot"
        """
        # Delete the command
        await ctx.message.delete()

        # Say it
        await ctx.send(message)

# Setup function to load the cog
async def setup(bot: commands.Bot):
    await bot.add_cog(FunCommands(bot))