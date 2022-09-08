import discord
from discord.ext import commands
import check

allowed_channels = [796137851972485151, 697492398070300763, 796731890630787126, 631935311592554636] #["🤖・cow-bip-bop-bots", "bruh-botsandmusic", "test-bot", "général de mon propre serveur"]

def checks_in_bot_channel(channels, channel):
    global allowed_channels
    for i in range(len(allowed_channels)):
        channel_id = allowed_channels[i]
        print(channel_id, channel)
        if channel_id == channel:
            return True
    return False

class OtherCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, chiffre, *texte):
        checker = self.bot.add_cog(check.checks(self.bot))
        current_channel = ctx.message.channel.id
        channels = ctx.guild.channels
        if checks_in_bot_channel(channels, current_channel) == True:
            if int(chiffre) > 10:
                await ctx.send("dsl j'ai été patch je peux plus faire plus de 10 messages")
            else:
                for i in range(int(chiffre)):
                    await ctx.send(" ".join(texte))
                await ctx.send("Si tu en as besoin tu peux écrire $aide pour avoir des explication sur toutes les commandes disponible avec ce bot.")
        else:
            await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")
