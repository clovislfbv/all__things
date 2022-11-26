import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from youtube_dl import *
import asyncio
from random import randint, choice, shuffle
import urllib.parse, urllib.request, re
from time import sleep
from gtts import gTTS
from time import sleep
import top, musicCommands, ban, unban, kick, punch, hug, kiss, coucou, clear, togglebotchannel, edt

bot = commands.Bot(command_prefix="$", description = "Bot créé par Clovis!")
slash = SlashCommand(bot, sync_commands = True)
ytdl = YoutubeDL()
client = discord.Client()
agenda = []
message_skip = 0
message_channel = 0
playing = 0
pays = {"FR" : '37i9dQZEVXbIPWwFssbupI?si=1e836528e2384a70', "UK" : "37i9dQZEVXbLnolsZ8PSNw?si=bcc5a83311b54e67", "USA" : "37i9dQZEVXbLRQDuF5jeBp?si=0b5e105bed784940",  "WORLD" : '37i9dQZEVXbMDoHDwVN2tF?si=510c4902c6ba4d80', "ES" : "37i9dQZEVXbNFJfN1Vw8d9?si=3087bda4c2df4961", "IN" : "37i9dQZEVXbLZ52XmnySJg?si=085b180ae65b4609", "PH" : "37i9dQZEVXbNBz9cRCSFkY?si=b30c3057903f4ef5", "TU" : "37i9dQZEVXbIVYVBNw9D5K?si=3f4a25f140904d2f", "JA" : "37i9dQZEVXbKXQ4mDTEBXq?si=5971ca3ffc744d15", "PB" : "37i9dQZEVXbKCF6dqVpDkS?si=0b8e08dc941e4b47", "IT" : "37i9dQZEVXbIQnj7RRhdSX?si=3d1f7cb768e14959", "RU" : "37i9dQZEVXbL8l7ra5vVdB?si=28dc400fabb8424b"}


def my_hook(d):
    if d['status'] == 'downloading':
        print ("downloading "+ str(round(float(d['downloaded_bytes'])/float(d['total_bytes'])*100,1))+"%")
    if d['status'] == 'finished':
        filename=d['filename']
        print(filename)

ydl_opts = {
    'format': 'bestvideo[width<=1080]+bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'progress_hooks': [my_hook]
}

@bot.event
async def on_connect():
    bot.load_extension("OtherCommands")

@bot.event
async def on_ready():
    print("Ready")
    changeStatus.start()

status = ["$help", "surpasser Bomboclaat Bot", "$aide"]

allowed_channels = [796137851972485151, 697492398070300763, 796731890630787126, 631935311592554636] #["🤖・cow-bip-bop-bots", "bruh-botsandmusic", "test-bot", "général de mon propre serveur"]

def checks_in_bot_channel(channels, channel):
    global allowed_channels
    for i in range(len(allowed_channels)):
        channel_id = allowed_channels[i]
        print(channel_id, channel)
        if channel_id == channel:
            return True
    return False

'''
@bot.event
async def on_command_error(ctx, error):
    # coding: utf-8
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Dsl mon gars, la commande que t'as écrite existe peut être dans tes rêves mais elle n'existe pas dans la réalité")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Dsl mec mais t'as pas les permissions d'utiliser cette commande.")
    elif isinstance(error.original, discord.Forbidden):
        await ctx.send("Dsl mec je peux pas exécuter ta commande pcq les admins ne m'ont pas donner les permissions pour faire cela.")'''

@bot.command()
async def start(ctx, secondes = 5):
	changeStatus.change_interval(seconds = secondes)

@tasks.loop(seconds = 5)
async def changeStatus():
	game = discord.Game(choice(status))
	await bot.change_presence(activity = game)
'''
@bot.command()
@commands.has_permissions(administrator=True)
async def broadcast(ctx):
    for guild in bot.guilds:
        index = 0
        while not isinstance(guild.channels[index], discord.TextChannel):
            index += 1
        await guild.channels[index].send("Au le con j'avais oublié le lien : https://www.instagram.com/p/CjIyZMxsdpN/")
'''
@bot.command()
async def current_time(ctx, contitry):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel):
        hours = ""
        minutes = ""
        secondes = ""
        times = [hours, minutes, secondes]
        tz = pytz.timezone(contitry)
        current_time = datetime.now(tz)
        current_time = current_time.strftime("%H:%M:%S")
        contitry = list(contitry)
        print(contitry)
        while contitry[0] != "/":
            del contitry[0]
        del contitry[0]
        contitry = "".join(contitry)
        print("Current Time =", current_time)
        temps = await ctx.send(f"Il est actuellement {current_time} à {contitry}")
        current_time = list(current_time)
        while current_time[0] != ":":
            hours += current_time[0]
            del current_time[0]
        del current_time[0]
        while current_time[0] != ":":
            minutes += current_time[0]
            del current_time[0]
        del current_time[0]
        for i in range(2):
            print(current_time)
            secondes += current_time[0]
            del current_time[0]
        hours = int(hours)
        minutes = int(minutes)
        secondes = int(secondes)

        tts = gTTS(f"Il est actuellement {hours} heures, {minutes} minutes et {secondes} secondes à {contitry}", lang="fr")
        tts.save('/home/pi/Documents/bot_discord_benjamin/all_things-my-Discord-bot/audio/heure.mp3')
        user = ctx.message.author
        if user.voice is not None:
            channel = ctx.author.voice.channel
            client = await channel.connect()
            client.play(discord.FFmpegPCMAudio('/home/pi/Documents/bot_discord_benjamin/all_things-my-Discord-bot/audio/heure.mp3'))
            ctx.voice_client.source.volume = 1000 / 100
            length = mutagen_length("/home/pi/Documents/bot_discord_benjamin/all_things-my-Discord-bot/audio/heure.mp3")
            sleep(length)
            client = ctx.guild.voice_client
            await client.disconnect()
        else:
            await ctx.send("Stv y a une petite surprise lorsque tu te mets dans un chat vocal et que tu réexécutes cette commande.")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")
        
player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@bot.command()
async def morpion(ctx, p1: discord.Member, p2: discord.Member):
    """ input : @player1 @player2"""
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel):
        print("morpion began")
        global count
        global player1
        global player2
        global turn
        global gameOver

        if gameOver:
            global board
            board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                    ":white_large_square:", ":white_large_square:", ":white_large_square:",
                    ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            turn = ""
            gameOver = False
            count = 0

            player1 = p1
            player2 = p2

            # print the board
            line = ""
            for x in range(len(board)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[x]

            # determine who goes first
            num = random.randint(1, 2)
            if num == 1:
                turn = player1
                await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
            elif num == 2:
                turn = player2
                await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
            await ctx.send("To play you have to write the command $place and then the rank where you want to put your thing from your team")
        else:
            await ctx.send("A game is already in progress! Finish it before starting a new one.")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel):

        if not gameOver:
            mark = ""
            if turn == ctx.author:
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark = ":o2:"
                if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                    board[pos - 1] = mark
                    count += 1

                    # print the board
                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]

                    checkWinner(winningConditions, mark)
                    print(count)
                    if gameOver:
                        await ctx.send(mark + " wins!")
                    elif count >= 9:
                        gameOver = True
                        await ctx.send("It's a tie!")

                    # switch turns
                    if turn == player1:
                        turn = player2
                    elif turn == player2:
                        turn = player1
                else:
                    await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
            else:
                await ctx.send("It is not your turn.")
        else:
            await ctx.send("Please start a new game using the !tictactoe command.")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@morpion.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")

@slash.slash(name="slap", description="donne une claque à un membre du serveur", guild_ids=[631935311592554601], options=[
    create_option(name="member", description="le membre du serveur à qui tu veux donner une claque", option_type=3, required=True)    
])
@bot.command()
async def slap(ctx:SlashContext, member):
    if {ctx.author.mention} == member:
        ctx.send("T'es teubé ou quoi ? Tu peux pas te donner de claques à toi-même ?! Y a que toi pour être si teubé que ça !!")
    else:
        slaps = ["https://i.gifer.com/XaaW.gif", "https://i.gifer.com/2eNz.gif", "https://i.gifer.com/2Dji.gif", "https://i.gifer.com/1Vbb.gif", "https://i.gifer.com/K03.gif", "https://i.gifer.com/DjuN.gif", "https://i.gifer.com/Djw.gif", "https://i.gifer.com/4kpG.gif", "https://i.gifer.com/K02.gif"]
        slappy = slaps[randint(0, len(slaps)-1)]
        emb = discord.Embed(title=None, description = f"{ctx.author.mention} met une claque à {member}", color=0x3498db)
        emb.set_image(url=f"{slappy}")
        await ctx.send( embed = emb)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def nombre_serveurs(ctx):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel):
        counter = 0
        names = ""
        for guild in bot.guilds:
            counter += 1
            names += guild.name
            names += ", "
        await ctx.send(f"Je suis membre dans un total de {counter} serveurs qui se nomment : {names}")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def lettre_random(ctx):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel):
        for i in range(5):
            lettres = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
            lettre_bot = lettres[randint(0, len(lettres))]
            print(lettre_bot)
            await ctx.send("Je pense à une lettre. Essaye de la deviner")

            def check(message):
                return message.author == ctx.message.author and ctx.message.channel == message.channel

            lettre_joueur = await bot.wait_for("message", check = check)
            if lettre_joueur.content == lettre_bot:
                await ctx.send("Bien joué ! Tu as trouvé la lettre à laquelle je pensais")
            else:
                await ctx.send(f"Ta lettre : {lettre_joueur.content} \n Ma lettre : {lettre_bot} \n Dommage ! Tu as perdu !")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

def mutagen_length(path):
    try:
        audio = MP3(path)
        length = audio.info.length
        return length
    except:
        return None

@bot.command()
async def accent(ctx, langue, *, message):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel):
        if langue == "qu":
            tts = gTTS(message, lang="fr", tld="ca")
        else:
            tts = gTTS(message, lang=langue)
        tts.save('Desktop/bot_discord/traduction.mp3')
        user = ctx.message.author
        if user.voice is None:
            return await ctx.send("Not connected to voice channel")

        channel = ctx.author.voice.channel
        client = await channel.connect()
        client.play(discord.FFmpegPCMAudio('Desktop/bot_discord/traduction.mp3'))
        ctx.voice_client.source.volume = 1000 / 100
        length = mutagen_length("C:/Users/gamin/Desktop/bot_discord/traduction.mp3")
        print("duration sec: " + str(length))
        print("duration min: " + str(int(length/60)) + ':' + str(int(length%60)))
        sleep(length)
        client = ctx.guild.voice_client
        await client.disconnect()
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def serverInfo(ctx):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel):
        server = ctx.guild
        numberOfTextChannels = len(server.text_channels)
        numberOfVoiceChannels = len(server.voice_channels)
        serverDescription = server.description
        numberOfPerson = server.member_count
        serverName = server.name
        message = f"Le serveur **{serverName}** contient *{numberOfPerson}* personnes. \n La description du serveur est {serverDescription}. \n Ce serveur possède *{numberOfTextChannels}* salons textuels ainsi que *{numberOfVoiceChannels}* salons vocaux."
        await ctx.send(message)
        await ctx.send("Si tu en as besoin tu peux écrire $aide pour avoir des explication sur toutes les commandes disponible avec ce bot.")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def ping(ctx):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel):
        await ctx.send("Pong !")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def getInfo(ctx, text):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel):
        server = ctx.guild
        numberOfTextChannels = len(server.text_channels)
        numberOfVoiceChannels = len(server.voice_channels)
        serverDescription = server.description
        numberOfPerson = server.member_count
        serverName = server.name
        if text == "memberCount":
            await ctx.send(numberOfPerson)
        elif text == "numberOfChannel":
            await ctx.send(numberOfTextChannels + numberOfVoiceChannels)
        elif text == "name":
            await ctx.send(serverName)
        else:
            await ctx.send("Etrange... Je ne connais pas cela")
        await ctx.send("Si tu en as besoin tu peux écrire $aide pour avoir des explication sur toutes les commandes disponible avec ce bot.")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")


@bot.command()
async def aide(ctx):
    '''get more informations about commands'''
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel):
        commands = "```fix\n$serverInfo```permet de connaître quelques informations sur le serveur \n\n```fix\n$say + nombre de fois + message à dire```permet de faire dire quelque chose au bot fois un nombre (par exemple, input : $say 4 coucou, output : coucou coucou coucou coucou) \n\n```fix\n$getInfo + input```permet d'avoir des infos sur l'input que vous donnez (input possible : memberCount, numberOfChannel, name) \n\n```fix\n$clear + nombre de messages précédents```efface le nombre de message précedent (exemple input : $clear 5 output : effacement des 5 précédents messages)\n\n```fix\n$ping```fait une partie de tennis de table avec moi. \n\n```fix\n$kiss + ping d'un membre du serveur```fait un bisou à la personne que tu mentionnes (l'input doit être sous la forme '$kiss @destinataire') \n\n```fix\n$slap + mention d'un membre du serveur```donne une claque au destinataire, s'écrit sous la même forme que la fonction $kiss \n\n```fix\n$coucou + mention d'un membre du serveur```permet de faire coucou au destinataire, s'écrit sous la même forme que la fonction $kiss \n\n```fix\n$punch + mention d'un membre du serveur```donne un coup de poing au destinataire, s'écrit sous la même forme que la fonction $kiss \n\n```fix\n$play + nom de la musique à jouer```joue une musique choisi par l'utilisateur dans le salon vocal où est l'utilisateur (exemple d'input : $play despacito) \n\n```fix\n$morpion + ping des deux joueurs qui veulent jouer```démarre une partie de morpion (ou tic tac toe en anglais). Pour y jouer il faut mettre en input 2 mentions de 'vraies' personnes et non des bots. De plus, pour pouvoir placer un pion sur le plateau, il faut utiliser la commande $place puis écrire en input le rang où le joueur veut poser son pion. Pour vous aider, voici le plateau avec à la place des cases leur rang pour vous aider à poser vos pions \n    1   2   3   \n   4   5   6   \n   7   8   9   \n\n```fix\n$top + code du pays```donne le top 25 actuel des meilleurs chansons du pays que vous avez indiqué sur Spotify. Voici les pays disponibles et leur code correspondant : (France : FR, Royaume-Uni : UK, Etats-Unis : USA, Monde : WORLD, Espagne : ES, Inde : IN, Philippines : PH , Turquie : TU, Japon : JA, Pays-Bas : PB, Italie : IT, Russie : RU). Je tiens à préciser que d'autres pays vont être ajouter à cette commande dans le futur. \n\n```fix\n$play_music + code classement pays dans $top + rang de la musique voulu```permet de jouer rapidement une musique du classement du pays de votre choix (vous pouvez trouvez les codes des pays disponibles dans l'aide pour la commande $top) en mettant son rang que vous pouvez retrouver grâce à la commande $top. Petite nouveauté sur cette commande : il est possible de jouer toutes les musiques dans un ordre aléatoire du $top du pays de votre choix en écrivant par exemple : $play_music FR all \n\n```fix\n$blague```lorsque vous activer cette commande je vous raconte n'importe quelle blague que je connais en français\n\n```fix\n$joke```lorsque vous écrivez cette commande je vous raconte n'importe quelle blague que je connais en anglais \n\n```fix\n$start_hangman```démarre une partie du jeu du pendu mais svp n'essayez pas cette commande car elle est en développement. Elle risque de faire crache le bot et le server. \n\n```fix\n$nombre_serveurs```donne le nombre de serveur dans lequel je suis et je donne leur nom.```fix\n$accent + code langue + message à dire``` je lis votre message avec l'accent dans la langue de votre choix. les langues disponibles sont : 'af': 'Afrikaans', 'ar': 'Arabic', 'bg': 'Bulgarian', 'bn': 'Bengali', 'bs': 'Bosnian', 'ca': 'Catalan', 'cs': 'Czech', 'cy': 'Welsh', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'eo': 'Esperanto', 'es': 'Spanish', 'et': 'Estonian', 'fi': 'Finnish', 'fr': 'French', 'gu': 'Gujarati', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'hy': 'Armenian', 'id': 'Indonesian', 'is':'Icelandic', 'it': 'Italian', 'ja': 'Japanese', 'jw': 'Javanese', 'km': 'Khmer', 'kn': 'Kannada', 'ko': 'Korean', 'la': 'Latin', 'lv': 'Latvian', 'mk': 'Macedonian', 'ml': 'Malayalam', 'mr': 'Marathi', 'my': 'Myanmar (Burmese)', 'ne': 'Nepali', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'qu': 'Québécois', 'ro': 'Romanian', 'ru': 'Russian', 'si': 'Sinhala', 'sk': 'Slovak', 'sq': 'Albanian', 'sr': 'Serbian', 'su': 'Sundanese', 'sv': 'Swedish', 'sw': 'Swahili', 'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese', 'zh-CN': 'Chinese', 'zh-TW': 'Chinese (Mandarin/Taiwan)', 'zh': 'Chinese (Mandarin)' \n\n```fix\n$current_time + nom du continent en anglais/nom de la capitale en anglais``` donne l'heure actuelle dans la ville écrite en Input."
        liste = list(commands)
        number_of_times = len(liste) // 2000 + 1
        print(number_of_times, len(liste))
        for r in range(number_of_times):
            if len(liste) - 2000 >= 0:
                list_commands = ""
                for i in range(2000):
                    list_commands += liste[0]
                    del liste[0]
                    print(len(liste))
                await ctx.send(list_commands)
            else:
                list_commands = ""
                for i in range(len(liste)):
                    list_commands += liste[0]
                    del liste[0]
                await ctx.send(list_commands)
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

fin = 1
@bot.command()
async def start_hangman(ctx):
    global fin
    liste_mots_cache = ["mathematiques", "programmer", "ordinateur", "clavier", "souris", "python", "arduino", "internet", "creation", "passion", "clovis", "manuel", "anglais", "telephone", "jouer", "joueur","joueuse", "matiere", "bouteille", "calendrier", "reveil", "caserole", "fleurs", "cles", "calculatrice", "calculette", "apple", "batman", "guirlande", "stylo", "trousse", "vampire", "jour", "pont", "guitare", "flute", "violon", "radiateur", "evian", "vittel", "cristaline", "animaux", "photos", "guillaume", "hugo", "eren", "titan", "colossal", "cuirasse", "muraille","chine", "arsene","toilette","fils","tomber","courir", "ecrire", "nuit", "echec", "pendu", "numerique", "science","informatique", "mur", "maria", "rose", "rules of survival", "brawl stars", "fortnite", "hearthstone", "rubik's cube", "rocket league", "wesh", "lampe", "chewing-gum", "boire", "manger", "machouiller", "fete", "livre", "adaptateur", "casque", "pantalon", "chaise"]
    mot_a_trouver = list(liste_mots_cache[randint(0, len(liste_mots_cache))])
    mot_montré = []
    for i in range(len(mot_a_trouver)):
        if mot_a_trouver[i] == " ":
            mot_montré.append(" ")
        elif mot_a_trouver[i] == "'":
            mot_montré.append("'")
        elif mot_a_trouver[i] == "-":
            mot_montré.append("-")
        else:
            mot_montré.append("\\_")
    letters_played = []
    fautes = 0
    variable = 0
    message_channel = ctx.message.channel.id
    channel = discord.utils.get(ctx.guild.channels, name= "jeu-du-pendu")
    channel_id = channel.id
    print(channel_id, message_channel)
    if channel_id == message_channel:
        if fin == 1:
            fin = 0
            await ctx.send(mot_a_trouver)
            mot_montré = " ".join(mot_montré)
            await ctx.send(f"le mot à trouver : {mot_montré}")
            await ctx.send("Ecris une lettre pour deviner le mot")
            mot_montré = "".join(mot_montré)
            print(mot_montré)
            mot_montré = list(mot_montré)
            for l in range(len(mot_montré)-len(mot_a_trouver)):
                if mot_montré[l] == "\\":
                    del mot_montré[l]
            for e in range(len(mot_montré)-(len(mot_a_trouver)-1)):
                if mot_montré[e] == " ":
                    del mot_montré[e]
            print(mot_montré)
        else:
            await ctx.send("Une partie est déjà en cours. Veuillez la terminer pour pouvoir en commencer une nouvelle.")

        def check(message):
            #return message.author == ctx.message.author and ctx.message.channel == message.channel
            return True

        while fin != 1:
            try:
                lettre_du_joueur = await bot.wait_for("message", check = check, timeout = 360)
                lettre_du_joueur = lettre_du_joueur.content

                indexes = []
                print(letters_played)
                if lettre_du_joueur in letters_played:
                    await ctx.send("TU AS DEJA JOUÉ CETTE LETTRE !!!")
                elif lettre_du_joueur in mot_a_trouver:
                    for i in range(len(mot_a_trouver)):
                        if lettre_du_joueur == mot_a_trouver[i]:
                            indexes.append(i)
                    for r in range(len(indexes)):
                        mot_montré[indexes[r]] = lettre_du_joueur
                        variable += 1
                    letters_played.append(lettre_du_joueur)
                else:
                    if fautes != 10:
                        await ctx.send("**Dommage !!** Ce n'était pas la bonne lettre ! Essaye encore !")
                    else:
                        await ctx.send("**Perdu !!** Tu feras mieux la prochaine fois (peut-être) :)")
                    fautes += 1

                if fautes == 1:
                    emb = discord.Embed(title=None, description = "", color=0x3498db)
                    emb.set_image(url="https://cdn.discordapp.com/attachments/631935311592554636/871483571204919386/1.PNG")

                if fautes == 2:
                    emb = discord.Embed(title=None, description = "", color=0x3498db)
                    emb.set_image(url="https://cdn.discordapp.com/attachments/631935311592554636/871484660058841088/2.PNG")

                if fautes == 3:
                    emb = discord.Embed(title=None, description = "", color=0x3498db)
                    emb.set_image(url="https://cdn.discordapp.com/attachments/631935311592554636/871483577559285821/3.PNG")

                if fautes == 4:
                    emb = discord.Embed(title=None, description = "", color=0x3498db)
                    emb.set_image(url="https://cdn.discordapp.com/attachments/631935311592554636/871483579006349372/4.PNG")

                if fautes == 5:
                    emb = discord.Embed(title=None, description = "", color=0x3498db)
                    emb.set_image(url="https://cdn.discordapp.com/attachments/631935311592554636/871483580293988352/5.PNG")

                if fautes == 6:
                    emb = discord.Embed(title=None, description = "", color=0x3498db)
                    emb.set_image(url="https://cdn.discordapp.com/attachments/631935311592554636/871483581929779291/6.PNG")

                if fautes == 7:
                    emb = discord.Embed(title=None, description = "", color=0x3498db)
                    emb.set_image(url="https://cdn.discordapp.com/attachments/631935311592554636/871483583485849700/7.PNG")

                if fautes == 8:
                    emb = discord.Embed(title=None, description = "", color=0x3498db)
                    emb.set_image(url="https://cdn.discordapp.com/attachments/631935311592554636/871483584932900874/8.PNG")

                if fautes == 9:
                    emb = discord.Embed(title=None, description = "", color=0x3498db)
                    emb.set_image(url="https://cdn.discordapp.com/attachments/631935311592554636/871483586283446373/9.PNG")

                if fautes == 10:
                    emb = discord.Embed(title=None, description = "", color=0x3498db)
                    emb.set_image(url="https://cdn.discordapp.com/attachments/631935311592554636/871483590268055562/10.PNG")

                if fautes != 0:
                    await ctx.send( embed = emb)

                if mot_montré == mot_a_trouver:
                    fin += 1
                    mot_montré = " ".join(mot_montré)
                    await ctx.send(mot_montré)
                    await ctx.send("Bravo, tu as trouvé le mot caché !!")
                    mot_a_trouver = list(liste_mots_cache[randint(0, len(liste_mots_cache))])
                    mot_montré = []
                    for i in range(len(mot_a_trouver)):
                        if mot_a_trouver[i] == " ":
                            mot_montré.append(" ")
                        elif mot_a_trouver[i] == "'":
                            mot_montré.append("'")
                        elif mot_a_trouver[i] == "-":
                            mot_montré.append("-")
                        else:
                            mot_montré.append("\\_")
                    letters_played = []
                    fautes = 0
                    sol = "  \\_ \\_ \\_ \\_ \\_    "
                    tiret_haut1 = "     |       "
                    tiret_haut2 = "     |       "
                    tiret_haut3 = "     |       "
                    tiret_haut4 = "     |       "
                    tiret_haut5 = "     |       "
                    haut = ["    "]
                    for i in range(6):
                        haut.append("\\_ ")
                    haut = "".join(haut)
                    variable = 0
                elif fautes == 10:
                    fin += 1
                    await ctx.send("Malheureusement, tu n'as pas trouvé le mot caché !! Le mot à trouver était :", "".join(mot_a_trouver))
                    mot_a_trouver = list(liste_mots_cache[randint(0, len(liste_mots_cache))])
                    mot_montré = []
                    for i in range(len(mot_a_trouver)):
                        if mot_a_trouver[i] == " ":
                            mot_montré.append(" ")
                        elif mot_a_trouver[i] == "'":
                            mot_montré.append("'")
                        elif mot_a_trouver[i] == "-":
                            mot_montré.append("-")
                        else:
                            mot_montré.append("\\_")
                    letters_played = []
                    fautes = 0
                    for i in range(6):
                        haut.append("\\_ ")
                    haut = "".join(haut)
                    variable = 0
                else:
                    for z in range(len(mot_montré)):
                        if mot_montré[z] == "_":
                            mot_montré[z] = "\\_"
                    mot_montré = " ".join(mot_montré)
                    await ctx.send(f"le mot à trouver : {mot_montré}")
                    await ctx.send("Ecris une lettre pour deviner le mot ")
                    mot_montré = "".join(mot_montré)
                    print(mot_montré)
                    mot_montré = list(mot_montré)
                    for l in range(len(mot_montré)-(len(mot_a_trouver) - variable)):
                        if mot_montré[l] == "\\":
                            del mot_montré[l]
                    for e in range(len(mot_montré)-(len(mot_a_trouver) - variable)):
                        if mot_montré[e] == " ":
                            del mot_montré[e]
                    print(mot_montré)
            except:
                await ctx.send("**Ta partie de hangman a été annulé car tu as mis trop de temps à répondre.**")
                fin = 1
                break
    else:
        await ctx.send("Tu n'est pas sur le bon channel. Pour jouer à ce jeu, il faut te rendre sur le channel 'jeu-du-pendu' du serveur Las Vacas Aerodinamicas ou alors contacter mon créateur pour plus d'infos.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def end_hangman(ctx):
    global fin
    fin = 1
    await ctx.send("La partie de pendu a été terminé manuellement. Tu peux en redémarrer une nouvelle avec la commande $start_hangman.")

bot.add_cog(top.AudioCommands(bot))
bot.add_cog(musicCommands.AudioCommands(bot))
bot.add_cog(ban.AdminCommands(bot))
bot.add_cog(unban.AdminCommands(bot))
bot.add_cog(kick.AdminCommands(bot))
bot.add_cog(punch.GifCommands(bot))
bot.add_cog(hug.GifCommands(bot))
bot.add_cog(kiss.GifCommands(bot))
bot.add_cog(coucou.GifCommands(bot))
bot.add_cog(togglebotchannel.AdminCommands(bot))
bot.add_cog(clear.AdminCommands(bot))
bot.add_cog(edt.ClassCommands(bot))

with open('token_bot.txt', 'r') as token:
    bot.run(token.read())
