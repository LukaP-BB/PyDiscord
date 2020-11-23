#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import discord          #on fait un bot pour discord, c'est de première nécessité
from discord.ext import commands
from discord.ext.commands import CommandNotFound
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
import coroPack.interface as itf
import coroPack.geo as geo
import anniv as anvs

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
bot = commands.Bot(command_prefix = '$', intents=intents) #création d'une instance de bot

DATE_HEURE_CONNEXION = datetime.datetime.now()

#************ FERMETURE DU BOT *************************************************

@bot.command(hidden=True)
async def quit(ctx):
    if ctx.author.id == 404395089389944832 :
        await ctx.send("Au revoir")
        print("Bot éteint sans anicroches")
        await bot.close()
    else :
        await ctx.send("nope")

@bot.command()
async def lulu(ctx, member : discord.Member = None):
    auteur = ctx.message.author
    if member == None and auteur.id != 621748334104805416:
        await ctx.send(f"Laisses Lucie tranquille {auteur.mention} !")
    elif member == None :
        await ctx.send(f"Gnagnagnagna")
    else :
        await ctx.send(f"Laisses Lucie tranquille {member.mention} !")

@bot.event
async def on_member_join(member):
    print(member)
    MYSELF = bot.get_user(404395089389944832)
    await MYSELF.send(f"{member.mention} a rejoint le serveur **{member.guild}** :D")
    if member.guild.id == 630852721573888061 :
        channel = bot.get_channel(759743347245449237)
    else :
        channel = bot.get_channel(671289712576692234)
        role_retour = discord.utils.get(member.guild.roles, id=671289711846883328)
        await member.add_roles(role_retour, reason=None, atomic=True)
    await channel.send(f"Bienvenue {member.mention} ! <:youpicquet:685075741259595781>")

@bot.event
async def on_member_leave(member):
    MYSELF = bot.get_user(404395089389944832)
    await MYSELF.send(f"{member.mention} a quitté le serveur :(")

@bot.command()
async def ban(ctx):
    await ctx.send(f"T'as cru quoi {ctx.author.mention} ? <:kekw:636583908334501899>")

@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, user_id, reason=None):
    MYSELF = bot.get_user(404395089389944832)
    ID = re.search(r"\d{17,20}", user_id).group(0)
    print(ID)
    ID = int(ID)
    guild = ctx.guild
    person = bot.get_user(ID)
    if ID == 404395089389944832 :
        await ctx.author.send(f"Bien essayé {ctx.author.mention} 🤣\nEnvoie un message à {MYSELF.mention}.")
        await guild.kick(ctx.author.id, reason="On ne kick pas le patron, namého")
    else :
        await guild.kick(person, reason=reason)
        await ctx.send(f"🦀 {ctx.author.mention} a kick {person.mention} 🦀")

@kick.error
async def kickerr(ctx, error):
    await ctx.send("Je n'ai pas pu trouver la personne mentionnée...")

#----------- commandes liées au calendrier -------------------------------------

@bot.command()
async def zzz(ctx):
    roles = [role.name for role in ctx.author.roles]
    if "alternant" in roles :
        calurl = "https://edt.univ-nantes.fr/sciences/g351268.ics"
    elif "biostats" in roles :
        calurl = "https://edt.univ-nantes.fr/medecine/g497301.ics"
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
            calurl = "https://edt.univ-nantes.fr/medecine/g497301.ics"
            statut = "Biostats"
            colour = discord.Colour.red()
        else :
            statut = "Bioinfos"
            calurl = "https://edt.univ-nantes.fr/sciences/g351247.ics"
            colour = discord.Colour.green()

    # useless and childish easter eggs
    if amount == 69 :
        ctx.send("Nice 😏")
    elif amount == 42 :
        ctx.send("<:YouKnow:648164979245318144>")
    elif amount == 420 :
        ctx.send("🌿")
    # and useful stuff
    elif amount > 3 :
        await ctx.send("""```fix
A chaque jour suffit sa peine, pas plus de 3 cours OK ? 😴
```""")
    else :
        fstr = f"> __**Cours à venir : **__\n> *Les cours suivants sont prévus pour les __{statut}__ :*\n"
        await ctx.send(fstr)
        events = icp.searchTimetable(calurl, amount)
        try :
            for event in events :
                dictres = icp.formatTT2(event['description'], event["date"])
                embed = discord.Embed(title=dictres["Matière"],
                                    description=event["date"],
                                    colour=colour)
                embed.add_field(name="Salle", value=dictres["Salle"], inline=False)
                embed.add_field(name="Enseignant", value=dictres["Enseignant"], inline=False)
                embed.add_field(name="Groupes", value=dictres["Groupes"], inline=False)
                await ctx.send(embed=embed)
        except AttributeError:
            await ctx.send(f"Aucun cours n'a été trouvé pour les __{statut}__, tanquille la vie ?")


################################################################################
## COMMANDES CORO --------------------------------------------------------------
@commands.cooldown(1, 5, commands.BucketType.guild)
@bot.group()
async def coro(ctx):
    if ctx.invoked_subcommand is None :
        await ctx.send("Pour de l'aide sur la commande Coro, utilises `!coro help`")

@coro.command()
async def help(ctx):
    await ctx.send(itf.help_message)

@coro.command()
async def plot(ctx, *args):
    args = itf.parseArgs(args)
    # print(args)
    file = discord.File("fig.jpg")
    if args["type"] == "hospi" :
        async with ctx.channel.typing():
            infos = itf.plotFromArgs(args)
            embed = discord.Embed(
                title=infos["Titre"],
                description=infos["Description"],
                colour=discord.Colour.magenta())
            embed.set_image(url="attachment://fig.jpg")
            if len(infos["Erreurs"]) > 0 :
                for info in infos["Erreurs"] :
                    embed.add_field(name="Information : ", value=info)
            await ctx.send(file=file, embed=embed)
    elif args["type"] == "tests" :
        if args["dep"] == "FR" :
            await ctx.send("Il faut spécifier un département (pour l'instant)")
        else :
            async with ctx.channel.typing():
                dep, d1, d2 = geo.plotGivenDep(dep=args["dep"], params=args, d1=args["d1"], d2=args["d2"])
                embed = discord.Embed(
                    title=f"Courbe des dépistages positifs : {dep}",
                    description=f"Entre le {d1} et le {d2}\nMoyenne flottante sur 15 jours",
                    colour=discord.Colour.magenta())
                embed.set_image(url="attachment://fig.jpg")
                await ctx.send(file=file, embed=embed)

@plot.error
async def plot_error(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("La commande n'a pas été invoquée correctement, utilises `!coro help` pour plus d'informations !")

@coro.command()
async def dep(ctx, *args):
    args = itf.parseArgs(args)
    if args["type"] == "dep" :
        await ctx.message.author.send(itf.sendDeps())
        await ctx.send(f"Je t'ai envoyé la liste des département en message privé {ctx.author.mention}")

@coro.command()
async def carte(ctx, typeD=None, days=40, fmean=15):
    if typeD not in ["tests", "hospi"] :
        await ctx.send("Il faut donner un type de données : `!coro carte tests` pour les données de dépistage et `!coro carte hospi`pour les données hospitalières")
    else :
        async with ctx.channel.typing():
            if typeD == "tests" :
                df = geo.donnesDepistage(days=days, floatingMean=fmean)
                typeD = "taux de tests positifs"
            else :
                df = geo.donnesHosp(days=days, floatingMean=fmean)
                typeD = "nombre de décès répertoriés (données hospitalières)"
            geo.mapDepInfection(df)
            file = discord.File("fig.jpg")
            embed = discord.Embed(
                title=f"Progression du Covid : augmentation du {typeD}",
                description=f"Départements ou le Covid progresse le plus vite depuis {days} jours. \nMoyenne flottante sur {fmean} jours",
                colour=discord.Colour.magenta())
            embed.set_image(url="attachment://fig.jpg")
            await ctx.send(file=file, embed=embed)

@coro.error
async def coro_error(ctx, error):
    if isinstance(error, commands.errors.CommandOnCooldown) :
        await ctx.send(f"Minute papillon, laisses moi quelques secondes ! :rage: {ctx.author.mention}")
    else :
        with open("id.txt", "r") as idtxt :
            id = int(idtxt.read())
        MYSELF = bot.get_user(id)
        await MYSELF.send(f"Une erreur non anticipée est advenue : \n'{error}'\n\
Serv : {ctx.guild.name}\n\
Salon : {ctx.channel.mention}")



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
async def anniv(ctx, com="False", amount=3):
    liste_anniversaires = anvs.loadAnnivs()
    today = datetime.date.today()

    datesAnniv = [key for key in liste_anniversaires.values()]

    if today in datesAnniv and com not in ["next", "help"]:
        annivsToday = [key for key in liste_anniversaires if liste_anniversaires[key] == today ]
        for key in annivsToday :
            user = bot.get_user(key)
            mess_anniv = anvs.sendRandMess(user)
            await ctx.send(random.choice(mess_anniv))

    elif com == "next" or com == "False" :
        if com == "next" :
            title = "<:youpicquet:685075741259595781>"
        else :
            title = "Pas d'anniversaire aujourd'hui 😢"
        embed = discord.Embed(
                title=title,
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

    elif today == datetime.datetime(2020, 12, 1) :
        la_super_phrase_de_marine = "blabla"
        await ctx.send(la_super_phrase_de_marine)


#************* JEU DE HASARD ***************************************************

@bot.command(help="Un petit jeu pour tuer le temps : il faut taper $score suivi d'un guess entre 0 et 100. Le bot trouve un nombre mystère aléatoire et fait la différence avec ton guess. Plus celle-ci est petite, plus tu es lucky")                           #commande $score : permet de faire un guess et d'obtenir la différence avec ce guess
async def score(ctx, guess):

    random.seed()                           #initialise la seed et
    score = random.randint(0,100)           #renvoie un nb pseudo aléatoire dans l'intervalle [0;100]
    delta = abs(score-int(guess))  # 2 lignes pour calculer la différence absolue entre le guess et le score obtenu (abs vient de la bibliothèque math)

    await ctx.send(f'nombre mystère : {resultats}\ndifférence : {delta}')


    today = datetime.date.today()       #2 lignes pour écrire la date d'obtention du score

    resultats = open("resultats.txt","a")   #ouvre le fichier resultats.txt en mode "append" : chaque écriture se fait à la suite de ce qui est déjà écrit
    resultats.writelines([str(ctx.message.author), " : " ,str(delta), " : ", str(today),"\n"]) #ecrit le nom d'utilisateur, le score et la date dans chaque nouvelle ligne du .txt
    resultats.close()   # a priori utile de fermer le fichier une fois écrit pour pouvoir l'ouvrir dans une autre commande

# gestion d'erreurs pour le mini jeu
@score.error
async def score_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il faut mettre un nombre après $score")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("$score n'accepte pas les chaines de caractères :rage:")
    else:
        await ctx.send("erreur")

# COMMANDE BEST
@bot.command(help="Cette commande renvoie le nom d'utilisateur ayant eu le meilleur delta par rapport à son guess.\n\
Les résultats sont rentrés dans un fichier quand $score est appelé, et cette commande lit le fichier qui en résulte.")
#commande pour extraire celui ayant le meilleur guess, accompagné de la date
async def best(ctx):
    with open("resultats.txt", "r") as resultats :
        min = 101
        for line in resultats:
            match = re.search(r'(: )(\d?\d)( :)', line) #chaque expression entre parenthèse correspond à un groupe
            if match:
                score_obtenu = match.group(2)          #le group(2) fait référence aux deuxièmes parenthèses du match
                score_obtenu = int(score_obtenu)
                if (score_obtenu < min):
                    min = score_obtenu
                    match = re.search('[^0-9^#]*', line)
                    if match:
                        nom = match.group(0)
                    match = re.search(r'\d{4}-\d{2}-\d{2}', line)
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
    with open("cartouches.txt","r") as cartouches :
        qte = int(1.5*int(cartouches.read()))
    with open("cartouches.txt","w") as cartouches :
        cartouches.write(str(qte))
    await ctx.send(f'{qte} articles se sont pris une cartouche :gun:')

# SINOQUET ------------------
@bot.command()
async def sinoquet(ctx):
    with open("bot-sinoquet.txt","r") as phrases :
        phrases = phrases.readlines()
    await ctx.send(random.sample(phrases, 1)[0].strip())


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
@bot.command(help="Supprime un salon et un rôle\n\
Donner le nom du salon et du rôle en arguments de la commande\n\
Pour les noms composés de plusieurs mots, utiliser les guillemets")
@commands.has_permissions(administrator=True)
async def dels(ctx, ch : discord.TextChannel, rl : discord.Role):
    await rl.delete()
    await ch.delete()
@dels.error
async def dels_error():
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("tu n'as pas les droits, loser !")


#************ PARTIE COMPTAGE DES MESSAGES / EVENTS ****************************

@bot.event
async def on_reaction_add(reaction, user):
    try :
        name = reaction.emoji.name
        ID = reaction.emoji.id
        name = f"<:{name}:{ID}>"
    except :
        name = reaction.emoji
        if name == "📌" :
            await reaction.message.pin(reason=f"{user}")
        if name == "🔨" :
            await reaction.message.unpin(reason=f"{user}")
    else :
        with open("reactions.json", "r", encoding="utf-8") as reactionF :
            reactions = json.load(reactionF)

        if name in reactions.keys() :
            reactions[name] +=1
        else :
            reactions[name] = 1

        with open("reactions.json", "w+", encoding="utf-8") as reactionF :
            json.dump(reactions, reactionF)
    # print(name)


@bot.event
async def on_reaction_remove(reaction, user):
    if reaction.emoji == "📌" :
        await reaction.message.unpin(reason=f"{user}")


@bot.command()
async def reactions(ctx) :
    with open("reactions.json", "r") as reactionF :
        reactions = json.load(reactionF)

    reactions = sorted(reactions.items(), key=lambda item: item[1], reverse=True)
    reactions = [f"{reaction[1]} : {reaction[0]}" for reaction in reactions]
    await ctx.send("> **Top des réactions :** \n> \n> " + "\n> ".join(reactions))

#Comptage des messages, envoi de messages aléatoire et réaction aux messages ***
@bot.event
async def on_message(message):
    if  message.guild is None :
        print(f"Message reçu de {message.author} : {message.content}\n")

    #partie comptage ---------
    elif message.guild.id in [621610918429851649, 630852721573888061]  :
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

    # NOTE: this is essential for the bot to stay aware of commands
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
        message = (f"Tu as envoyé {nb_messages} messages {ctx.message.author.mention}\nT'es le top 1, le king, on ne voit que toi sur discord, félicitations BG")
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

def timeDeltaToStr(timedelta:datetime.timedelta) :
    reg = r"(\d{1,3}):(\d{2}):(\d{2}.\d*)"
    find = re.search(reg, str(timedelta))
    heures = int(find.group(1))
    minutes = int(find.group(2))
    secondes = float(find.group(3))
    jours = timedelta.days
    if heures > 23 :
        jours = heures//24
        heures = heures%24
    return jours, heures, minutes, secondes

#Personnes les plus bavardes du chat
@bot.command()
async def rank(ctx, a="new"):
    if a ==  "new" :
        fileRangs = "rangs.json"
        jours, heures, minutes, secondes = timeDeltaToStr(datetime.datetime.now()-DATE_HEURE_CONNEXION)
        infos = f"Messages envoyés depuis la dernière reconnexion du bot il y a {jours} jours, {heures} heures, {minutes} minutes et {secondes} secondes"

    elif a == "old":
        fileRangs = "rangs_old.json"
        infos = "Vieux décompte des messages, c'était l'bon temps"
    top = 5
    liste_auteurs = []
    with open(fileRangs, "r") as rangs:
        rangsDict = json.load(rangs)
        liste_auteurs = sorted(rangsDict, key=lambda auteur: rangsDict[auteur], reverse=True)
    sortie = ""
    i = 1
    for auteur in liste_auteurs :
        sortie = sortie + (f"Top {i} : {auteur} avec {str(rangsDict[auteur])} messages\n")
        i += 1
    embed = discord.Embed(title="Qui spam le plus le salon ?", description=sortie)
    await ctx.send(infos)
    await ctx.send(embed=embed)

#************ ON AFFICHE LES BOLCHEVIKS ET ON LOG LES MESSAGES SUPPRIMES *******

#en cas de suppression de message
@bot.event
async def on_message_delete(message):
    if len(message.content) > 2 and not message.author.bot :
        now = datetime.datetime.now()
        now = now - datetime.timedelta(hours=1, seconds=3)
        #On vérifie si le message a été supprimé par son auteur ou par un modérateur
        guild = message.guild
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
    print('Bot connecté')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Plague Inc."))

#************ FIN ***********************FIN ***********************************

def main():
    with open('token.txt', 'r') as token :
        t = token.read()
        # t = "NjU1NzIzMzk0MDAzNjMyMTI5.XfYP_w.SqH0-3I6CxoKPDlZABwY_Luyzqg"
        bot.run(t)

if __name__ == '__main__':
    main()
