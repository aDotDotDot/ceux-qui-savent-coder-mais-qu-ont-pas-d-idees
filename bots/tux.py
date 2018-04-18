import discord
import asyncio
import time
from calendar import timegm
from datetime import date
import random
from traceback import format_exc
from re import search
from urllib.request import urlopen, Request
from urllib.parse import quote_plus
import json
from html import unescape
from os import popen
from sys import exit
import feedparser
import codecs
import speedtest
from unicodedata import name

fast = """```  ______        _   
 |  ____|      | |  
 | |__ __ _ ___| |_ 
 |  __/ _` / __| __|
 | | | (_| \__ \ |_ 
 |_|  \__,_|___/\__|```
 """

aide_fast = fast +  u"""**Fast** est un jeu où vous devez retaper la chaîne de caractères choisie par le bot le plus rapidement possible. Faites `!fast <niveau>` pour déclancher le début du jeu.
__Niveau **1**__ : 10 à 20 caractères minuscules
__Niveau **2**__ : 10 à 20 caractères minuscules ou majuscules
__Niveau **3**__ : 10 à 20 caractères minuscules (avec ou sans accent), majuscules ou numériques
__Niveau **4**__ : 10 à 20 caractères minuscules (avec ou sans accent), majuscules, numériques ou spéciaux
__Niveau **5**__ : 20 à 30 caractères minuscules (avec ou sans accent), majuscules, numériques ou spéciaux
Bon courage \N{SMILING FACE WITH HORNS}"""

commandes = {"blague": "`!blague` pour avoir une blague au hasard parmis celles que je connais et `!blague add <Votre blague.>` pour m'en apprendre une nouvelle (mettre un `|` pour que je fasse une pause au moment de raconter votre blague)",
             "chr": "`!chr <code>` je renvois le caractère correspondant au code Unicode donné (au format décimal)",
             "citation": "`!citation` pour avoir une citation au hasard parmis celles que je connais et `!citation add <Votre citation.>` pour m'en apprendre une nouvelle",
             "crypto": "`!crypto <nom>` pour avoir des infos sur l'état actuel de la crypto monnaie",
             "date": "la date d'aujourd'hui, tout simplement ^^",
             "devine": "un super jeu ! (je choisis un nombre entre 0 et 100 et tu dois le deviner)",
             "fast": aide_fast,
             "gif": "`!gif <recherche>` pour chercher un GIF (une recherche vide donne un GIF aléatoire)",
             "gps": "`!gps <latitude,longitude>` pour avoir les trois mots what3words et l'adresse correspondant aux coordonnées. Exemple : `!gps 49.192149,-0.306415`.",
             "help": "la liste des commandes (`!help <comande>` pour avoir toutes les infos sur une commande)",
             "heure": "l'heure, tout simplement ^^",
             "lmgtfy": "Let Me Google That For You, je fais une recherche sur Internet pour toi",
             "loc": "Lines Of Code : je te dis combien de lignes comporte actuellement mon programme Python",
             "weather": "`!weather <ville> <jours>` pour avoir les prévisions météo de la ville pendant un certain nombre de jour (un nombre entre 1 et 7)",
             "ping": "tester la vitesse connection avec le bot",
             "proverbe": "`!proverbe` pour avoir un proverbe au hasard parmis ceux que je connais et `!proverbe add <Votre proverbe.>` pour m'en apprendre un nouveau",
             "r2d": "`!r2d <nombre en chiffres romains>` pour convertir un nombre en chiffres romains en un nombre en chiffres décimaux",
             "role": "`!role <list|add|remove> [rôle1] [rôle2] [rôle3] ...` pour vous ajouter, supprimer ou lister tous les rôles disponibles",
             "roll": "un nombre (pseudo-)aléatoire entre 0 et 100",
             "rot13": "`!rot13 <texte>` pour chiffrer/déchiffrer un message en rot13",
             "speedtest": "je me la pète un peu avec ma conexion de taré ^^",
             "vps": "quelques infos sur le VPS qui m'héberge",
             "rug": "Random User Generator, une identité aléatoire",
             "ud": "`!ud <mot>` pour chercher la définition d'un mot sur Urban Dictionnary (en anglais)",
             "unicode": "`!unicode <c>` où c est n'importe quel caractère pour avoir le nom et le code Unicode de ce caractère",
             "user": "`!user @mention` quelques infos sur la personne",
             "w3w": "`!w3w <mot1.mot2.mot3> [langue]` pour avoir les coordonnées GPS et l'adresse d'un lieu à partir des ses trois mots what3words. La langue est le code ISO 639-1 de deux lettres coorespondant. Ce paramètre est facultatif si les mots sont français. Plus d'infos sur https://what3words.com/fr/a-propos/",
             "whois": "`!whois <nom de domaine>` pour avoir queqlues infos sur un nom de domaine",
             "wiki": "`!wiki <recherche>` pour effectuer une recherche sur Wikipédia et avoir la première phrase de l'article"}

caracteres = ['abcdefghijklmnopqrstuvwxyz',
              'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
              'ABCDEFGHIJKLMNOPQRSTUVWXYZaàbcçdeêëéèfghijklmnopqrstuùvwxyz0123456789',
              'ABCDEFGHIJKLMNOPQRSTUVWXYZaàbcçdeêëéèfghijklmnopqrstuùvwxyz0123456789&"#\'{([-|_\\)]°+=}$*?,.;/:!']

feeds = ["https://korben.info/feed",
         "https://www.begeek.fr/feed",
         "http://blogmotion.fr/feed",
         "http://www.framboise314.fr/feed/", "http://www.journaldugeek.com/feed/",
         "https://thehackernews.com/feeds/posts/default",
         "https://usbeketrica.com/rss",
         "https://www.lemondeinformatique.fr/flux-rss/",
         "http://www.01net.com/rss/actualites/"]

with open("wordlist/courants.txt", "r") as f : mots = f.read().split("\n")
with open("secret.json", "r") as f : secret = json.loads(f.read())

pendu = ["""```
                       
                        
                        
                         
                          
                          
                         
                        
         
        ============```""", """```
            
           ||          
           ||          
           ||          
           ||         
           ||         
           ||
           ||
           ||
        ============```""",
          """```
            ============
           ||        
           ||        
           ||       
           ||       
           ||        
           ||
           ||
           ||
        ============```""",
          """```
            ============
           ||  /      
           || /       
           ||/       
           ||       
           ||       
           ||
           ||
           ||
        ============```""",
          """```
            ============
           ||  /      |
           || /       |
           ||/        
           ||        
           ||        
           ||
           ||
           ||
        ============```""",
          """```
            ============
           ||  /      |
           || /       |
           ||/        O
           ||         |
           ||        
           ||
           ||
           ||
        ============```""",
          """```
            ============
           ||  /      |
           || /       |
           ||/        O/
           ||         |
           ||        
           ||
           ||
           ||
        ============```""",
          r"""```
            ============
           ||  /      |
           || /       |
           ||/       \O/
           ||         |
           ||        
           ||
           ||
           ||
        ============```""",
          r"""```
            ============
           ||  /      |
           || /       |
           ||/       \O/
           ||         |
           ||          \
           ||
           ||
           ||
        ============```""",
          r"""```
            ============
           ||  /      |
           || /       |
           ||/       \O/
           ||         |
           ||        / \
           ||
           ||
           ||
        ============```"""]


          

chaine, nbr, coups, ancienmsg, PartieP, mot, aff, vies = {},{},{},{},{},{},{},{}
tmp = log = None

def getUrl(url) :
    req = Request(url, headers={'User-Agent': "Je n'suis pas un robot (enfin si mais un gentil ^^) !"})
    result = urlopen(req)
    result = unescape(result.read().decode("utf-8"))
    return json.loads(result)

try :
    """
    async def actu():
        await client.wait_until_ready()
        channel = discord.Object(id='420635603592413185')
        while not client.is_closed:
            dernier = time.time()
            await asyncio.sleep(10*60) # 10 minutes
            for feed in feeds :
                rss = feedparser.parse(feed)
                for i in rss['entries'] :
                    if timegm(i['published_parsed']) > dernier :
                        await client.send_message(channel, i['link'])
    """        
    client = discord.Client()
            
    @client.event
    async def on_ready():
        try :
            global log, ribt
            log = time.strftime("log/%Y%m%d", time.localtime())
            with open(log,"a") as f : f.write(time.strftime('\n\n***[%H:%M:%S]', time.localtime()) + ' Connecté en tant que ' + client.user.name + ' (id : ' + client.user.id + ')\n')
            await client.change_presence(game=discord.Game(name='jouer avec vous'))
            ribt = await client.get_user_info("321675705010225162")
            await client.start_private_message(ribt)
            await client.send_message(ribt, 'OK')
        except:
            txt = time.strftime('[%d/%m/%Y %H:%M:%S]\n', time.localtime()) + format_exc() + "\n\n"
            with open("log/erreurs.txt","a") as f : f.write(txt)


    @client.event
    async def on_message(message):
        try:
            if message.author == client.user : return
            
            if message.server == None :
                if message.content == "!reboot" and message.author == ribt :
                    with open("log/erreurs.txt","a") as f : f.write(time.strftime('[%d/%m/%Y %H:%M:%S]') + "Tux va tenter de redemarrer sur demande de ribt\n")
                    cmd = popen("python3 tux.py &")
                    exit()
                else : await client.send_message(message.author, 'Je ne répond pas au MP désolé \N{HEAVY BLACK HEART}')
                return

            
            global log, tmp, ancienmsg, loader, chaine, nbr, coups, vies, mot, aff
            #print (message.content)
            t = timegm(message.timestamp.timetuple())
            msg = message.content
            serv = message.server.id
            txt = time.strftime('\n[%H:%M:%S] #', time.localtime(t)) + str(message.channel) + ' ' + str(message.author) + ' : ' + msg
            if log != time.strftime("log/%Y%m%d", time.localtime()): log = time.strftime("log/%Y%m%d", time.localtime())
            with open(log,"a") as f : f.write(txt)

            if message.author.top_role.name == "VilainPasBeau" :
                await client.delete_message(message)
                await client.send_message(message.author, 'Chut !')

            else :
                if search(r"(?i)^ah?\W*$", msg) :
                    await client.send_message(message.channel, 'tchoum')

                if search(r"(?i)^[kq]u?oi?\W*$", msg) :
                    await client.send_message(message.channel, 'ffeur')

                elif search(r"(?i)^lol\W*$", msg) :
                    await client.send_message(message.channel, 'ita')
                
                if msg == "" : pass

                elif msg == '!ping':
                    tmp = time.time() * 1000 - t * 1000
                    await client.send_message(message.channel, 'Pong ! ('+str(round(tmp,1))+' ms)')

                elif (msg == "Recherche d'un GIF..." or msg == "Recherche du meilleur serveur...") and message.author.id == client.user.id :
                    loader = message

                elif msg == '!help':
                    txt = "__Liste des commandes disponibles :__\n\n(faire `!help <commande>` pour avoir toutes les infos sur une comande)\n\n"
                    for commande in commandes.keys() : txt += "- `!" + commande + "`\n"
                    txt += "\n**Cette liste est en constante évoluton : n'hésitez pas à revenir la consulter régulièrement !**"
                    if message.channel.name == "spam-bot" : await client.send_message(message.channel, txt)
                    else :
                        await client.send_message(message.author, txt)
                        await client.send_message(message.channel, "Check tes MP " + "<@" + message.author.id + "> \N{WINKING FACE}")

                elif msg.startswith("!help ") :
                    commande = msg[6:]
                    if commande in commandes :
                        embed = discord.Embed(title="Description de la commande !" + commande + " :", description=commandes[commande], color=0x00ff00)
                        await client.send_message(message.channel, embed=embed)
                    else :
                        await client.send_message(message.channel, "Elle existe pas cette commande là ^^")

                elif msg == '!roll' :
                    await client.send_message(message.channel, str(random.randint(0, 100)))

                elif msg == '!heure' :
                    await client.send_message(message.channel, time.strftime('Il est %H:%M passé de %S secondes.', time.localtime()))

                elif msg == '!date':
                    await client.send_message(message.channel, time.strftime('Nous sommes le %d/%m/%Y.', time.localtime()))

                elif msg == '!blague':
                    f = open("blagues.txt", "r")
                    c = f.read().split('\n')
                    f.close()
                    blague = random.choice(c).split('|')
                    while blague == [""] or blague == tmp : blague = random.choice(c).split('|')
                    tmp = blague
                    for txt in blague :
                        await client.send_message(message.channel, txt)
                        time.sleep(2)               

                elif msg.startswith('!blague add '):
                    blague = msg.replace('!blague add ', '')
                    f = open("blagues.txt", "r")
                    c = f.read().split('\n')
                    f.close()
                    if blague in c : await client.send_message(message.channel, message.author.mention + ' Je connais déjà cette blague.')
                    else :
                        f = open("blagues.txt", "a")
                        f.write('\n' + blague)
                        f.close()
                        await client.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")

                elif msg == '!proverbe':
                    f = open("proverbes.txt", "r")
                    c = f.read().split('\n')
                    f.close()
                    proverbe = random.choice(c)
                    while proverbe == "" or proverbe == tmp : proverbe = random.choice(c)
                    tmp = proverbe
                    await client.send_message(message.channel, proverbe)

                elif msg.startswith('!proverbe add '):
                    proverbe = msg.replace('!proverbe add ', '')
                    f = open("proverbes.txt", "r")
                    c = f.read().split('\n')
                    f.close()
                    if proverbe in c : await client.send_message(message.channel, message.author.mention + ' Je connais déjà ce proverbe.')
                    else :
                        f = open("proverbes.txt", "a")
                        f.write('\n' + proverbe)
                        f.close()
                        await client.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")

                elif msg == '!citation':
                    f = open("citations.txt", "r")
                    c = f.read().split('\n')
                    f.close()
                    citation = random.choice(c)
                    while citation == "" or citation == tmp : citation = random.choice(c)
                    tmp = citation
                    await client.send_message(message.channel, citation)

                elif msg.startswith('!citation add '):
                    citation = msg.replace('!citation add ', '')
                    f = open("citations.txt", "r")
                    c = f.read().split('\n')
                    f.close()
                    if citation in c : await client.send_message(message.channel, message.author.mention + ' Je connais déjà cette citation.')
                    else :
                        f = open("citations.txt", "a")
                        f.write('\n' + citation)
                        f.close()
                        await client.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")

                elif  msg.startswith('!wiki'):
                    args = msg.split(" ")
                    if len(args) < 2 : await client.send_message(message.channel, "Usage : `!wiki <recherche>`.")
                    else :
                        req = quote_plus(" ".join(args[1:]))
                        resultat = getUrl("https://fr.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exsentences=2&explaintext&exintro&redirects=true&titles=" + req)["query"]["pages"]
                        id = list(resultat)[0]
                        titre = resultat[id]["title"]
                        if id == "-1" :
                            resultat = getUrl("https://fr.wikipedia.org/w/api.php?action=opensearch&limit=1&format=json&search=" + req)
                            if resultat[2] != [] and resultat[2][0] != "" :
                                e = discord.Embed(description=resultat[2][0], color=0x00ff00)
                                titre = quote_plus(resultat[1][0])
                                image = getUrl("https://fr.wikipedia.org/w/api.php?action=query&prop=pageimages&pithumbsize=250&format=json&titles=" + titre)["query"]["pages"]
                                id = list(image)[0]
                                if "thumbnail" in image[id] : e.set_image(url=image[id]["thumbnail"]["source"])
                                await client.send_message(message.channel, embed=e)
                            else : await client.send_message(message.channel, "Auncun résultat pour cette recherche...")
                        else :
                            e = discord.Embed(description=resultat[id]["extract"], color=0x00ff00)
                            image = getUrl("https://fr.wikipedia.org/w/api.php?action=query&prop=pageimages&pithumbsize=250&format=json&titles=" + req)["query"]["pages"]
                            id = list(image)[0]
                            if "thumbnail" in image[id] : e.set_image(url=image[id]["thumbnail"]["source"])
                            await client.send_message(message.channel, embed=e)                  
                            
                        
                elif msg.startswith('!fast'):
                    if serv in chaine :
                        tmp = ""
                        for i in chaine[serv] : tmp += i + " "
                        await client.send_message(message.channel, "Une partie est déja en cours avec la chaîne `" + tmp[:-1] + "`...")
                    elif len(msg) != 7 :
                        await client.send_message(message.channel, "Usage : `!fast <niveau>`. Faire `!help fast`pour plus de détails.")
                    else :
                        try : niveau = int(msg[6])
                        except ValueError: await client.send_message(message.channel, "Usage : `!fast <niveau>`. Faire `!help fast`pour plus de détails.")
                        else :
                            if not(1 <= niveau <= 5) : await client.send_message(message.channel, "Usage : `!fast <niveau>`. Faire `!help fast`pour plus de détails.")
                            else :             
                                chaine[serv] = ''
                                if niveau == 5:
                                    choix = caracteres[3]
                                    l = random.randint(20, 30)
                                else :
                                    choix = caracteres[niveau - 1]
                                    l = random.randint(10, 20)
                                i = 0
                                while i < l:
                                    chaine[serv] += random.choice(choix)
                                    i += 1
                                tmp = ""
                                for i in chaine[serv] : tmp += i + " "
                                await client.send_message(message.channel, fast + "Chaine à recopier : " + tmp[:-1] + "\n\n Les espaces c'est juste pour éviter le copier-coller ;-)")
                elif serv in chaine and msg == chaine[serv] :
                    del(chaine[serv])
                    await client.send_message(message.channel, 'Gagné ' + message.author.mention + ' !!!')

                elif msg.startswith('!r2d') :
                    if len(msg) < 6: await client.send_message(message.channel, "Usage : `!r2d <nombre en chiffres romains>`.")
                    else :
                        r = msg.replace('!r2d ', '')
                        r = r.replace(' ', '').upper()
                        dico = {"I":1, "V":5, "X":10, "L":50, "C":100, "D":500, "M":1000}
                        d = 0
                        erreur = False
                        i = 0
                        while i < len(r):
                            if not(r[i] in dico) :
                                erreur = True
                                break
                            if i == len(r) - 1:
                                d += dico[r[i]]
                            else :
                                if dico[r[i]] < dico[r[i + 1]] :
                                    d -= dico[r[i]]
                                else :
                                    d += dico[r[i]]
                            i += 1
                        if erreur :
                            await client.send_message(message.channel, "Le nombre entré n'est pas correct.")
                        else : await client.send_message(message.channel, str(d))


                elif msg == "!cnf" :
                    fact = getUrl("https://www.chucknorrisfacts.fr/api/get?data=tri:alea;nb:1")[0]['fact']
                    await client.send_message(message.channel, fact)

                elif msg == "!ud" : await client.send_message(message.channel, "Usage : `!ud <mot>` (`!help ud` pour plus de détails)")

                elif msg.startswith("!ud ") :
                    url = msg.replace("!ud ", "http://api.urbandictionary.com/v0/define?term=")
                    definition = getUrl(url)
                    if definition['result_type'] == 'no_results' : await client.send_message(message.channel, 'Aucun résultat...')
                    else : await client.send_message(message.channel, definition['list'][0]['definition'])

                elif msg == "!rug" :
                    data = getUrl("https://randomuser.me/api/?nat=fr")['results'][0]
                    txt = ""
                    txt += "Tu t'appelles " + data['name']['first'].capitalize() + " " + data['name']['last'].capitalize() + ". "
                    txt += "Ton adresse mail est " + data['email'].replace("example.com", random.choice(["gmail.com","yahoo.com","neuf.fr","laposte.net","orange.fr","ovh.net",])) + ". "
                    jour, heure = data['dob'].split(" ")
                    jour = jour.split("-")
                    jour = jour[2] + "/" + jour[1] + "/" + jour[0]
                    txt += "Tu es né le " + jour + " à " + heure + ". "
                    txt += "Ton numéro de téléphone est le " + data['phone'].replace("-", " ") + ". "
                    loc = data['location']
                    txt += "Tu habites au " + loc['street'] + " à " + loc['city'].title() + ". "
                    txt += "Ton pseudo est " + data['login']['username'] + " et ton mot de passe est `" + data['login']['password'] + "`."
                    await client.send_message(message.channel, txt)

                elif msg == "!vps" :
                    txt = ""
                    txt += "freespace=" + popen("df -h /").read().split("\n")[1].split()[3] + "\n"
                    txt += "host=" + popen("hostname --fqdn").read()
                    await client.send_message(message.channel, txt)

                elif msg.startswith("!gif") :            
                    if len(msg) == 4 :
                        loader = await client.send_message(message.channel, "Recherche d'un GIF...")
                        url = "http://api.giphy.com/v1/gifs/random?api_key=" + secret["giphy-key"]
                        gif = getUrl(url)['data']
                        await client.edit_message(loader, "Téléchargement du GIF...")
                        with open("/home/ribt/python/discord/tmp.gif", "wb") as f : f.write(urlopen(gif['image_url']).read())
                        await client.edit_message(loader, "Upload du GIF...")
                        await client.send_file(message.channel, "tmp.gif", filename="random.gif")
                        await client.delete_message(loader)
                    
                    else :
                        loader = await client.send_message(message.channel, "Recherche d'un GIF...")
                        req = msg[5:]
                        url = "http://api.giphy.com/v1/gifs/search?api_key="+ secret["giphy-key"] + "&lang=fr&limit=1&q=" + req
                        gif = getUrl(url)['data'][0]
                        await client.edit_message(loader, "Téléchargement du GIF...")
                        with open("/home/ribt/python/discord/tmp.gif", "wb") as f : f.write(urlopen(gif['images']['original']['url']).read())
                        await client.edit_message(loader, "Upload du GIF...")
                        await client.send_file(message.channel, "tmp.gif", filename=gif['title'].replace(" ", "_")+".gif")
                        await client.delete_message(loader)

                elif msg == "!devine" :
                    if message.channel.name != "spam-bot" :
                        await client.send_message(message.channel, "On va pas jouer ici alors qu'il y'a un salon qui s'appelle spam-bot !")
                    else :
                        if serv in nbr :
                            await client.send_message(message.channel, "Une partie est déja en cours...")
                        else :
                            coups[serv] = {}
                            nbr[serv] = random.randint(0, 100)
                            await client.send_message(message.channel, "C'est parti mon kiki !")
                elif serv in nbr and message.channel.name == "spam-bot" :
                    try : proposition = int(msg)
                    except ValueError : pass
                    else :
                        if message.author.id in coups[serv] : coups[serv][message.author.id] += 1
                        else : coups[serv][message.author.id] = 1
                        if proposition == nbr[serv] :
                            del(nbr[serv])
                            await client.send_message(message.channel, 'Gagné en ' + str(coups[serv][message.author.id]) + ' coups ' + message.author.mention + ' !')
                        elif nbr[serv] < proposition :
                            await client.send_message(message.channel, "C'est moins que " + str(proposition))
                        else :
                            await client.send_message(message.channel, "C'est plus que " + str(proposition))

                elif msg.startswith("!weather") :
                    try :
                        ville, jours = msg.replace("!weather ", "").split(" ")
                        jours = int(jours)
                    except ValueError :
                        await client.send_message(message.channel, "Usage : !weather <ville> <jours>")
                    else :
                        if not(1 <= jours <= 7) : await client.send_message(message.channel, "<jours> doit être un nombre entre 1 et 7")
                        else :
                            try : data = feedparser.parse("http://api.meteorologic.net/forecarss?p=" + ville)['entries'][0]['summary']
                            except IndexError : await client.send_message(message.channel, "Pas de données météo pour cette ville...")
                            else :
                                if data == "" : await client.send_message(message.channel, "Pas de données météo pour cette ville...")
                                else :
                                    data = data.replace("<strong>", "").replace("</strong>", "").replace("\t", "").replace("<br />", "\n")
                                    data = data.split("\n\n\n")[:-1]
                                    data[0] = "\n" + data[0]
                                    i = 0
                                    while i < len(data) and i < jours :
                                        data[i] = data[i].split("\n")[1:-1]
                                        data[i][0] = "__" + data[i][0][:-1] + "__"
                                        await client.send_message(message.channel, "\n".join(data[i]))
                                        i += 1

                elif msg.startswith("!rot13 ") :
                    await client.send_message(message.channel, codecs.encode(msg[7:], 'rot_13'))

                elif msg == "!whois" : await client.send_message(message.channel, "Usage : `!whois <nom de domaine>` (`!help whois` pour plus de détails)")

                elif msg.startswith("!whois ") :
                    dn = msg[7:]
                    url = "https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey=" + secret["whois-key"] + "&outputFormat=JSON&domainName=" + dn
                    try : data = getUrl(url)['WhoisRecord']['registryData']['administrativeContact']['rawText'].split("\n")
                    except KeyError : await client.send_message(message.channel, 'nom de domaine inconnu...')
                    else :
                        txt = tmp = ""
                        i = 0
                        while len(tmp) <= 400 and i < len(data):
                            txt = tmp
                            tmp += data[i] + "\n"
                            i += 1
                        await client.send_message(message.channel, txt)

                elif msg == "!pi" : await client.send_message(message.channel, "3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823378678316527120190914564856692346034861045432664821339360726024914127372458700660631558817488152092096282925409171536436789259036001133053054882046652138414695194151160")

                elif msg == "!pendu" :
                    if message.channel.name != "spam-bot" :
                        await client.send_message(message.channel, "On va quand même pas jouer ici alors qu'il y'a un salon qui s'appelle spam-bot !")
                    else :
                        if serv in mot : await client.send_message(message.channel, "Une partie est déjà en cours (" + aff[serv] + ")...")
                        else :
                            vies[serv] = len(pendu)
                            mot[serv] = random.choice(mots)
                            aff[serv] = ["_"]*len(mot[serv])
                            await client.send_message(message.channel, "C'est parti ! (N'oubliez pas que je compte les accents et les cédilles ^_^)")
                            await client.send_message(message.channel, " ".join(aff[serv]).replace("_", r"\_"))
                            
                elif message.channel.name == "spam-bot" and serv in mot and len(msg) == 1:
                    lettre = msg.lower()
                    if lettre in mot[serv] :
                        i = 0
                        while i < len(mot[serv]) :
                            if mot[serv][i] == lettre : aff[serv][i] = lettre
                            i += 1
                        if not "_" in aff[serv] :
                            del(mot[serv])
                            await client.send_message(message.channel, "Gagné ^^")
                    else :
                        await client.send_message(message.channel, pendu[-vies[serv]])
                        vies[serv] -= 1
                        if vies[serv] == 0 :
                            await client.send_message(message.channel, "PERDU !!! (le mot était... " + mot[serv] + " !)")
                            del(mot[serv])
                    
                    if serv in mot : await client.send_message(message.channel, " ".join(aff[serv]).replace("_", r"\_"))
                
                elif msg.startswith("!role") :
                    args = msg.split(" ")
                    if len(args) < 2 : await client.send_message(message.channel, "Usage : `!role <list|add|remove> [rôle]` (`!help role` pour plus de détails)")
                    elif args[1] == "list" :
                        txt = "__Liste des rôles disponibles :__\n\n"
                        for i in message.server.roles :
                            if str(i.colour) == "#ffffff" : txt += "- **" + i.name + "**\n"
                        txt += "\n(Vous pouvez proposer de nouveaux rôles proposer dans " + discord.utils.get(message.server.channels, name='suggestions').mention + " \N{WINKING FACE})"
                        await client.send_message(message.channel, txt)
                    elif len(args) < 3 : await client.send_message(message.channel, "Usage : `!role <list|add|remove> [rôle]` (`!help role` pour plus de détails)")
   
                    elif args[1] == "add" :
                        for arg in args[2:] :
                            role = None
                            for i in message.server.roles :
                                if i.name.lower() == arg.lower() : role = i
                            if role == None : await client.send_message(message.channel, "Le rôle *" + arg + "* n'existe pas encore mais vous pouvez le proposer dans " + discord.utils.get(message.server.channels, name='suggestions').mention + " \N{WINKING FACE}")
                            elif str(role.colour) != "#ffffff" : await client.send_message(message.channel, "Le rôle *" + arg + "*, t'as pas le droit de le prendre \N{WINKING FACE}")
                            else :
                                await client.add_roles(message.author, role)
                                await client.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")

                    elif args[1] == "remove" :
                        for arg in args[2:] :
                            role = None
                            for i in message.author.roles :
                                if i.name.lower() == arg.lower() : role = i
                            if role == None : await client.send_message(message.channel, "Tu n'as pas le rôle *" + arg + "*...")
                            else :
                                await client.remove_roles(message.author, role)
                                await client.add_reaction(message, u"\N{WHITE HEAVY CHECK MARK}")

                    else : await client.send_message(message.channel, "Usage : `!role <list|add|remove> [rôle]` (`!help role` pour plus de détails)")

                elif msg.startswith("!w3w"):
                    args = msg.split(" ")
                    if len(args) < 2 or len(args) > 3 : await client.send_message(message.channel, "Usage : `!w3w <mot1.mot2.mot3> [langue]` (`!help w3w` pour plus de détails)")
                    else :
                        url = "https://api.what3words.com/v2/forward?addr=" + quote_plus(args[1]) + "&key=" + secret["w3w-key"] + "&format=json&display=minimal"
                        if len(args) == 3 and args[2].lower() != "fr" : url += "&lang=" + quote_plus(args[2].lower())
                        else : url += "&lang=fr"
                        gps = getUrl(url)['geometry']
                        if gps == None : await client.send_message(message.channel, "Aucun résultat avec ces trois mots...")
                        else :
                            lat = str(gps['lat'])
                            lng = str(gps['lng'])
                            await client.send_message(message.channel, "coordonées GPS : " + lat + "," + lng)
                            url = "https://services.gisgraphy.com/reversegeocoding/search?format=json&lat=" + lat + "&lng=" + lng
                            adresse = getUrl(url)['result'][0]
                            await client.send_message(message.channel, "adresse complète : " + adresse['formatedFull'])

                elif msg.startswith("!gps"):
                    args = msg.split(" ")
                    if len(args) != 2 : await client.send_message(message.channel, "Usage : `!gps <latitude,longitude>` (`!help gps` pour plus de détails)")
                    lat, lng = args[1].split(",")
                    url = "https://api.what3words.com/v2/reverse?coords=" + lat + "," + lng + "&key=" + secret["w3w-key"] + "&lang=fr&format=json&display=minimal"
                    w3w = getUrl(url)['words']
                    if w3w == None : await client.send_message(message.channel, "Les coordonnées semblent être incorrectes... Respectez la syntaxe : `!gps <latitude,longitude>`.")
                    else :
                        await client.send_message(message.channel, "w3w : " + w3w)              
                        url = "https://services.gisgraphy.com/reversegeocoding/search?format=json&lat=" + lat + "&lng=" + lng
                        adresse = getUrl(url)['result'][0]
                        await client.send_message(message.channel, "adresse complète : " + adresse['formatedFull'])

                elif msg == "!speedtest":
                    loader = await client.send_message(message.channel, "Recherche du meilleur serveur...")
                    s = speedtest.Speedtest()
                    s.get_best_server()
                    await client.edit_message(loader, "Mesure du débit descendant (ça peut prendre un certain temps)...")
                    s.download()
                    await client.edit_message(loader, "Mesure du débit montant (ça peut prendre un certain temps)...")
                    s.upload()
                    await client.edit_message(loader, "Génération d'une jolie image trop stylée...")
                    url = s.results.share()
                    await client.delete_message(loader)
                    await client.send_message(message.channel, url)


                elif msg.startswith("!lmgtfy") or msg.startswith("!lmqtfy") or msg.startswith("!qwant"):
                    args = msg.split(" ")
                    if len(args) < 2 : await client.send_message(message.channel, "Usage : `" + args[0] + " <recherche>` (`!help " + args[0][1:] + "` pour plus de détails)")
                    else :
                        recherche = " ".join(args[1:])
                        url = "https://api.qwant.com/egp/search/web?count=10&q=" + quote_plus(recherche)
                        resultats = getUrl(url)
                        if resultats['status'] == "error" : await client.send_message(message.channel, "Une erreur s'est produite, j'espère que c'est pas parce que t'as écrit n'importe quoi \N{WINKING FACE}")
                        else :
                            txt = "Voici les 10 premiers liens de ta recherche sur Qwant :\n"
                            if args[0][3] == "g" : txt +=  "(t'as quand même pas cru que j'allais utiliser Google \N{SMILING FACE WITH OPEN MOUTH AND TIGHTLY-CLOSED EYES})\n"
                            for i in resultats['data']['result']['items'] : txt += i['url'] + "\n"
                            txt += "Voilà, voilà..."
                            await client.send_message(message.channel, txt)

                elif msg.startswith("!unicode") :
                    if len(msg) != 10 : await client.send_message(message.channel, "Usage : `!unicode <c>` (`!help unicode` pour plus de détails)")
                    else :
                        c = msg[9]
                        await client.send_message(message.channel, "Le caractère `" + c + "` répond au doux nom de **" + name(c) + "** et son code Unicode est **" + str(ord(c)) + "**.")

                elif msg.startswith("!chr") :
                    args = msg.split(" ")
                    if len(args) != 2 : await client.send_message(message.channel, "Usage : `!chr <code>` (`!help chr` pour plus de détails)")
                    else :
                        try :
                            c = chr(int(args[1]))
                            await client.send_message(message.channel, "Le caractère correspondant au code " + args[1] + " est le suivant : `" + c + "` (" + name(c) + ").")
                        except (ValueError, OverflowError) : await client.send_message(message.channel, "Aucun caractère ne correspond à ce numéro...")

                elif msg == "!loc" :
                    l = popen("wc -l tux.py").read().split(" ")[0]
                    s = popen("ls -lh tux.py").read().split(" ")[4] + "o"
                    await client.send_message(message.channel, "Mon code source (écrit en Python) comporte actuellement " + l + " lignes (" + s + ").")

                elif msg.startswith("!crypto") :
                    args = msg.split(" ")
                    if len(args) < 2 : await client.send_message(message.channel, "Usage : `!crypto <nom de la monnaie>`")
                    else :
                        req = " ".join(args[1:]).lower()
                        crypto = getUrl("https://api.coinmarketcap.com/v1/ticker/?limit=0")
                        cid = None
                        for i in crypto :
                            if i["id"].lower() == req or i["name"].lower() == req or i["symbol"].lower() == req :
                                cid = i["id"]
                        if cid :
                            data = getUrl("https://api.coinmarketcap.com/v1/ticker/" + cid + "/?convert=EUR")[0]
                            txt = "**valeur :** " + data["price_eur"] + "€ (" + data["price_usd"] + "$ ou encore " + data["price_btc"] + "\u20BF)\n"
                            if data["percent_change_1h"][0] != "-" : data["percent_change_1h"] = "+" + data["percent_change_1h"]
                            txt += "**évolution depuis 1h :** " + data["percent_change_1h"] + "%\n"
                            if data["percent_change_24h"][0] != "-" : data["percent_change_24h"] = "+" + data["percent_change_24h"]
                            txt += "**évolution depuis 24h :** " + data["percent_change_24h"] + "%\n"
                            if data["percent_change_7d"][0] != "-" : data["percent_change_7d"] = "+" + data["percent_change_7d"]
                            txt +="**évolution depuis une semaine :** " + data["percent_change_7d"] + "%\n"
                            txt += "**volume (24h) :** " + data["24h_volume_eur"] + "€\n"
                            if data["market_cap_eur"] : txt +="**capitalisation boursière :** " + data["market_cap_eur"] + " €"
                            embed=discord.Embed(title=data["name"] + " (" + data["symbol"] + ")", description=txt, color=0x00ff00)
                            await client.send_message(message.channel, embed=embed)
                        else : await client.send_message(message.channel, "Je n'ai pas trouvé cette crypto-monnaie...")

                elif msg.startswith("!user") :
                    if len(message.mentions) == 1 :
                        member = message.mentions[0]
                        user = await client.get_user_info(member.id)
                        em = discord.Embed(title=user.name, colour=0x00ff00)
                        em.set_image(url=user.avatar_url)
                        if user.bot : em.add_field(name="bot :", value="oui", inline=True)
                        else : em.add_field(name="bot :", value="non", inline=True)
                        em.add_field(name="id :", value=user.id, inline=True)
                        em.add_field(name="discriminator :", value=user.discriminator, inline=True)
                        em.add_field(name="compte créé le", value=time.strftime("%d/%m/%Y", date.timetuple(user.created_at)), inline=True)
                        em.add_field(name="serveur rejoint le", value=time.strftime("%d/%m/%Y", date.timetuple(member.joined_at)), inline=True)
                        em.add_field(name="statut :", value=str(member.status), inline=True)
                        if member.game : em.add_field(name="jeu :", value=str(member.game), inline=True)
                        if member.top_role : em.add_field(name="plus grand role :", value=str(member.top_role), inline=True)
                        if member.nick : em.add_field(name="surnom :", value=member.nick, inline=True)
                        await client.send_message(message.channel, embed=em)
                    else : await client.send_message(message.channel, "Usage : `!user @quelqu'un`")

                elif msg == "!life": await client.send_file(message.channel, "life.gif")
                
                elif msg == "!gratuit": await client.send_file(message.channel, "gratuit.png")

                elif msg == '!haddock':
                    with open("haddock.txt","r") as f : c = f.read().split('\n')
                    await client.send_message(message.channel, random.choice(c))
                    
                    
                    




                # ^ nouvelles commandes ici ^

                elif len(msg) > 2 and msg[0] == '!' :
                   await client.send_message(message.channel, 'A tes souhaits ' + message.author.mention + ' !')

                ancienmsg[serv] = msg
                
        except Exception :
            txt = time.strftime('[%d/%m/%Y %H:%M:%S]\n') + format_exc() + "\n\n"
            with open("log/erreurs.txt","a") as f : f.write(txt)
                

    #client.loop.create_task(actu())
    client.run(secret["discord-token"])
except Exception :
    txt = "\n\n##########[ERREUR FATALE]##########\n" + time.strftime('[%d/%m/%Y %H:%M:%S]') + format_exc() + "\n\n"
    with open("log/erreurs.txt","a") as f : f.write(txt)
    time.sleep(60*10)
    with open("log/erreurs.txt","a") as f : f.write(time.strftime('[%d/%m/%Y %H:%M:%S]') + "Tux va tenter de redemarrer\n")
popen("python3 tux.py &")
        

