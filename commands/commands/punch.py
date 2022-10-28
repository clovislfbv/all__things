import discord
from discord.ext import commands

class GifCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def punch(self, ctx, member):
        current_channel = ctx.message.channel.id
        channels = ctx.guild.channels
        if checks_in_bot_channel(channels, current_channel) == True:
            if {ctx.author.mention} == member:
                ctx.send("T'es teubé ou quoi ? Tu peux pas te donner des coups de poing à toi-même ?! Y a que toi pour être si teubé que ça !!")
            else:
                punchs = ["https://i.gifer.com/C225.gif", "https://i.gifer.com/RAKN.gif", "https://i.gifer.com/RUZS.gif", "https://i.gifer.com/HR4q.gif", "https://i.gifer.com/Tr72.gif"]
                punchy = punchs[randint(0, len(punchs)-1)]
                emb = discord.Embed(title=None, description = f"{ctx.author.mention} met un **ENORME !!!** coup de poing à {member}", color=0x3498db)
                emb.set_image(url=f"{punchy}")
                await ctx.send( embed = emb)
        else:
            await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")
