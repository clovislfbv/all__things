import discord
from discord.ext import commands
from random import randint

allowed_channels = [796137851972485151, 697492398070300763, 796731890630787126, 631935311592554636] #["🤖・cow-bip-bop-bots", "bruh-botsandmusic", "test-bot", "général de mon propre serveur"]

def checks_in_bot_channel(channels, channel):
    global allowed_channels
    for i in range(len(allowed_channels)):
        channel_id = allowed_channels[i]
        print(channel_id, channel)
        if channel_id == channel:
            return True
    return False

class GifCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def slap(ctx, member):
        current_channel = ctx.message.channel.id
        channels = ctx.guild.channels
        if checks_in_bot_channel(channels, current_channel) == True:
            if ctx.author.mention == member:
                ctx.send("T'es teubé ou quoi ? Tu peux pas te donner de claques à toi-même ?! Y a que toi pour être si teubé que ça !!")
            else:
                slaps = ["https://i.gifer.com/XaaW.gif", "https://i.gifer.com/2eNz.gif", "https://i.gifer.com/2Dji.gif", "https://i.gifer.com/1Vbb.gif", "https://i.gifer.com/K03.gif", "https://i.gifer.com/DjuN.gif", "https://i.gifer.com/Djw.gif", "https://i.gifer.com/4kpG.gif", "https://i.gifer.com/K02.gif"]
                slappy = slaps[randint(0, len(slaps)-1)]
                emb = discord.Embed(title=None, description = f"{ctx.author.mention} met une claque à {member}", color=0x3498db)
                emb.set_image(url=f"{slappy}")
                await ctx.send( embed = emb)
        else:
            await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")
