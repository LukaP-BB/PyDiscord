#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import re
import datetime as dt
import locale
import requests as req

# locale.setlocale(locale.LC_ALL, 'fr')

def CalFromUrl(url):
    return req.get(url).text

def CalFromFile(file):
    eventLines = ""
    with open(file, "r", encoding="utf-8") as calFile :
        for line in calFile.readlines():
            eventLines += line
    return eventLines

def findEvents(eventLines):
    regCheck = "BEGIN:VEVENT"
    findsCheck = len(re.findall(regCheck, eventLines))
    """takes a string in the ics format and returns a list of dicts with available infos"""
    regex = re.compile("BEGIN:VEVENT\r?\n\
(DTSTART:(?P<dtstart>(.*))\r?\n)?\
(DTEND:(?P<dtend>(.*))\r?\n)?\
(UID:(.*)\r?\n)?\
(SUMMARY:(?P<summary>(.*))\r?\n)?\
(LOCATION:(?P<location>(.*))\r?\n)?\
(DESCRIPTION:(?P<description>((.*)+))\r?\n)?\
(END:VEVENT)?")
    finds = [match.groupdict() for match in regex.finditer(eventLines)]
    finds = sorted(finds, key=lambda a: a["dtstart"])
    if findsCheck == len(finds) :
        infos = "All events found"
    else :
        infos = "Some events may be missing"
    return finds

def parseDate(dateIcal):
    """Takes an iCal date (str) and returns a datetime object"""
    year = int(dateIcal[:4])
    month = int(dateIcal[4:6])
    day = int(dateIcal[6:8])
    hour = int(dateIcal[9:11])
    min = int(dateIcal[11:13])
    date = dt.datetime(year=year, month=month, day=day, hour=hour, minute=min, tzinfo=dt.timezone.utc)
    timeZoneNow = dt.datetime.now().astimezone().tzinfo
    return date.astimezone(timeZoneNow)

def nextC(calendar, amount):
    amount = int(amount)
    listOfEvents = []
    i = 0
    now = dt.datetime.now().astimezone()
    while now > parseDate(calendar[i]["dtstart"]):
        i += 1
    for x in range(i, i+amount) :
        d = parseDate(calendar[x]["dtstart"]).strftime("%H:%M%p")
        d2 = parseDate(calendar[x]["dtend"]).strftime("%H:%M%p, %d %B")
        if calendar[x]['summary'] or calendar[x]['description'] :
            infos = {}
            infos["date"] = f"{d} → {d2}"
            infos["summary"] = calendar[x]['summary'].replace('\\n', '\n').replace("\\", "")
            infos["description"] = calendar[x]['description'].replace('\\n', '\n').replace("\\", "")
            listOfEvents.append(infos)

    return listOfEvents

def searchTimetable(url, amount):
    eventLines = CalFromUrl(url)
    events = findEvents(eventLines)
    return nextC(events, amount)

def timeToEnd(url):
    eventLines = CalFromUrl(url)
    events = findEvents(eventLines)
    now = dt.datetime.now().astimezone()
    i = 0
    while now > parseDate(events[i]["dtstart"]):
        date = parseDate(events[i]["dtend"])
        i += 1
    now = dt.datetime.now().astimezone()
    secsRemaining = int((date-now).total_seconds())
    return round(secsRemaining/60, 1)


if __name__ == '__main__':
    calurl = "https://edt.univ-nantes.fr/sciences/g351247.ics"
    print(timeToEnd(calurl))
    print(searchTimetable(calurl, 5))


# pouet