import asyncio
import aiohttp
import time
import asyncio
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.keys import Keys
import time
from pprint import pprint
import json
import itertools
import pandas as pd

import copy

import pymongo



client = pymongo.MongoClient("mongodb://localhost:27017/")
db=client["info_macth_1xbet"]
collection=db["id_1xbet_live"]
db1=client["info_betkeen"]




collection1=db["id_champ_1xbet_live"]
collection2=db["liste_match_live"]


result=collection2.find({},{"Value.O1":1,'_id':0})
result=collection2.find({},{"Value.I":1 ,"Value.O1":1 ,"Value.O2":1,"Value.CI":1,"Value.L":1,"Value.S":1,'Value.SG.0.MG':1 ,'_id':0})
#pprint(list(result))
p=list(result)
z=[list(x.values()) for x in p]
resultat = list(itertools.chain.from_iterable(z))
resultat = list(itertools.chain.from_iterable(resultat))
resultat=list(filter(lambda d: "O2" in d, resultat))
#pprint(resultat)

a = map(lambda x: {**x, "events": f"{x['O1']} v {x['O2']}"}, resultat)


a=list(a)
l=["Asian Handicap","Goal Lines","Match Odds","Over/Under 0.5 Goals", "Over/Under 1.5 Goals", "Over/Under 2.5 Goals" ,"Over/Under 3.5 Goals", "Over/Under 4.5 Goals" ,"Over/Under 5.5 Goals" ,"Over/Under 6.5 Goals", "Over/Under 7.5 Goals", "Over/Under 8.5 Goals","Half Time", "First Half Goals 0.5","First Half Goals 1.5","First Half Goals 2.5" ]
'''
for i in range(len(list(a))):
	a[i]=[{**copy.deepcopy(a[i]), "market":l[_]} for _ in range(len(l))]
#print(a)
resultat = list(itertools.chain.from_iterable(a))
#print(resultat)
'''

#d=db1.con.find()
#pprint(list(d))


event=sorted(a,key=lambda x:x["S"])


#je cree une liste des confrontation uniquement 

event1=map(lambda x:x['events'],event)
print(list(event1))

#cree des fonction pour filter les mactchs que je ne veux pas

def _4X4(x):
	return "4x4".lower() not in x.lower()
def _3X3(x):
	return "3x3".lower() not in x.lower()
def _5X5(x):
	return "5x5".lower() not in x.lower()

def klask(x):
	return "KLASK".lower() not in x.lower()


def short(x):
	return 'Short'.lower() not in x.lower()

def specials(x):
	return "Specials".lower() not in x.lower()

def special(x):
	return "Special".lower() not in x.lower()

def statistics(x):
	return "Statistics".lower() not in x.lower()

def alternative(x):
 	return "Alternative".lower() not  in x.lower()
def region(x):
	return "Regional".lower() not in  x.lower()

a1=filter(lambda x: _3X3(x["L"]) and _4X4(x["L"]) and _5X5(x["L"]) and klask(x["L"]) and short(x["L"]) and specials(x["L"]) and special(x["L"]) and statistics(x["L"]) and alternative(x["L"]) and region(x["L"]), event) 

event1=list(event1)



p=list(a1)
print(p)
import pickle

# Sauvegarder la liste dans un fichier binaire
with open('match1xbet.pickle', 'wb') as f:
    pickle.dump(p, f)

print(len(p))










