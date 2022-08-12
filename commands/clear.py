import discord
from discord.ext import commands

class CogOwner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, nombre : int):
        messages = await ctx.channel.history(limit = nombre + 1).flatten()
        for message in messages:
            await(message.delete())
