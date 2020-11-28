import discord          #on fait un bot pour discord, c'est de première nécessité
import random           #importe la bilbiothèque nécessaire pour créer de l'aléatoire
import math             #importe le module math pour la valeur aboslue
import re               #importe les expressions régulières
import datetime         #importe la date du jour et des méthodes en rapport
import time             #permet d'utiliser sleep
import json             #pour interragir avec des fichiers json
import os               #pour interragir avec le système, lancer des commandes en bash par exemple
import subprocess
from discord.ext import commands
bot = commands.Bot(command_prefix = '$') #création du préfixe qui servira à dire "ceci est une commande"

async def rand_mess(message):

    #partie envoi de message aléatoire (en essayant de ne pas spam)
    if re.search('\?', (message.content)) and not message.author.bot :
        if int(message.id)%47 == 0 :
            lol = ["Oui", "Non"]
            await message.channel.send(lol[random.randint(0,(len(lol)-1))])
    else :
        if int(message.id)%47 == 0 and not message.author.bot:
            random.seed()
            lol = ["...",
                    "OK",
                    f"On t'as déjà dit que tu as de beaux yeux ? 😍 {message.author.mention} ",
                    "C'est pas faux !",
                    "Oui",
                    "Non",
                    "Ça m'en touche une sans faire bouger l'autre",
                    "Merci pour ton intervention, c'était intéressant !",
                    "J'ai déjà entendu cette théorie",
                    "meh..",
                    "🥴",
                    "Haha, bonne blague :-) ",
                    "Nope",
                    "Je ne crois pas non"
                    ]
            await message.channel.send(lol[random.randint(0,(len(lol)-1))])

async def react_emoji(message):
    # if 672534227694125077 in [r.id for r in message.author.roles] and int(message.id)%40:
    #     await message.channel.send(f"On t'as déjà dit que t'as de beaux cheveux ? {message.author.mention}")
    #     await message.add_reaction("<:regrets:672800202461282322>")

    #partie réaction à des messages ----------
    if re.search('fleurs du malt|scierie|bois|boire|bière|berlin|sur mesure|vestiaire|chat noir|la maison|bar |biere|beer', (message.content).lower()):
        await message.add_reaction("🍺")

    if re.search('soif', (message.content).lower()) :
        await message.add_reaction("🍻")

    if re.search('whiskey|whisky', (message.content).lower()) :
        await message.add_reaction("🥃")

    if re.search('alcool', (message.content).lower()) :
        await message.add_reaction("🍷")

async def react_mess(message):

    contenu =  (message.content).lower()

    if re.search(' bot ', contenu) :
        print(contenu)
        await message.add_reaction("🤖")

        if re.search('merci', contenu) :
            lol = [
            f"Je savais que ça te ferais plaisir {message.author.mention}",
            f"A ton service ! {message.author.mention}",
            f"Ça me fait plaisir :wink: {message.author.mention}",
            f"Tkt BB, tjrs là pour toi ! {message.author.mention}",
            ]
            await message.channel.send(lol[random.randint(0,(len(lol)-1))])

        if re.search('🥰|😍|🤩|😘|❤|🧡|💛|💚|💙|💜|🤎|🖤|🤍|♥', contenu) :
            await message.channel.send(f"Arrête, je vais rougir :blush: {message.author.mention}")
            await message.add_reaction("💝")

        elif int(message.id)%7 == 0 :
            lol = ["On m'apelle ?",
                    f"Tu parles de moi {message.author.mention}, tu veux te battre ?",
                    ]
            await message.channel.send(lol[random.randint(0,(len(lol)-1))])

    # if re.search('merci', contenu) and not message.author.bot and int(message.id)%7 == 0 :
    #     lol = ["Mais de rien, c'est avec plaisir !",
    #             "De rien !",
    #             ]
    #     await message.channel.send(lol[random.randint(0,(len(lol)-1))])

    if (re.search('tg ', contenu)
        or re.search('ta gueule', (message.content).lower())
        or re.search('la ferme', (message.content).lower())
        or re.search('tais toi|nique ta mère', (message.content).lower())):
        lol = [f"Tu vas vite te calmer ! {message.author.mention}",
                f"Ça va mal se mettre ! {message.author.mention}",
                f"Ta maman ne t'as pas appris la politesse ? Gourgandin.e va {message.author.mention}",
                "Pour toute réclamation quand à mon comportement, le bureau des plaintes est au fond à droite 😉",
                "Merci de respecter la bienséance et la politesse dans ce salon.",
                ]
        await message.channel.send(lol[random.randint(0,(len(lol)-1))])
        await message.add_reaction("😡")
        await message.add_reaction("😒")
        await message.add_reaction("🙄")
        await message.add_reaction("😞")
        await message.add_reaction("😠")

    if re.search('fabien|panic|panique', contenu) and not message.author.bot :
        emoji = "<:Ipanic:776749782889660466>"
        await message.add_reaction(emoji)

    if re.search("^où.*\?", contenu) :
        await message.channel.send("Dans ton cul ! <:HyperJoy:628614965787623425>")

    if re.search("ça m'en touche une...", contenu) and not message.author.bot :
        await message.channel.send("...sans faire bouger l'autre")

# async def discut(message):
#
#     random.seed()
#
#
#     contenu = (message.content).lower()
#     if re.search("@!630846935493771274", contenu):
#
#         if re.search('^comment .* ?$', contenu) :
#             liste = ["oui", "non", "je ne sais pas"]
#             await message.channel.send(liste[random.randint(0,(len(liste)-1))])
