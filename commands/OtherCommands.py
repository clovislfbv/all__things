import discord
from discord.ext import commands
from blagues_api import BlaguesAPI
from pyjokes import *
import asyncio

allowed_channels = [796137851972485151, 697492398070300763, 796731890630787126, 631935311592554636] #["🤖・cow-bip-bop-bots", "bruh-botsandmusic", "test-bot", "général de mon propre serveur"]

def setup(bot):
    bot.add_cog(OtherCommands(bot))

def checks_in_bot_channel(channels, channel):
    global allowed_channels
    for i in range(len(allowed_channels)):
        channel_id = allowed_channels[i]
        print(channel_id, channel)
        if channel_id == channel:
            return True
    return False

async def show(blagues):
    return await blagues.random()

class OtherCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="blague", description="génère une blague aléatoirement")
    async def blague(self, ctx):
        current_channel = ctx.message.channel.id
        channels = ctx.guild.channels
        if checks_in_bot_channel(channels, current_channel):
            with open('token_blague.txt', 'r') as token_blague:
                blagues = BlaguesAPI(token_blague.read())

            result = await asyncio.gather(show(blagues))
            await ctx.send(result[0].joke)
            await ctx.send(result[0].answer)
        else:
            await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

    @commands.command()
    async def joke(self, ctx):
        current_channel = ctx.message.channel.id
        channels = ctx.guild.channels
        if checks_in_bot_channel(channels, current_channel) == True:
            await ctx.send(get_joke(category = "all"))
        else:
            await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

    @commands.command()
    async def dit(self, ctx, chiffre, *texte):
        current_channel = ctx.message.channel.id
        channels = ctx.guild.channels
        if checks_in_bot_channel(channels, current_channel) == True:
            if int(chiffre) > 10:
                await ctx.send("dsl j'ai été patch je peux plus faire plus de 10 messages")
            else:
                for i in range(int(chiffre)):
                    await ctx.send(" ".join(texte))
        else:
            await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")
