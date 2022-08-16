import discord
from discord.ext import commands

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, user : discord.User, *reason):
        reason = " ".join(reason)
        await ctx.guild.kick(user, reason = reason)
        await ctx.send(f"{user} a été kick pour la reason suivante : {reason}.")
        print(reason)
