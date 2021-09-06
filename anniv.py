import json, datetime

def restoreAnnivs():
    d = datetime.date
    liste_anniversaires = {
    404395089389944832 : d(2021, 2, 8), #me
    345321795546775563 : d(2020, 10, 4), #romain
    545906454087991297 : d(2020, 10, 9), #jerome
    621624765211475979 : d(2020, 10, 9), #nicolas D
    621612049843093525 : d(2020, 11, 20), #paul
    274142551320297472 : d(2020, 12, 4), #florence
    509447801315262474 : d(2020, 12, 13), #fabien
    191953751131553793 : d(2021, 1, 21), #simon
    291319580461236225 : d(2021, 1, 29), #erwan
    264153089823604746 : d(2021, 2, 20), #Nicolas S
    616364333391413279 : d(2021, 3, 5), #coralie
    621989030900531200 : d(2021, 3, 5), #marie
    530161764420288512 : d(2021, 3, 31), #anne-emeline
    621656870356123648 : d(2021, 4, 27), #nathan
    622085418921492483 : d(2021, 5, 10), #léa
    249673860729929730 : d(2021, 5, 28), #alexis
    568038541020495882 : d(2021, 6, 24), #sarah
    621656884352516126 : d(2021, 7, 10), #louis
    623591669085896730 : d(2021, 7, 11), #antoine
    300603234597208065 : d(2021, 7, 15), #damien
    623535494994853898 : d(2021, 7, 19), #nora
    568855896525111307 : d(2021, 8, 14), #camille
    621748334104805416 : d(2021, 8, 22), #lucie
    573037185171980299 : d(2021, 9, 7), #marine
    428257059146825728 : d(2020, 9, 12), #elisa R
    }
    with open("anniv.json", "w+") as annivs :
        json.dump(liste_anniversaires, annivs, default=dateConverter, indent=0)

def dateConverter(date):
    if isinstance(date, datetime.date):
        return date.__str__()

def loadAnnivs():
    with open('anniv.json', "r") as annivs :
        try:
            annivDict = json.load(annivs)
        except Exception as e:
            restoreAnnivs()
            annivDict= loadAnnivs()
    b = {}
    for id in annivDict :
        date = annivDict[id]
        year, month, day = int(date[0:4]), int(date[5:7]), int(date[8:10])
        annivDate = datetime.date(year=year, month=month, day=day)
        if annivDate < datetime.date.today() :
            annivDate = annivDate.replace(year=datetime.date.today().year+1)
            print(annivDate)
        b[int(id)] = annivDate
    b =  dict(sorted(b.items(), key=lambda item: item[1]))

    with open("anniv.json", "w+") as annivs :
        json.dump(b, annivs, default=dateConverter, indent=0)

    return b

def sendRandMess(user) :
    mess_anniv = [
    f"Hey {user.mention}, bon anniversaire !!!",
    f"Hey {user.mention}, bon anniversaire !!!",
    f"Hey {user.mention}, peut-être que, pour le monde, tu n’es qu’une personne, mais pour des personnes tu es tout le monde, bon anniversaire !!!",
    f"Hey {user.mention}, quelques bougies de plus sur le gâteau ne peuvent rien faire d’autre que d’éclairer davantage ton visage, bon anniversaire !!!",
    f"Hey {user.mention}, ce ne sont pas des cheveux blancs. Ce sont les reflets de la sagesse, bon anniversaire !!!",
    f"Hey {user.mention}, nos anniversaires sont des plumes dans l’aile large du temps.",
    f"{user.mention} C'est l'anniversaire, dans tous les recoins. \nC'est presque tous les ans qu'on a l'anniversaire. \nGrâce à cet anni c'est la joie, c'est pratique. \nC'est au moins un principe à retenir pour faire la frite. \nCette année c'est bien, l'anniversaire tombe à pique!!",
    f"{user.mention}, Joyeux anniversaire rime avec 'reprends du dessert'. Un hasard ? Je ne pense pas !!!",
    f"{user.mention}, On ne peut pas cultiver son potager, mais à 80 ans on est un sacré pote âgé !!!",
    f"Hey {user.mention}, noyeux janniversaire !!!",
    f"Hey {user.mention}, bon anniversaire !!!",
    ]
    return mess_anniv

if __name__ == '__main__':
    for id, date in loadAnnivs().items() :
        print(id, " | ", date)
