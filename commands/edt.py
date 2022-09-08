import discord
from discord.ext import commands
import requests as r
from datetime import datetime
import vobject
import os.path
import os
import pytz

path = "/home/pi/Téléchargements/GroupCalendar.ics"

if not(os.path.exists(path)):
    os.remove(path)

allowed_channels = [796137851972485151, 697492398070300763, 796731890630787126, 631935311592554636] #["🤖・cow-bip-bop-bots", "bruh-botsandmusic", "test-bot", "général de mon propre serveur"]

def checks_in_bot_channel(channels, channel):
    global allowed_channels
    for i in range(len(allowed_channels)):
        channel_id = allowed_channels[i]
        print(channel_id, channel)
        if channel_id == channel:
            return True
    return False

lastdlday = None
lastedt = None

class ClassCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def edt(self, ctx, day=None):
        global lastdlday, lastedt

        if day is not None:
            today=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            todayStr = today.isoformat()
            todayFinal = ""
            todayStr = todayStr.split("-")
            todayStr[2] = todayStr[2][0] + todayStr[2][1]
            for i in range(len(todayStr)-1):
                todayFinal = "/" + todayStr[i] + todayFinal
            todayFinal = todayStr[2] + todayFinal

            if day != todayFinal:
                day = day.split("/")
                today = datetime(int(day[2]), int(day[1]), int(day[0]), 0, 0)
        else:
            today=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        print(today, lastdlday)
        if lastdlday is not None and (datetime.now()-lastdlday).days <= 0:
            cal = lastedt
            print("ics already installed")
        else:
            response = r.get("https://zeus.ionis-it.com/api/group/325/ics/Yzi0mVNPNp")
            data = response.text
            cal = vobject.readOne(data)

            lastdlday = datetime.now()
            lastedt = cal

            print("installing ics...")

        emb = discord.Embed(title=today.strftime("%d/%m/%Y"), color=0x3498db)
        for ev in cal.vevent_list:
            start_time = ev.dtstart.valueRepr().isoformat().split("-")
            variable = start_time[0]
            start_time[0] = start_time[2][0] + start_time[2][1]
            start_time[2] = variable
            time = datetime(int(start_time[2]), int(start_time[1]), int(start_time[0]), 0, 0)
            date_start = ev.dtstart.value.astimezone(pytz.timezone("Europe/Paris")).strftime("%H:%M")
            date_end = ev.dtend.value.astimezone(pytz.timezone("Europe/Paris")).strftime("%H:%M")
            if time == today:
                field = emb.add_field(name = ev.summary.valueRepr(), value = "time start : " + date_start + "\n" + "time end : " + date_end + "\n" + 'Description : ' + ev.description.valueRepr() + "\n" + "location : " + ev.location.value)

        msg = await ctx.send(embed = emb)
