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

class CogOwner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kiss(self, ctx,*, member):
        print(member)
        current_channel = ctx.message.channel.id
        channels = ctx.guild.channels
        if checks_in_bot_channel(channels, current_channel) == True:
            if {ctx.author.mention} == member:
                ctx.send("T'es teubé ou quoi ? Tu peux pas te donner de bisous à toi-même ?! Y a que toi pour être si teubé que ça !!")
            elif member == "bot Benjamin#3840":
                await ctx.send("Oh ! Je crois que je vais rougir.")
            else:
                kisses = ["https://i.gifer.com/iJb.gif", "https://i.gifer.com/V4hX.gif", "https://i.gifer.com/g33j.gif", "https://media.giphy.com/media/NKmXVFgwd8HKw/giphy.gif", "http://31.media.tumblr.com/bfbe6acecd87db57ad96c573d0e49e97/tumblr_mt2si1aAoC1sinrido1_500.gif", "https://i.gifer.com/abb.gif", "https://www.deviantart.com/inukagome134/art/Japan-Kiss-Animated-GIF-255408766"]
                kissy = kisses[randint(0, len(kisses)-1)]
                emb = discord.Embed(title=None, description = f"{ctx.author.mention} fait un bisou à {member}", color=0x3498db)
                emb.set_image(url=f"{kissy}")
                await ctx.send( embed = emb)
        else:
            await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")
