import discord
from discord.ext import commands

allowed_channels = [796137851972485151, 697492398070300763, 796731890630787126, 631935311592554636] #["🤖・cow-bip-bop-bots", "bruh-botsandmusic", "test-bot", "général de mon propre serveur"]

class checks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def checks_in_bot_channel(channels, channel):
        global allowed_channels
        for i in range(len(allowed_channels)):
            channel_id = allowed_channels[i]
            print(channel_id, channel)
            if channel_id == channel:
                return True
        return False
