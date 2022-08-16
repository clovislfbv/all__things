import discord
from discord.ext import commands

class AudioCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def leave(self, ctx):
        global url_queue
        current_channel = ctx.message.channel.id
        channels = ctx.guild.channels
        if checks_in_bot_channel(channels, current_channel) == True:
            client = ctx.guild.voice_client
            await client.disconnect()
            musics[ctx.guild] = []
            url_queue = []
        else:
            await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")
