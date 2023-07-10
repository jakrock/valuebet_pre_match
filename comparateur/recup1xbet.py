import asyncio
import aiohttp
import time
import asyncio
import httpx
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
import pymongo
import itertools


import sys
#sys.stdout = open("NUL", "w")




client = pymongo.MongoClient("mongodb://localhost:27017/")
db=client["info_macth_1xbet"]
collection=db["id_1xbet_live"]




collection1=db["id_champ_1xbet_live"]
collection2=db["liste_match_live"]


async def effectuer_requete(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json_response = await response.json()
            return json_response
url="https://1xbet.mobi/LineFeed/GetChampsZip?sport=1&lng=fr&tf=1440&tz=2&country=182"
#url='https://1xbet.mobi/LiveFeed/GetChampsZip?sport=1&lng=en&country=182'


loop=asyncio.get_event_loop()
a=loop.run_until_complete(effectuer_requete(url))
d=[]
for j,i in enumerate(a["Value"]):
    #pprint(i["LI"])
    d.append([j,i["CI"],i["LI"]])

result=collection1.delete_many({})
print(f"Nombre de documents supprimés : {result.deleted_count}")
result=collection1.insert_one({"liste":d})

print("ID du document inséré :", result.inserted_id)

l=collection1.find_one()["liste"]
print(l[2])
#k1=f"https://1xbet.mobi/LineFeed/Get1x2_VZip?sports=1&champs={i[2]}&count=50&lng=fr&tz=2&mode=4&country=182&getEmpty=true"
urls=[f"https://1xbet.mobi/LineFeed/Get1x2_VZip?sports=1&champs={i[2]}&count=50&lng=en&mode=4&country=182&getEmpty=true&mobi=true" for i in l]
print(urls)
taille_lot=20
lot=[urls[i:i+taille_lot] for i in range(0,len(urls),taille_lot)]

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        print(f"fetching {url}")
        async with session.get(url) as response:
            row=await response.read()
            row_data=json.loads(row.decode("utf-8"))
            return row_data

async def fetch_urls(urls):
    return await asyncio.gather(*(fetch(url) for url in urls))            

  
def requetemorceaux(morceaux):
    loop = asyncio.get_event_loop()
    beg = time.time()
    a = loop.run_until_complete(fetch_urls(morceaux))
    return a

result=collection2.delete_many({})
print(f"Nombre de documents supprimés : {result.deleted_count}")
n=0
while n<len(lot):
    try:
        a = requetemorceaux(lot[n])
    except Exception as e :
        n-=1
        print(f" erreur{e}")
        time.sleep(5)
        print("il a une erreur")
        continue
    n+=1 
    if a:       
        result=collection2.insert_many(a)
        print("IDs des documents insérés :", result.inserted_ids)
        time.sleep(5)


result=collection2.find({},{"Value.I":1 ,"Value.O1":1 ,"Value.O2":1,"Value.CI":1,"Value.L":1,"Value.S":1 ,'_id':0})
p=list(result)
z=[list(x.values()) for x in p]
resultat = list(itertools.chain.from_iterable(z))
resultat = list(itertools.chain.from_iterable(resultat))
resultat=list(filter(lambda d: "O2" in d, resultat))
#pprint(resultat)

resultat = map(lambda x: {**x, "event": f"{x['O1']} v {x['O2']}"}, resultat)


d=db.collection.delete_many({})

d=db.collection.insert_one({"event":list(resultat)})

import subprocess

subprocess.run(['python3', 'text.py'])
subprocess.run(['python3', 'traitement.py'])


client.close()

import gc
gc.collect()

sys.exit()
