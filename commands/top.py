import discord
from discord.ext import commands
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

pays = {"FR" : '37i9dQZEVXbIPWwFssbupI?si=1e836528e2384a70', "UK" : "37i9dQZEVXbLnolsZ8PSNw?si=bcc5a83311b54e67", "USA" : "37i9dQZEVXbLRQDuF5jeBp?si=0b5e105bed784940",  "WORLD" : '37i9dQZEVXbMDoHDwVN2tF?si=510c4902c6ba4d80', "ES" : "37i9dQZEVXbNFJfN1Vw8d9?si=3087bda4c2df4961", "IN" : "37i9dQZEVXbLZ52XmnySJg?si=085b180ae65b4609", "PH" : "37i9dQZEVXbNBz9cRCSFkY?si=b30c3057903f4ef5", "TU" : "37i9dQZEVXbIVYVBNw9D5K?si=3f4a25f140904d2f", "JA" : "37i9dQZEVXbKXQ4mDTEBXq?si=5971ca3ffc744d15", "PB" : "37i9dQZEVXbKCF6dqVpDkS?si=0b8e08dc941e4b47", "IT" : "37i9dQZEVXbIQnj7RRhdSX?si=3d1f7cb768e14959", "RU" : "37i9dQZEVXbL8l7ra5vVdB?si=28dc400fabb8424b"}

allowed_channels = [796137851972485151, 697492398070300763, 796731890630787126, 631935311592554636] #["🤖・cow-bip-bop-bots", "bruh-botsandmusic", "test-bot", "général de mon propre serveur"]

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

    @commands.command()
    async def top(self, ctx, code_pays):
        global pays
        """shows actual best songs in a country on Spotify"""
        current_channel = ctx.message.channel.id
        channels = ctx.guild.channels
        if checks_in_bot_channel(channels, current_channel) == True:
            if code_pays not in pays:
                await ctx.send("Dsl, mais je ne connais pas le code de ce pays. utilise la commande '$aide' pour voir tout les codes des pays disponibles et leur orthographe exacte.")
            else:
                link_pays = "spotify:user:spotifycharts:playlist:" + pays[code_pays]
                print(link_pays)
                liste_tracks = []
                liste_artists = []
                liste_images = []
                images = ""
                with open('token_spo.txt', 'r') as token_spo:
                    client_credentials_manager = SpotifyClientCredentials(client_id="358a882e0433437896ed0c77a429023b",client_secret=token_spo.read())
                sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

                playlist_id = link_pays
                results = sp.playlist(playlist_id)
                tracks = results['tracks']
                for i, item in enumerate(tracks['items']):
                    track = item['track']
                    liste_tracks.append(track['name'])
                    liste_images.append(track['album']['images'][2]['url'])
                    liste_artists.append(track['artists'][0]['name'])
                emb = discord.Embed(title=None, description = "Top 25 - " + code_pays + " on Spotify", color=0x3498db)
                print(images)
                for i in range(25):
                    field = emb.add_field(name = str(i+1), value = liste_artists[i] + " - " + liste_tracks[i])
                    field.set_thumbnail(url = liste_images[0])
                print(liste_tracks)
                msg = await ctx.send(embed = emb)
        else:
            await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

