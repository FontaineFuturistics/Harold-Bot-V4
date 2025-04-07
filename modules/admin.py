from discord.ext import commands

# Cog class to hold the fun commands
class AdminCommands(commands.Cog):
    """A collection of commands for administrating and configuring Harold-bot"""

    # Init override
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #
    # Commands
    #

    # AddLogChannel command
    @commands.command()
    async def addlog(self, ctx, new_channel: int):
        """
        Adds a new channel to the log list
        """
        # Try to find the channel
        channel_ref = self.bot.get_channel(new_channel)
        if channel_ref:
            self.bot.indat["LOG_CHANNELS"].append(new_channel)
            self.bot.indat.save()
            await ctx.send(f"#{channel_ref.name} in {channel_ref.guild.name} added to log channel list")
        else:
            await ctx.send("Invalid channel id")

    # RemoveLogChannel command
    @commands.command()
    async def removelog(self, ctx, old_channel: int):
        """
        Remove a channel from the log list
        """
        # Try to find the channel
        channel_ref = self.bot.get_channel(old_channel)
        if channel_ref:
            self.bot.indat["LOG_CHANNELS"].remove(old_channel)
            self.bot.indat.save()
            await ctx.send(f"#{channel_ref.name} in {channel_ref.guild.name} removed from log channel list")
        else:
            await ctx.send("Invalid channel id")

    # LogList command
    @commands.command()
    async def listlog(self, ctx):
        """
        Prints every channel in the log list
        """
        message = "```Here are all channels in the log list:\n"
        for channel_id in self.bot.indat["LOG_CHANNELS"]:
            channel_ref = self.bot.get_channel(channel_id)
            message += f"#{channel_ref.name} in {channel_ref.guild.name}\n"
        message += "```"
        await ctx.send(message)

# Setup function to load the cog
async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCommands(bot))