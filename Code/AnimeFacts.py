import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


anime = pd.read_csv('../data/anime.csv')
rating = pd.read_csv('../data/rating.csv')
#18.896156858107716% animedest on mittehinnatud
#5.325516228201431% kasutajatest ei hinda ühtki animet

def mittehinnatud():
    #kasutajad = rating['user_id'].tolist()
    hinnangud = rating['rating'].tolist()
    mittehinnatud = 0
    kokku = 0
    for i in hinnangud:
        if i == -1:
            mittehinnatud += 1
        kokku += 1
    tulemus = mittehinnatud / kokku * 100

    print(str(round(tulemus, 2)) + "% anime vaatamistest on mittehinnatud")
mittehinnatud()

def mittehindajad():
    kasutajad = rating['user_id'].tolist()
    hinnangud = rating['rating'].tolist()
    kokku = 0
    mittehindajate_summa = 0
    hindajate_summa = 0
    kasutaja = kasutajad[0]
    indeks = 0
    polehinnanud = True
    for i in kasutajad:
        eelmine_kasutaja = kasutaja
        kasutaja = i
        if kasutaja != eelmine_kasutaja:
            if polehinnanud == True:
                mittehindajate_summa += 1
            kokku += 1
            polehinnanud = True
        if hinnangud[indeks] != -1:
            polehinnanud = False
        indeks += 1
    tulemus = mittehindajate_summa / kokku * 100
    print(str(round(tulemus, 2)) + "% kasutajatest ei hinda ühtki animet")
mittehindajad()

def allaXarvu(piir):
    animed = anime['rating'].tolist()
    vastus = 0
    kokku = 0
    for i in animed:
        if i < piir:
            vastus += 1
        kokku += 1
    protsent = vastus / kokku * 100
    print(str(vastus) + " animet " + str(kokku) + "-st on alla ratingu " + str(piir) + " ehk " + str(round(protsent, 2)) + "%")
allaXarvu(4.0)

def uleXarvu(piir):
    animed = anime['rating'].tolist()
    vastus = 0
    kokku = 0
    for i in animed:
        if i > piir:
            vastus += 1
        kokku += 1
    protsent = vastus / kokku * 100
    print(str(vastus) + " animet " + str(kokku) + "-st on üle ratingu " + str(piir) + " ehk " + str(round(protsent, 2)) + "%")
uleXarvu(8.0)