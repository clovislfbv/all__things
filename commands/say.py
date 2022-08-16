import discord
from discord.ext import commands
import check

class OtherCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, chiffre, *texte):
        checker = self.bot.add_cog(check.checks(self.bot))
        current_channel = ctx.message.channel.id
        channels = ctx.guild.channels
        if checker.checks_in_bot_channel(channels, current_channel) == True:
            if int(chiffre) > 10:
                await ctx.send("dsl j'ai été patch je peux plus faire plus de 10 messages")
            else:
                for i in range(int(chiffre)):
                    await ctx.send(" ".join(texte))
                await ctx.send("Si tu en as besoin tu peux écrire $aide pour avoir des explication sur toutes les commandes disponible avec ce bot.")
        else:
            await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")
