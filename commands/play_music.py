import discord
from discord.ext import commands
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import urllib.parse, urllib.request, re
from youtube_dl import *
from random import shuffle
import asyncio

url_queue = []
musics = {}

pays = {"FR" : '37i9dQZEVXbIPWwFssbupI?si=1e836528e2384a70', "UK" : "37i9dQZEVXbLnolsZ8PSNw?si=bcc5a83311b54e67", "USA" : "37i9dQZEVXbLRQDuF5jeBp?si=0b5e105bed784940",  "WORLD" : '37i9dQZEVXbMDoHDwVN2tF?si=510c4902c6ba4d80', "ES" : "37i9dQZEVXbNFJfN1Vw8d9?si=3087bda4c2df4961", "IN" : "37i9dQZEVXbLZ52XmnySJg?si=085b180ae65b4609", "PH" : "37i9dQZEVXbNBz9cRCSFkY?si=b30c3057903f4ef5", "TU" : "37i9dQZEVXbIVYVBNw9D5K?si=3f4a25f140904d2f", "JA" : "37i9dQZEVXbKXQ4mDTEBXq?si=5971ca3ffc744d15", "PB" : "37i9dQZEVXbKCF6dqVpDkS?si=0b8e08dc941e4b47", "IT" : "37i9dQZEVXbIQnj7RRhdSX?si=3d1f7cb768e14959", "RU" : "37i9dQZEVXbL8l7ra5vVdB?si=28dc400fabb8424b"}

allowed_channels = [796137851972485151, 697492398070300763, 796731890630787126, 631935311592554636, 849756838962528316] #["🤖・cow-bip-bop-bots", "bruh-botsandmusic", "test-bot", "général de mon propre serveur"]

def checks_in_bot_channel(channels, channel):
    global allowed_channels
    for i in range(len(allowed_channels)):
        channel_id = allowed_channels[i]
        print(channel_id, channel)
        if channel_id == channel:
            return True
    return False

def play_song(ctx, bot, client, queu, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url, before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))
    global url_queue

    def next(_):
        global liste_tracks, ydl_opts, message_channel, current_music
        if len(url_queue) > 0 and len(queu) == 0:
            url = url_queue[0]
            video = Video(url)
            queu.append(video)
            print(url_queue, " ", queu)

        if len(queu) > 0:
            new_song = queu[0]
            current_music = url_queue[0]
            del queu[0]
            del url_queue[0]
            print(current_music)
            with YoutubeDL(ydl_opts) as ydl:
                title = f"%s" %(ydl.extract_info(current_music, download=False)['title'])
            asyncio.run_coroutine_threadsafe(ctx.send(f"Je lance **{title}** : {current_music}"), bot.loop)
            play_song(ctx, bot, client, queu, new_song)
            ctx.voice_client.source.volume = 50 / 100
            print(50/100)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)
    client.play(source, after=next)

def my_hook(d):
    if d['status'] == 'downloading':
        print ("downloading "+ str(round(float(d['downloaded_bytes'])/float(d['total_bytes'])*100,1))+"%")
    if d['status'] == 'finished':
        filename=d['filename']
        print(filename)

class Video:
    def __init__(self, link):
        ydl_opts = {
            'format': 'bestvideo[width<=1080]+bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [my_hook]
        }
        with YoutubeDL(ydl_opts) as ydl:
            video = ydl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]

ydl_opts = {
    'format': 'bestvideo[width<=1080]+bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'progress_hooks': [my_hook]
}

def checks_in_bot_channel(channels, channel):
    global allowed_channels
    for i in range(len(allowed_channels)):
        channel_id = allowed_channels[i]
        print(channel_id, channel)
        if channel_id == channel:
            return True
    return False

class AudioCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def play_music(self, ctx, code_pays, rang):
        current_channel = ctx.message.channel.id
        channels = ctx.guild.channels
        if checks_in_bot_channel(channels, current_channel) == True:
            global url_queue, ydl_opts, current_music, pays
            if code_pays not in pays:
                await ctx.send("Dsl, mais je ne connais pas le code de ce pays. utilise la commande '$aide' pour voir tout les codes des pays disponibles et leur orthographe exacte.")
            else:
                link_pays = "spotify:user:spotifycharts:playlist:" + pays[code_pays]
                print(link_pays)
            real_liste_tracks = []
            real_liste_artists = []
            liste_tracks = []
            liste_artists = []
            client = ctx.guild.voice_client
            channel = ctx.author.voice

            if channel is None:
                return await ctx.send("Not connected to voice channel")

            with open('token_spo.txt', 'r') as token_spo:
                client_credentials_manager = SpotifyClientCredentials(client_id="358a882e0433437896ed0c77a429023b",client_secret=token_spo.read())
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        
            playlist_id = link_pays
            results = sp.playlist(playlist_id)
            tracks = results['tracks']
            for i, item in enumerate(tracks['items']):
                track = item['track']
                real_liste_tracks.append(track['name'])
                real_liste_artists.append(track['artists'][0]['name'])

            for i in range(26):
                liste_tracks.append(real_liste_tracks[i])
                liste_artists.append(real_liste_artists[i])

            if rang != "all":
                if int(rang) > len(liste_tracks):
                    ctx.send("Mec t'a écris un nombre trop grand. Y a aucune musique à cette place.")
                else:
                    music_playing = liste_tracks[int(rang) - 1] + " " + liste_artists[int(rang) - 1]
            else:
                await ctx.send("Veuillez patienter lors du chargement des musiques")
                shuffle(liste_tracks)
                music_playing = liste_tracks[0] + " " + liste_artists[0]

            query_string = urllib.parse.urlencode({
                'search_query': music_playing
            })
            htm_content = urllib.request.urlopen(
                'https://www.youtube.com/results?' + query_string
)
            search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())

            video = 'http://www.youtube.com/watch?v=' + search_results[0]
            with YoutubeDL(ydl_opts) as ydl:
                liste = [f"1 :  %s" %(ydl.extract_info(video, download=False)["title"])]

            url = 'http://www.youtube.com/watch?v=' + search_results[0]
            print("play")

            if rang == "all":
                for i in range(1, 26):
                    music_playing = liste_tracks[i] + " " + liste_artists[i]
                    query_string = urllib.parse.urlencode({
                        'search_query': music_playing
                    })
                    htm_content = urllib.request.urlopen(
                        'https://www.youtube.com/results?' + query_string
                    )
                    search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())

                    video = 'http://www.youtube.com/watch?v=' + search_results[0]
                    url_queue.append(video)
            title = f"%s" %(ydl.extract_info(url, download=False)['title'])

            if client and client.channel:
                video = Video(url)
                url_queue.append(url)
                musics[ctx.guild].append(video)
                print("dans la file d'attente")
                await ctx.send(f"**{title}** {video.url} a été ajouté à la file d'attente")
            else:
                channel = ctx.author.voice.channel
                video = Video(url)
                musics[ctx.guild] = []
                client = await channel.connect()
                current_music = title
                msg = await ctx.send(f"Je lance **{title}** :  {video.url}")
                play_song(ctx, self.bot, client, musics[ctx.guild], video)
                ctx.voice_client.source.volume = 50 / 100
                print(50/100)
        else:
            await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")
