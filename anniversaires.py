import datetime
import discord
import random
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
d = datetime.datetime

@bot.command()
async def anniv(ctx):
    #anniversaires à venir :
    liste_anniversaires = {
    621989030900531200 : d(2020, 3, 5), #marie
    621656870356123648 : d(2020, 4, 27), #nathan
    249673860729929730 : d(2020, 5, 28), #alexis
    568038541020495882 : d(2020, 6, 24), #sarah
    621656884352516126 : d(2020, 7, 10), #louis
    623591669085896730 : d(2020, 7, 11), #antoine
    300603234597208065 : d(2020, 7, 15), #damien
    623535494994853898 : d(2020, 7, 19), #nora
    568855896525111307 : d(2020, 8, 14), #camille
    621748334104805416 : d(2020, 8, 22), #lucie
    573037185171980299 : d(2020, 9, 7), #marine
    428257059146825728 : d(2020, 9, 12), #elisa R
    345321795546775563 : d(2020, 10, 4), #romain
    545906454087991297 : d(2020, 10, 9), #jerome
    621624765211475979 : d(2020, 10, 9), #nicolas D
    621612049843093525 : d(2020, 11, 20), #paul
    274142551320297472 : d(2020, 12, 4), #florence
    509447801315262474 : d(2020, 12, 13), #fabien
    191953751131553793 : d(2021, 1, 21), #simon
    291319580461236225 : d(2021, 1, 29), #erwan
    }
    #manque : anne-emeline, nicolas S, coralie, léa, ollo, fatou

    for key in liste_anniversaires :
        print(key)
