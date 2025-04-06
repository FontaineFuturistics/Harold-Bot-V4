from discord.ext import commands

# Cog Class to hold the Cast commands
class CastCommands(commands.Cog):
    """Commands related to the cast utility"""

    # Init command
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Cast add command
    @commands.command()
    async def castadd(self, ctx, new_channel: int):
        """
        Adds a new channel to the cast list
        """
        # Try to find the channel
        channel_ref = self.bot.get_channel(new_channel)
        if channel_ref:
            self.bot.indat["CAST_CHANNELS"].append(new_channel)
            self.bot.indat.save()
            await ctx.send(f"#{channel_ref.name} in {channel_ref.guild.name} added to cast channel list")
        else:
            await ctx.send("Invalid channel id")

    # Cast remove command
    @commands.command()
    async def castremove(self, ctx, old_channel: int):
        """
        Remove a channel from the cast list.
        """
        # Try to find the channel
        channel_ref = self.bot.get_channel(old_channel)
        if channel_ref:
            self.bot.indat["CAST_CHANNELS"].remove(old_channel)
            self.bot.indat.save()
            await ctx.send(f"#{channel_ref.name} in {channel_ref.guild.name} removed from cast channel list")
        else:
            await ctx.send("Invalid channel id")

    # Cast list command
    @commands.command()
    async def castlist(self, ctx):
        """
        Prints every channel in the cast list
        """
        message = "```Here are all channels in the cast list:\n"
        for channel_id in self.bot.indat["CAST_CHANNELS"]:
            channel_ref = self.bot.get_channel(channel_id)
            message += f"#{channel_ref.name} in {channel_ref.guild.name}\n"
        message += "```"
        await ctx.send(message)

    # Cast command
    @commands.command()
    async def cast(self, ctx, message: str):
        """
        Broadcast message to cast channels.
        The user's message must be enclosed in quotes. The command is deleted after Harold's message is sent

        Example: f!say "Harold is the coolest bot"
        """
        for channel_id in self.bot.indat["CAST_CHANNELS"]:
            channel_ref = self.bot.get_channel(channel_id)
            await channel_ref.send(message)

# Setup function to load the cog
async def setup(bot: commands.Bot):
    await bot.add_cog(CastCommands(bot))