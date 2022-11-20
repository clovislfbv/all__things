import discord
from discord.ext import commands
import requests as r
from requests.auth import HTTPBasicAuth
from datetime import datetime
import vobject
import pytz

allowed_channels = [796137851972485151, 697492398070300763, 796731890630787126, 631935311592554636] #["🤖・cow-bip-bop-bots", "bruh-botsandmusic", "test-bot", "général de mon propre serveur"]

def checks_in_bot_channel(channels, channel):
    global allowed_channels
    for i in range(len(allowed_channels)):
        channel_id = allowed_channels[i]
        print(channel_id, channel)
        if channel_id == channel:
            return True
    return False

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
        ''' donne notre emploi du temps (format argument : dd/mm/yyyy), l'argument par défaut est à la date d'aujourd'hui '''
        global lastdlday, lastedt

        if day is not None:
            number_slash = 0
            for char in day:
                if char == "/":
                    number_slash += 1
            print(number_slash)
            if number_slash == 2:
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
            print("test")
        else:
            number_slash = 2
            today=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        if number_slash == 2:
            if lastdlday is not None and (datetime.now()-lastdlday).days <= 0:
                cal = lastedt
                print("ics already installed")
            else:
                url = open('edt_token.txt').read() 
                response = r.get(url)
                print(response.status_code)
                print(response.text)
                response.encoding = "utf-8"
                print(response)
                print("test1")
                data = response.text
                print("test2")
                print(data)
                cal = vobject.readOne(data)
                print("test3")

                lastdlday = datetime.now()
                lastedt = cal

                print("installing ics...")

            emb = discord.Embed(title=today.strftime("%d/%m/%Y"), color=0x3498db)
            dates = []
            print("test4")
            for ev in cal.vevent_list:
                start_time = ev.dtstart.valueRepr().isoformat().split("-")
                variable = start_time[0]
                start_time[0] = start_time[2][0] + start_time[2][1]
                start_time[2] = variable
                time = datetime(int(start_time[2]), int(start_time[1]), int(start_time[0]), 0, 0)
                if time == today:
                    date_start = ev.dtstart.value.astimezone(pytz.timezone("Europe/Paris")).strftime("%H:%M")
                    date_end = ev.dtend.value.astimezone(pytz.timezone("Europe/Paris")).strftime("%H:%M")
                    dates.append(date_end)
                    dates.sort()
                    for i in range(len(dates)):
                        if dates[i] == date_end:
                            index = i
                    field = emb.insert_field_at(index=index, name = ev.summary.valueRepr(), value = "time start : " + date_start + "\n" + "time end : " + date_end + "\n" + "location : " + ev.location.value)

            if len(dates) == 0:
                emb.add_field(name = "PAS COURS !!", value = "Aujourd'hui, il n'y a pas cours")
            msg = await ctx.send(embed = emb)
        else:
            print("bad argument")
            await ctx.send("Je n'ai pas compris la date que tu as mise. La date que tu écris doit être sous le format `dd/mm/yyyy`. Cependant, si tu ne mets aucune date en argument, la commande montrera l'emploi du temps d'aujourd'hui.")
