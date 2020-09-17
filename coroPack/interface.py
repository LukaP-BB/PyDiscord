#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
import re
import datetime as dtt

# print(dtt.date.isoformat(dtt.date.today()))

import coroPack.analyse as anl

help_message = """
**Aide pour la commande coro :**
```
Exemples :
    $coro
    $coro 44
    $coro 75 hosp
    $coro dc rad
    $coro 10-07-2020
    $coro help
    $coro dep

Cette commande permet de créer un graphique basé sur les données hospitalières relatives au Covid disponibles sur data.gouv .
Un certain nombre d'arguments sont acceptés, et le bot fera de son mieux pour les interpréter :
    - pas d'arguments : toutes les données sont renvoyées à l'échelle de la france
    - le département voulu : on peut utiliser soit le code, soit le nom (le code doit être à 2 ou 3 chiffres uniquement, ex : 01, 109)
    - une ou deux dates au format jj-mm-aaaa. Si une seule date est fournie, le bot assume que l'on veut les infos entre la date donnée et aujourd'hui
    - le type de données hospitalières parmi :
        + hosp : les personnes hospitalisées (nb de personnes par jour)
        + rea : les personnes en réanimation (par jour)
        + dc : le cumul des personnes décédées
        + rad : le cumul des personnes retournées à domicile
    - help : affiche ce message
    - dep : envoie en DM la liste des départements acceptés (leur code et leur nom)

Source des données : https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/#_
```"""

def sendDeps():
    deps = anl.loadDeps()
    finalStr = "```py\nLes département : \n"
    i = 0
    for dep in deps :
        finalStr += f"{dep['code']} - \"{dep['name']}\"\n"
        i+=1
    finalStr += "```"

    return finalStr

def look4dep(args, deps):
    """Look for a department in the args and returns it if found, else, returns 'FR'"""
    for arg in args :
        for dep in deps :
            arg = arg.lower()
            if arg==dep["name"].lower() or arg==dep["slug"].lower() or arg==dep["code"].lower() :
                return dep["code"]
    return "FR"

def order(a, b):
    """Returns two ordered dates"""
    if a > b :
        return b, a
    else :
        return a, b

def sortDates(params, args):
    """Looks for dates in the arguments, and add them to the parameters passed to the higher level function"""
    date = re.findall("(\d\d)-(\d\d)-(\d\d\d\d)", " ".join(args))
    if len(date) == 1 :
        d1 = date[0]
        d1 = "-".join((d1[2],d1[1],d1[0]))
        d2 = dtt.date.isoformat(dtt.date.today())
        d1, d2 = order(d1, d2)
        params["d1"] = d1
        params["d2"] = d2
    elif len(date) == 2 :
        d1 = date[0]
        d2 = date[1]
        d1 = "-".join((d1[2],d1[1],d1[0]))
        d2 = "-".join((d2[2],d2[1],d2[0]))
        d1, d2 = order(d1, d2)
        params["d1"] = d1
        params["d2"] = d2
    else :
        params["d1"] = "2020-03-18"
        params["d2"] = dtt.date.isoformat(dtt.date.today())
        if len(date) > 2 :
            params["err"].append("Une ou plusieurs date(s) ont été détectée(s) et ignorée(s)")

    return params

def sortDataType(params, args):
    allFalse = True
    for param in ["hosp", "rea", "rad", "dc"] :
        if param in args :
            params[param] = True
            allFalse = False
        else :
            params[param] = False

    if allFalse :
        for param in ["hosp", "rea", "rad", "dc"] :
            params[param] = True

    return params

def parseArgs(args):
    params = {
        "type" : "plot",
        "dep" : None,
        "d1" : None,
        "d2" : None,
        "err" : [],
    }
    if "dep" in args or "départements" in args :
        params["type"] = "dep"
    elif "help" in args :
        params["type"] = "help"
    else :
        deps = anl.loadDeps()
        params["dep"] = look4dep(args, deps)
        params = sortDates(params, args)
        params = sortDataType(params, args)
    return params

def depFromCode(code):
    deps = anl.loadDeps()
    for dep in deps :
        if dep["code"] == code :
            return dep["name"]

def fromIsoformat(date) :
    date = re.search("(\d\d\d\d)-(\d\d)-(\d\d)", date)
    annee = date.group(1)
    mois = date.group(2)
    jour = date.group(3)
    return f"{jour}/{mois}/{annee}"

def getInfos(args):
    """returns a dict of human readable formated strings for the final display"""
    finalInfos = {}
    dataType = {
        "hosp" : "hospitalisations",
        "rea" : "réanimation",
        "dc" : "décès",
        "rad" : "retours à domicile"
    }
    if args["dep"] == "FR" :
        region = "France"
    else :
        region = depFromCode(args["dep"])
    d1 = fromIsoformat(args["d1"])
    d2 = fromIsoformat(args["d2"])
    finalInfos["Titre"] = f"Données hospitalières pour le covid : {region}"
    typesDeDonnees = []
    for type in dataType :
        if args[type] : typesDeDonnees.append(dataType[type])
    finalInfos["Description"] = f"{', '.join(typesDeDonnees).capitalize()}\n Entre le {d1} et le {d2}"
    finalInfos["Erreurs"] = args["err"]
    return finalInfos

def plotFromArgs(args):
    """Creates a plot in jpg format with the given arguments"""
    df2 = anl.loadData()

    if args["dep"] == "FR" :
        df2 = anl.france(df2)
    else :
        df2 = anl.parDep(df2, args["dep"])
    df2 = anl.timeFrame(df2, args["d1"], args["d2"])
    anl.plotThat(df2, args)

    # generate some infos to be printed somewhere
    finalInfos = getInfos(args)
    return finalInfos

if __name__ == '__main__':
    args = parseArgs(sys.argv)
    print(args)
    dfFromArgs(args)
