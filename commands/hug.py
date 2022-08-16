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
    async def hug(self, ctx, member):
        current_channel = ctx.message.channel.id
        channels = ctx.guild.channels
        if checks_in_bot_channel(channels, current_channel) == True:
            if {ctx.author.mention} == member:
                ctx.send("T'es teubé ou quoi ? Tu peux pas te faire des calins à toi-même ?! Y a que toi pour être si teubé que ça !!")
            else:
                hugs = ["https://i.gifer.com/1ak.gif", "https://i.gifer.com/2HBY.gif", "https://i.gifer.com/GAMC.gif", "https://i.gifer.com/UQOJ.gif", "https://i.gifer.com/I3M0.gif", "https://i.gifer.com/I50j.gif", "https://i.gifer.com/MMuP.gif", "https://i.gifer.com/O2pp.gif", "https://i.gifer.com/1pg.gif", "https://i.gifer.com/APS3.gif"]
                huggy = hugs[randint(0,len(hugs)-1)]
                emb = discord.Embed(title=None, description = f"{ctx.author.mention} fait un calin à {member}", color=0x3498db)
                emb.set_image(url=f"{huggy}")
                await ctx.send( embed = emb)
        else:
            await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")
