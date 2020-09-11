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

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("\n\n\n\nBot de test connecté")
    with open("summon.txt", "r") as summon :
        channel = summon.read()
        channel = bot.get_channel(int(channel))
    await channel.send("Me voici ! Et non, ma chambre n'est pas rangée !")
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

#******************************************************************************
with open('token2.txt', 'r') as token :
    t=token.read()
    bot.run(t)
