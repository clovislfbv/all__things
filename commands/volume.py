import discord
from discord.ext import commands

class AudioCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['v', 'vol'])
    async def volume(self, ctx, volume: int):
        current_channel = ctx.message.channel.id
        channels = ctx.guild.channels
        if checks_in_bot_channel(channels, current_channel) == True:
            if ctx.voice_client is None:
                return await ctx.send("Not connected to voice channel")

            print(volume/100)

            ctx.voice_client.source.volume = volume / 100
            await ctx.send(f"Changed volume to {volume}%")
        else:
            await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")
