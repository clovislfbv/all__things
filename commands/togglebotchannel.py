import discord
from discord.ext import commands

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def togglebotchannel(self, ctx):
        global allowed_channels
        current_channel = ctx.message.channel.id
        allowed_channels.append(current_channel)
        await ctx.send("Cette channel est désormais un bot channel.")
