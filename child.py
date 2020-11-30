#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import discord
import json
import random
import re
import datetime
import anniversaires
from time import sleep
from discord.ext import commands
import functools

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("\nBot de test connecté")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="vos conneries"))

@bot.command(hidden=True)
async def exit(ctx):
    if ctx.author.id == 404395089389944832 :
        await ctx.send("Fermeture du bot de test...")
        print("bot de testing fermé avec succès")
        await bot.close()
    else :
        await ctx.send("nope")


#******************************************************************************

def profs(function):
    @functools.wraps(function)  # Important to preserve name because `command` uses it
    async def wrapper(ctx, add="", contenu=""):
        if add == "add" :
            contenu = "> " + contenu 
            with open("profs.json", "r", encoding="utf-8-sig") as profsFile :
                phrases = json.load(profsFile)
                phrases[function.__name__].append(contenu)
            with open("profs.json", "w", encoding="utf-8-sig") as profsFile :
                json.dump(phrases, profsFile, indent=4)
            mess = f"La phrase '{contenu}' a été ajoutée à la commande ${function.__name__} par {ctx.author}"
            print(mess)
            return await function(ctx, mess=mess)
        elif add == "all" :
            with open("profs.json", "r", encoding="utf-8-sig") as profsFile :
                phrases = json.load(profsFile)
            mess = "\n".join(phrases[function.__name__])
            return await function(ctx, mess=mess)       
        else :
            with open("profs.json", "r", encoding="utf-8-sig") as profsFile :
                phrases = json.load(profsFile)
            mess = random.sample(phrases[function.__name__], k=1)[0]
            return await function(ctx, mess=mess)
    return wrapper

@bot.command()
@profs
async def serrano(ctx, add="", mess=""):
    await ctx.send(mess)

@bot.command()
@profs
async def mekaouche(ctx, add="", mess=""):
    await ctx.send(mess)

@bot.command()
@profs
async def godart(ctx, add="", mess=""):
    await ctx.send(mess)

@bot.command()
@profs
async def sinoquet(ctx, add="", mess=""):
    await ctx.send(mess)


#******************************************************************************

t="NjU1NzIzMzk0MDAzNjMyMTI5.XfYP_w.SqH0-3I6CxoKPDlZABwY_Luyzqg"
bot.run(t)
