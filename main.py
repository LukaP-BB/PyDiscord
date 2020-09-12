#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import discord          #on fait un bot pour discord, c'est de première nécessité
import random           #importe la bilbiothèque nécessaire pour créer de l'aléatoire
import math             #importe le module math pour la valeur aboslue
import re               #importe les expressions régulières
import datetime         #importe la date du jour et des méthodes en rapport
import time             #permet d'utiliser sleep
import json             #pour interragir avec des fichiers json
import os               #pour interragir avec le système, lancer des commandes en bash par exemple
import subprocess       #même idée
from chat import *
import iCalParser as icp

import anniv as anvs

from discord.ext import commands

bot = commands.Bot(command_prefix = '$') #création du préfixe qui servira à dire "ceci est une commande"

#************ FERMETURE DU BOT *************************************************

@bot.command(hidden=True)
async def quit(ctx):
    if ctx.author.id == 404395089389944832 :
        await ctx.send("Au revoir")
        print("Bot éteint sans anicroches")
        await bot.close()
    else :
        await ctx.send("nope")

#-------- pour tuer les subprocess ---------------------------------------------
@bot.command()
async def kill(ctx):
    PanicBot.terminate()
    p4.terminate()
    child.terminate()

#----------- commandes liées au calendrier -------------------------------------
@bot.command()
async def zzz(ctx):
    roles = [role.name for role in ctx.author.roles]
    if "alternant" in roles :
        calurl = "https://edt.univ-nantes.fr/sciences/g351268.ics"
    else :
        calurl = "https://edt.univ-nantes.fr/sciences/g351247.ics"

    time = icp.timeToEnd(calurl)
    if time > 0 :
        await ctx.send(f"Il te reste {time} minutes à souffrir, tiens bon")
    else :
        await ctx.send("T'es en cours là ? Mouais...")


@bot.command()
async def cours(ctx, amount=1):
    try :
        amount = int(amount)
    except :
        await ctx.send("Cette commande s'utilise ainsi : `$cours <int>` avec 0<int<5")
        return 1
    try :
        roles = [role.name for role in ctx.author.roles]
    except AttributeError:
        await ctx.send("Non.")
        return 1
    else :
        if "alternant" in roles :
            statut = "Alternants"
            calurl = "https://edt.univ-nantes.fr/sciences/g351268.ics"
            colour = discord.Colour.purple()
        elif "biostats" in roles :
            await ctx.send("Viens plutôt boire un coup ;)")
            return 0
            # calurl = "https://edt.univ-nantes.fr/sciences/g351247.ic"
            # statut = "Biostats"
        else :
            statut = "Bioinfos"
            calurl = "https://edt.univ-nantes.fr/sciences/g351247.ics"
            colour = discord.Colour.green()
    if amount > 4 :
        await ctx.send("A chaque jour suffit sa peine, pas plus de 4 cours OK ?")
    else :
        events = icp.searchTimetable(calurl, amount)
        embed = discord.Embed(
            title="Cours à venir",
            colour=colour,
            description=(f"Les cours suivants sont prévus pour les {statut}"))
        for event in events :
            embed.add_field(
                name=(event["date"]),
                value=(f"{event['summary']}\n\n{event['description']}"))
        await ctx.send(embed=embed)

#-------- Envoi de messages 'intelligents' -------------------------------------
@bot.command(hidden = True)
async def m(ctx, chan_id, content):
    if ctx.author.id in [404395089389944832, 264153089823604746] :
        chan = bot.get_channel(int(chan_id))
        await chan.send(content)
        if  ctx.message.guild is not None :
            print(f"Message reçu de {message.author} : {message.content}\n")
    else :
        await ctx.send("Fous moi la paix !")
############## ANNIVERSAIRES ###################################################
# d = datetime.date
@bot.command()
async def anniv(ctx, com="False", amount=1):
    liste_anniversaires = anvs.loadAnnivs()
    today = datetime.date.today()
    datesAnniv = [key for key in liste_anniversaires.values()]

    if today in datesAnniv and com not in ["next", "help"]:
        print("ON Y EST ARRIVE !!")
        annivsToday = [key for key in liste_anniversaires if liste_anniversaires[key] == today ]
        for key in annivsToday :
            user = bot.get_user(key)
            mess_anniv = anvs.sendRandMess(user)
            await ctx.send(random.choice(mess_anniv))

    elif com == "next" or com == "False" :
        embed = discord.Embed(
                title="Pas d'anniversaire aujourd'hui 😢",
                colour = discord.Colour.magenta(),
                description="Voici le(s) anniversaire(s) à venir : ")
        annivsNext = [key for key in liste_anniversaires.keys() if liste_anniversaires[key] > today]
        x = 0
        while x < int(amount) and x < len(annivsNext)-1 :
            try :
                ID = annivsNext[x]
                personneAgee = bot.get_user(ID)
                embed.add_field(
                    name=(personneAgee.display_name),
                    value=(liste_anniversaires[ID].strftime('%d/%m')))
            except :
                print(f"La personne suivante n'est pas détectée : {ID}")
            x += 1
        await ctx.send(embed=embed)

    elif com == "help" :
        await ctx.send(
"Utilises `$anniv` tel quel pour ping la personne dont c'est l'anniversaire\n\
Utilises `$anniv next <nombre>` pour connaitre les anniversaires à venir"
        )


################################################################################
###############   CORO #########################################################
import requests
@bot.command()
async def coro(ctx, arg1="France", arg2="recovered"):

    if arg1 == "infos" :
        await ctx.send("> Usage de la CoroCommande :\n\
```$coro <Pays> <info_recherchée>```\n\
> <Pays> doit être soit un nom de pays en anglais, soit 'global', et l'info recherchée peut se trouver dans cette liste :\n\
> *[cases,todayCases,deaths,todayDeaths,recovered,critical]*\n\
> Par défaut, et pour des raisons d'optimisme, le défaut est basé sur les personnes rétablies en France\n\
*ps : je ne sais rien de la fiabilité du site dont je tire les infos, molo sur l'interprétation*")
    elif arg1 == "global" :
        web = requests.get("https://corona.lmao.ninja/all")
        i = json.loads(web.text)
        # print(liste)
        # try :
        nombre = i[arg2]

        if arg2 == "cases" :
            remplacement = "cas au total"
        elif arg2 == "todayCases" :
            remplacement = "cas aujourd'hui"
        elif arg2 == "deaths" :
            remplacement = "morts au total"
        elif arg2 == "todayDeaths" :
            remplacement = "morts aujourd'hui"
        elif arg2 == "recovered" :
            remplacement = "personnes rétablies"
        elif arg2 == "critical" :
            remplacement = "personnes en état critique"

        phrase = f"A ce jour, il y a eu {nombre} {remplacement} dans le monde"
        await ctx.send(phrase)
        # except :
        #     await ctx.send("Vérifie bien que tu as mis un nom de pays valide, `$coro infos` pour plus de détails")

    else :
        web = requests.get("https://corona.lmao.ninja/countries")
        liste = json.loads(web.text)
        # print(liste)
        try :
            for i in liste :
                if i["country"] == arg1 :
                    nombre = i[arg2]

                    if arg2 == "cases" :
                        remplacement = "cas au total"
                    elif arg2 == "todayCases" :
                        remplacement = "cas aujourd'hui"
                    elif arg2 == "deaths" :
                        remplacement = "morts au total"
                    elif arg2 == "todayDeaths" :
                        remplacement = "morts aujourd'hui"
                    elif arg2 == "recovered" :
                        remplacement = "personnes rétablies"
                    elif arg2 == "critical" :
                        remplacement = "personnes en état critique"

                    phrase = f"Il y a eu {nombre} {remplacement} dans ce pays : {arg1}"
                    await ctx.send(phrase)
        except :
            await ctx.send("Vérifie bien que tu as mis un nom de pays valide, `$coro infos` pour plus de détails")
################################################################################


#************* JEU DE HASARD ***************************************************

@bot.command(help="Un petit jeu pour tuer le temps : il faut taper $score suivi d'un guess entre 0 et 100. Le bot trouve un nombre mystère aléatoire et fait la différence avec ton guess. Plus celle-ci est petite, plus tu es lucky")                           #commande $score : permet de faire un guess et d'obtenir la différence avec ce guess
async def score(ctx, guess):

    random.seed()                           #initialise la seed et
    score = random.randint(0,100)           #renvoie un nb pseudo aléatoire dans l'intervalle [0;100]

    guess = int(guess)
    delta = abs(score-guess)  # 2 lignes pour calculer la différence absolue entre le guess et le score obtenu (abs vient de la bibliothèque math)

    await ctx.send('nombre mystère : {}'.format(score)) #renvoie le résultat en msg discord
    await ctx.send('différence : {}'.format(delta))     #renvoie la différence

    from datetime import date
    today = date.today()       #2 lignes pour écrire la date d'obtention du score

    resultats = open("resultats.txt","a")   #ouvre le fichier resultats.txt en mode "append" : chaque écriture se fait à la suite de ce qui est déjà écrit
    resultats.writelines([str(ctx.message.author), " : " ,str(delta), " : ", str(today),"\n"]) #ecrit le nom d'utilisateur, le score et la date dans chaque nouvelle ligne du .txt
    resultats.close()   # a priori utile de fermer le fichier une fois écrit pour pouvoir l'ouvrir dans une autre commande

# gestion d'erreurs pour le mini jeu
@score.error
async def score_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il faut mettre un nombre après $score")
    elif(error, commands.CommandInvokeError):
        await ctx.send("$score n'accepte pas les chaines de caractères :rage:")
    else:
        await ctx.send("erreur")

# COMMANDE BEST
@bot.command(help="Cette commande renvoie le nom d'utilisateur ayant eu le meilleur delta par rapport à son guess.\nLes résultats sont rentrés dans un fichier quand $score est appelé, et cette commande lit le fichier qui en résulte.")
#commande pour extraire celui ayant le meilleur guess, accompagné de la date
async def best(ctx):
    resultats = open("resultats.txt", "r")
    min = 101
    for i, line in enumerate(resultats):
        match = re.search('(: )(\d?\d)( :)', line) #chaque expression entre parenthèse correspond à un groupe
        if match:
            score_obtenu = match.group(2)          #le group(2) fait référence aux deuxièmes parenthèses du match
            score_obtenu = int(score_obtenu)
            if (score_obtenu < min):
                min = score_obtenu
                match = re.search('[^0-9^#]*', line)
                if match:
                    nom = match.group(0)
                match = re.search('\d{4}-\d{2}-\d{2}', line)
                if match:
                    date = match.group(0)
        else:
            print("il n'y a pas encore de résultat")
    await ctx.send("{} a obtenu le meilleur delta, à savoir {} le {}".format(nom, min, date))


# ************* UNE SERIE DE FLORILEGES DE PHRASES TYPIQUES ********************

# SERRANO --------------
@bot.command(help="Quelques phrases typiques 😉")
async def serrano(ctx):
    random.seed()                           #initialise la seed
    lol = ["Considérez les préfixes comme étant corrects",
            "N'oubliez pas, les distanciels c'est 80% du temps de travail !",
            "Merci à Emmanuel Desmontils :heartpulse: :heart_eyes:",
            "On range son portable !",
            "FAITES PASSER LE PAQUET !!! :rage:",
            "Ne soyez pas non plus de mauvaise foi !",
            "UN PAQUET C'EST UNE COPIE",
            "Ne prenez pas mon stylo sinon on va tous être malade :nauseated_face: ",
            "Faut être plus précis",
            "Vous devez compléter le tableau !"
            ]
    await ctx.send(lol[random.randint(0,(len(lol)-1))])

# MEKAOUCHE ------------------
@bot.command(help="Quelques phrases typiques 😉")
async def mekaouche(ctx):
    random.seed()
    lol = ["Tu vas pas me salir, je vais pas te salir",
            "Et si on commençait par 30 minutes pour découvrir un nouveau language : Bash. Quoi ? vous avez eu des cours ?",
            "MAIS REGARDE DANS TON COURS !!",
            "Regarde dans ton cours..."]
    await ctx.send(lol[random.randint(0,(len(lol)-1))])


# GODART --------------
@bot.command(help="Quelques phrases typiques 😉")
async def godart(ctx):
    random.seed()
    lol = ["on a réglé le problème en supprimant l'individu",
    "Dans le cadre d'un management de projet on est plus sur un management de crise total que de management pro-actif",
    "C’est pas parce que c’est ma réponse que vous devez mettre la mienne"]
    await ctx.send(lol[random.randint(0,(len(lol)-1))])

# TELETCHEA -----------------
@bot.command()
async def teletchea(ctx):
    cartouches = open("cartouches.txt","r")
    qte=cartouches.read()
    await ctx.send(f'{qte} articles se sont pris une cartouche :gun:')
    qte=int(qte)
    qte=qte*1.5
    qte=int(qte)
    cartouches.close
    cartouches = open("cartouches.txt","w")
    qte=str(qte)
    cartouches.write(qte)
    cartouches.close

#************* SUPPRESSION DE MESSAGES *****************************************

@bot.command(help="efface le nombre de messages indiqué", hidden=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, nb_messages : int):
    await ctx.channel.purge(limit=nb_messages+1)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Tu n'as pas les droits, nameho !")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Il faut mettre un nombre après $clear")
    else :
        print(error)
#     else :
#         MYSELF = bot.get_user(404395089389944832)
#         await MYSELF.send(f"Une erreur non anticipée est advenue : \n'{error}'\n\
# Salon : {ctx.channel.name}")


#************* UNE FONCTION POUR LIMITER LES DISTRACTIONS **********************
@bot.command(help="Pour récupérer l'accès aux salons")
async def retour(ctx):
    role_m1 = discord.utils.get(ctx.guild.roles, id=627581972025442314)
    role_retour = discord.utils.get(ctx.guild.roles, id=671289711846883328)
    await ctx.author.add_roles(role_m1, reason=None, atomic=True)
    await ctx.author.remove_roles(role_retour, reason=None, atomic=True)

@bot.command(help="Quand tu as besoin d'éliminer les distractions liées à ce discord")
async def silence(ctx):
    role_m1 = discord.utils.get(ctx.guild.roles, id=627581972025442314)
    role_retour = discord.utils.get(ctx.guild.roles, id=671289711846883328)
    await ctx.author.remove_roles(role_m1, reason=None, atomic=True)
    await ctx.author.add_roles(role_retour, reason=None, atomic=True)



#************* GESTIONS DE SALONS **********************************************
#création de salons privés
@bot.command(help="Ecrire la commande suivie du nom du salon.\nPour ecrire plusieurs mots, ecrire la phrase entre guillemets")
@commands.has_permissions(administrator=True)
async def salon(ctx, arg):   #nom de la commande
#création du rôle
    guild = ctx.guild
    role = await guild.create_role(name=arg)

#création du salon
    cat=ctx.channel.category #permet de connaitre la catégorie du salon textuel, sinon le salon est créé tout en haut dans le serveur
    roles = {
    guild.default_role: discord.PermissionOverwrite(read_messages=False),
    role: discord.PermissionOverwrite(read_messages=True)
}
    await guild.create_text_channel(name=arg, overwrites=roles, category=cat)   #puis création du salon avec le même nom
@salon.error
async def salon_error():
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("tu n'as pas les droits, loser !")


#suppression des rôles et salons
@bot.command(help="Supprime un salon et un rôle\nDonner le nom du salon et du rôle en arguments de la commande\nPour les noms composés de plusieurs mots, utiliser les guillemets")
@commands.has_permissions(administrator=True)
async def dels(ctx, ch : discord.TextChannel, rl : discord.Role):
    await rl.delete()
    await ch.delete()
@dels.error
async def dels_error():
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("tu n'as pas les droits, loser !")


#************ PARTIE COMPTAGE DES MESSAGES / EVENTS ****************************

# @bot.event
# async def on_reaction_add(reaction, user):
#     from spammage import rappel2
#     await rappel2(reaction, user)

#Comptage des messages, envoi de messages aléatoire et réaction aux messages ***
@bot.event
async def on_message(message):
    # from spammage import rappel
    # await rappel(message)

    #partie comptage ---------
    if  message.guild is None :
        print(f"Message reçu de {message.author} : {message.content}\n")

    elif message.guild.id == 621610918429851649  : #and len(message.content)>2
        # await message.add_reaction("🎉")
        # await message.add_reaction("🎂")
        # await message.add_reaction("🍺")
        # await message.add_reaction("🍻")
        # await message.add_reaction("🥃")
        # await message.add_reaction("🍷")
        # await message.add_reaction("🥰")

        auteur=str(message.author)
        try :
            with open("rangs.json", "r+") as rangs:
                liste_auteurs=json.load(rangs)
                if auteur in liste_auteurs :
                    liste_auteurs[auteur] = liste_auteurs[auteur] +1
                else :
                    liste_auteurs[auteur] = 1
        except Exception as e:
            print(e)
        try :
            with open("rangs.json", "w+") as rangs:
                rangs.write(json.dumps(liste_auteurs, sort_keys=True, indent=4))
        except Exception as e:
            print(e)

    # await rand_mess(message)    #envoi aléatoire de message
    await react_emoji(message)  #réaction par emoji à certains messages
    await react_mess(message)   #réaction textuelle à certains messages
    #await discut(message)       #réaction à une mention du bot

    await bot.process_commands(message)


#Nombre de messages de l'auteur
@bot.command()
async def mess(ctx):
    somme = 0
    auteur = (str(ctx.message.author))
    with open("rangs.json", "r") as auteurs:
        liste = json.load(auteurs)
        nb_messages = liste[auteur]
    max = 0
    for auteur in liste :
        somme += int(liste[auteur])
        if int(liste[auteur]) > max :
            max = int(liste[auteur])
            print(max)
    if nb_messages >= max-1 :
        message = (f"Tu as envoyé {nb_messages} messages {ctx.message.author.mention}\n T'es le top 1, le king, on ne voit que toi sur discord, félicitations BG")
    elif nb_messages/somme > 1/10 :
        message = (f"Tu as envoyé {nb_messages} messages {ctx.message.author.mention}\nTu fais partie de l'élite, le top 10%, GG")
    elif nb_messages/somme > 1/15 :
        message = (f"Tu as envoyé {nb_messages} messages {ctx.message.author.mention}\nPas dégueu, merci de rendre ce forum actif !")
    elif nb_messages/somme > 1/30 :
        message = (f"Tu as envoyé {nb_messages} messages {ctx.message.author.mention}\nDes gens parlent plus, des gens parlent moins")
    elif nb_messages/somme > 1/60 :
        message = (f"Tu as envoyé {nb_messages} messages {ctx.message.author.mention}\nQuelques efforts sont à fournir")
    elif nb_messages/somme > 1/200 :
        message = (f"Tu as envoyé {nb_messages} messages {ctx.message.author.mention}\nIl va falloir penser à se réveiller")
    else :
        message = (f"Tu as envoyé {nb_messages} messages {ctx.message.author.mention}\nJe crois que je ne peux plus rien pour toi...")
    await ctx.send(message)

#Personnes les plus bavardes du chat
@bot.command()
async def rank(ctx):
    top=5
    liste_auteurs = []
    with open("rangs.json", "r") as rangs:
        dict = json.load(rangs)
        for key, value in dict.items():
            temp = [key,value]
            liste_auteurs.append(temp)
            if len(liste_auteurs)<int(top) :
                top = int(len(liste_auteurs))
    liste_auteurs.sort(key=lambda liste_auteurs: liste_auteurs[1], reverse=True)
    sortie = ""
    i = 1
    for auteur in liste_auteurs :
        sortie = sortie + (f"Top {i} : {auteur[0]} avec {str(auteur[1])} messages\n")
        i+=1
    embed = discord.Embed(title="Qui spam le plus le salon ?", description=sortie)
    await ctx.send(embed=embed)

#************ ON AFFICHE LES BOLCHEVIKS ET ON LOG LES MESSAGES SUPPRIMES *******

#en cas de suppression de message
@bot.event
async def on_message_delete(message):
    if len(message.content) > 2 and not message.author.bot :
        now=datetime.datetime.now()
        now=now - datetime.timedelta(hours=1, seconds=3)
        #On vérifie si le message a été supprimé par son auteur ou par un modérateur
        guild=message.guild
        #Pour cela, on va chercher le dernier log de suppression de message
        async for entry in guild.audit_logs(limit=1, after=now, action=discord.AuditLogAction.message_delete):
            censeur=entry.user        #on récupère le nom du modo
            date_supr=entry.created_at
        with open ("log.txt", "a", encoding="utf8") as log:
            try :
                log.write(
                f"Auteur du message : {message.author}\n \
                Contenu : {message.content}\nModo : {censeur}\n \
                Date de suppression : {date_supr}\n \
                Chan : {message.channel} \n*******************\n"
                )
            except :
                print("Something went wrong...")
        print (f"heure suppression  \t: {now}\nheure log \t: {date_supr}")

        if now<date_supr :
            embed = discord.Embed(
                title="Alerte !",
                description=(f"{censeur} a supprimé un message de manière inopinée, \
                    c'est innacceptable ! \nT'es pire qu'un bolchevik {censeur}"))
            embed.add_field(
                name=("Voyons ce que contenait ce message victime de despotisme : "),
                value=(f"{message.content}\nPar : {message.author}"))
            await message.channel.send(embed=embed)
        else :
            pass
            # await message.channel.send("🤫")


#********** COMMANDE D'AIDE ****************************************************

@bot.command()
async def aide(ctx):
    embed = discord.Embed(title="Aide",
    description="Comment utiliser les différentes commandes ? \
        \nLa commande $help joue un rôle similaire, en moins bien \
        \nUtiliser $help <commande> te permettra (ou pas) d'obtenir des informations plus détaillés sur la commande")
    embed.add_field(
        name="$score",
        value="Mini jeu : le but est de d'entrer un nombre entre 0 et 100 après la commande. \
        Le bot te dira quel nombre il avait tiré et la différence entre avec ton tirage")
    embed.add_field(
        name="$best",
        value="Renvoie le nom de celui ayant la plus petite différence. Je reset la commande quand quelqu'un a un 0")
    embed.add_field(
        name="$serrano, $teletchea, $mekaouche, $godart",
        value="Juste pour rire :)")
    embed.add_field(
        name="$salon",
        value="Crée un salon et un rôle dont le nom est donné en argument, réservé aux admins")
    embed.add_field(
        name="$dels",
        value="Efface un salon et un rôle. \
        Il faut mettre le nom du salon en premier argument et le nom du rôle en deuxième argument, réservé aux admins")
    embed.add_field(
        name="$mess",
        value="Te dit combien de messages tu as envoyé pendant que le bot est up")
    embed.add_field(
        name="$rank",
        value="Le classement des gens les plus bavards")
    embed.add_field(
        name="$jeux",
        value="Appelle le bot de jeux s'il n'est pas en ligne\n\
        Celui-ci permet de jouer à puissance 4 pour l'instant")
    embed.add_field(
        name="$silence, $retour",
        value="$silence permet de masquer la majorité des salons, $retour permet de revenir à la normale")
    await ctx.send(embed=embed)

#************** APPEL DU BOT DE TESTING ****************************************

@bot.command(help="Apelle un bébé bot afin de réaliser des tests à l'éthique discutable")
async def BOT(ctx):
    await ctx.send("Je t'envoie mon fils, il est un peu bordélique mais parfois il est utile...")
    with open("summon.txt", "w+") as summon :
        summon.write(str(ctx.channel.id))
    global child
    child = subprocess.Popen("./child.py")

#************** APPEL DU BOT DE JEUX *******************************************

@bot.command(help="Appelle le bot de jeux")
async def jeux(ctx):
    channel = bot.get_channel(667101857948237844)
    await ctx.send("Prend garde, le maître des jeux arrive !")
    if ctx.channel.id not in [667101857948237844, 640263768764317699] :
        await ctx.send(f"Pour la suite, ça se passe ici : {channel.mention}")
    with open("summon.txt", "w+") as summon :
        summon.write(str(ctx.channel.id))
    global p4
    p4 = subprocess.Popen("./p4.py")


#************* GESTION GLOBALE DES ERREURS *************************************
from discord.ext.commands import CommandNotFound
@bot.event
async def on_command_error(ctx, error):
    # pass
    if isinstance(error, CommandNotFound):
        await ctx.send("Cette commande n'existe pas")
    else:
        MYSELF = bot.get_user(404395089389944832)
        await MYSELF.send(f"Une erreur non anticipée est advenue : \n'{error}'\n\
Serv : {ctx.guild.name}\n\
Salon : {ctx.channel.mention}")
        print(error)

#commande pour obtenir la latence du bot ***************************************
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong !\nLatence : {round(bot.latency, 4)} secondes")
    # print(len(bot.emojis))
    for _ in range(20) :
        await ctx.message.add_reaction(random.choice(bot.emojis))


#*************MESSAGE D'ACCUEIL ************************************************
@bot.event
async def on_ready():
    print('bonjour')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Untitled Goose Game"))

#************ FIN ***********************FIN ***********************************

with open('token.txt', 'r') as token :
    t = token.read()
    bot.run(t)
