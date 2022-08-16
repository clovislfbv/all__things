import discord
from discord.ext import commands

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx, user : discord.User, *reason):
        reason = " ".join(reason)
        await ctx.guild.ban(user, reason = reason)
        await ctx.send(f"{user} a été ban pour la reason suivante : {reason}.")
        print(reason)
