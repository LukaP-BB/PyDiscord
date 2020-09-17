#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import json
import requests as req
from io import StringIO
import datetime

def loadDeps():
    with open("coroPack/json/departments.json", "r", encoding="utf-8") as departments :
        return json.load(departments)

def timeFrame(data, d1, d2):
    # print(d1, d2)
    data = data[data["jour"] >= d1]
    data = data[data["jour"] <= d2]
    return data

def parDep(data, zone):
    zone = str(zone)
    data = data[data.sexe==0]
    data = data[data.dep==zone]
    return data

def france(data):
    # working only on the whole population
    data = data[data.sexe==0]
    # summing all the departments
    data = data.groupby("jour", as_index=False).sum()
    return data

def plotThat(df, args):
    plt.style.use('Solarize_Light2')
    fig, ax = plt.subplots()
    if args["hosp"] : ax.plot(df.jour, df.hosp, label="Hospitalisations")
    if args["rea"] : ax.plot(df.jour, df.rea, label="Personnes en réanimation")
    if args["rad"] : ax.plot(df.jour, df.rad, label="Retours à domicile")
    if args["dc"] : ax.plot(df.jour, df.dc, label="Décès")
    ax.grid(True)
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax.yaxis.set_major_locator(plt.MaxNLocator(10))
    ax.legend()
    # plt.show()
    plt.savefig("fig.jpg")

def loadFromCache():
    return pd.read_csv("coroPack/data/data.csv", delimiter=";")

def loadFromUrl():
    url = "https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7"
    data = req.get(url).text
    with open("coroPack/data/data.csv", "w") as dataFile :
        dataFile.write(data)
    ioData = StringIO(data)
    with open("coroPack/data/lastDL.txt", "w") as lastdl :
        lastdl.write(datetime.date.today().isoformat())
    return pd.read_csv(ioData, delimiter=";")

def loadData():
    with open("coroPack/data/lastDL.txt", "r") as lastdl :
        last = lastdl.read()
    today = datetime.date.today().isoformat()
    if last < today :
        print("Loading data from URL")
        return loadFromUrl()
    else :
        print("Loading data from cache")
        return loadFromCache()


if __name__ == '__main__':
    # print(plt.style.available)
    # data = pd.read_csv("data.csv", delimiter=";")
    t1 = datetime.datetime.now()
    # loadFromUrl()
    loadData()
    print(datetime.datetime.now()-t1)
    # df = france(data)
    # df2 = parDep(data, 44)
    # timeFrame(df2)
    # print(df2)
    # plotThat(df)
    # plotThat(df2)
