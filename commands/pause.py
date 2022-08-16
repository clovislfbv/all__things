import discord
from discord.ext import commands

class AudioCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pause(self, ctx):
        current_channel = ctx.message.channel.id
        channels = ctx.guild.channels
        if checks_in_bot_channel(channels, current_channel) == True:
            client = ctx.guild.voice_client
            if not client.is_paused():
                client.pause()
                await ctx.send("La musique que vous écoutiez a bien été mis sur pause.")
        else:
            await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")
