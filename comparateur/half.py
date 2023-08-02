
import sqlite3
import pandas as pd
import pymongo
import pathlib
import os

import pandas as pd 
import pymongo
import sqlite3
import requests
from pprint import pprint 
import itertools
import json
#import aiosqlite
from datetime import datetime
import time
import asyncio
import aiohttp
import httpx
import time
import pickle
import uuid
import sys
#sys.stdout = open("NUL", "w")




client=pymongo.MongoClient('localhost',27017)
db=client["bet"]


contenu=''




db=client["info_betkeen"]
#collection= db["cookie_desktop"]
#collection1=db["cookie_mobile"]
con=db["liste_match_betkeen"]

c=client.info_betkeen.collection1
#__r=c.find()

__r=c.find({"name":"__RequestVerificationToken_Lw__"},{"value":1,"_id":0})
aspnet=c.find({"name":"ASP.NET_SessionId"},{"value":1,"_id":0})
#print(list(aspnet)[0]["value"])
ASPXAUTH=c.find({"name":".ASPXAUTH"},{"value":1,"_id":0})
#print(list(ASPXAUTH)[0]["value"])
#print(list(__r)[0]["value"])
#print(list(ASPXAUTH))
k= f'__RequestVerificationToken_Lw__={list(__r)[0]["value"]}; ASP.NET_SessionId={list(aspnet)[0]["value"]}; .ASPXAUTH={list(ASPXAUTH)[0]["value"]}'
headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'fr,fr-FR;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cookie':k,
    'referer': 'https://desk.easysport.bet/home/sports/1',
    'sec-ch-ua': '"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36 Edg/112.0.1722.48',
    'x-requested-with': 'XMLHttpRequest'
}

db_match_odd=client["finale_pre"]
collection1=db_match_odd["Half Time"]
data=list(collection1.find({},{"_id":0}))

collection2=db_match_odd["surebet"]
collection3=db_match_odd["valuebet"]
collection4=db_match_odd["storage"]
resultat=list(collection1.find({},{"_id":0}))
pprint(list(resultat))
'''
async def fetch_data(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url,headers=headers)
        asyncio.sleep(1)
        if response.status_code == 200:
            data = response.json()

            return data
        else:
            response.raise_for_status()'''
import aiohttp
import json

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            #await asyncio.sleep(5)
            if response.status == 200:
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' in content_type:
                    data = await response.json()
                    return data
                elif 'text/html' in content_type:
                    text = await response.text()
                    data = json.loads(text)
                    return data
                else:
                    raise ValueError(f"Unexpected Content-Type: {content_type}")
            else:
                response.raise_for_status()





async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            #await asyncio.sleep(5)
            if response.status == 200:
                return await response.json()
def flatten(l):
    for item in l:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def filtarage_valuebet():
    db=client["finale_pre"]
    collection=db["data supprimer"]
    for i in list(collection.find({},{'_id':0})) :
        result=collection3.delete_one({'id':i["id"]})

    temps=time.time()-2500
    result1=collection.delete_many({"last_update":{"$lt":temps}})

def filtarage_surbet():
    db=client["finale_pre"]
    collection=db["data supprimer1"]
    for i in list(collection.find({},{'_id':0})) :
        result=collection2.delete_one({'id':i["id"]})

    temps=time.time()-2500
    result1=collection.delete_many({"last_update":{"$lt":temps}})


import unicodedata

def enlever_caracteres_speciaux(chaine):
    chaine = unicodedata.normalize('NFKD', chaine).encode('ASCII', 'ignore').decode('utf-8')
    return chaine


import re

def enlever_caracteres_speciaux1(chaine):
    caracteres_speciaux = r"[(){}&,.'\"]"
    return re.sub(caracteres_speciaux, '', chaine)


# Cette fonction sert à supprimer les surebets qui ont 5 minutes d'existence sans être mis à jour
def last_surebet():
    db_match_odd=client["finale_pre"]
    collection2=db_match_odd["surebet"]
    cinq_minute = time.time() - 300
    result = collection2.delete_many({"last_update": {"$lt": cinq_minute}})
    print(f"{result.deleted_count} documents ont été supprimés.")


def last_surebet1():
    cinq_minute=time.time()-300
    result = collection3.delete_many({"last_update": {"$lt": cinq_minute}})


import aiohttp
from functools import reduce
#print(list(collection2.find({},{})))
result=collection2.delete_one({"id_1x2_1xbet":453156054})

async def match_odd_recuperation(a):
    b=a.copy()
    Id = a["id_half_1xbet"]
    
    # Le lien ici est pour les matchs en direct (liveFeed)
    url = f"https://1xbet.mobi/LineFeed/GetGameZip?id={Id+1}&lng=fr&tzo=2&isSubGames=true&GroupEvents=true&countevents=100&grMode=2&country=182&marketType=1&mobi=true"
    try :
        data = await fetch(url)
    except Exception as e:
        print(f"probleme {e} au niveau de l api 1xbet")
        return None
    #print(data)

    Id1 = a["id_half_betkeen"]
    print(Id1,a["events_betkeen"])
    url1 = f"https://mob.easysport.bet/Home/GetUpdateForm/?isaustralien=true&marketid={Id1}"
    try:
        data1 = await fetch_data(url1)
        #print(data1)
    except Exception as e:
        print(f'Probleme {e} au niveau de l api betkeen')
        return None
    betkeen=data1["EventMarket"]
    O1=data["Value"]["O1"].replace(" ","-")
    O1=enlever_caracteres_speciaux(O1)
    ci=data["value"]["CI"]
    O2=data["Value"]["O2"].replace(" ","-")
    O2=enlever_caracteres_speciaux(O2)
    _1xbet=f"{O1} v {O2}"
    unxbet=f"{O1}-{O2}".replace(" ","-")
    unxbet=enlever_caracteres_speciaux(unxbet)
    unxbet=enlever_caracteres_speciaux1(unxbet)
    ligue=data["Value"]["LE"].replace(" ","-").replace(".","")
    ligue=enlever_caracteres_speciaux(ligue)
    ligue=enlever_caracteres_speciaux1(ligue)
    LI=data["Value"]["LI"]
    lien=f"https://1xbet.mobi/fr/line/football/{LI}-{ligue}/{ci}-{unxbet}"
    print(lien)
    lien1=f"https://desk.easysport.bet/Home/FormBet/{Id1}"
    b["lien"]=lien
    b["lien1"]=lien1
    b["unxbet"]=unxbet
    b["ligue"]=ligue
    b["LI"]=LI
    b["betkeen"]=betkeen
    b["1xbet"]=_1xbet
    b["id"]=str(uuid.uuid4())
    data1 = data1["Selections"]
    if data1==[]:
        print("il n y a de data au niveau de l'api betkeen"  )
        return None
    #print(data1)

    t = {}
    try:
        a1 = [list(x.values()) for x in data["Value"]["GE"]]
    except Exception as e:
        print(f"le probleme //// {e} ////est survenu au niveau de <<a1=[list(x.values()) for x in data['Value']['SG'][0]['GE']]>>")
        return None
    a1 = flatten(a1)
    a1 = [elem for elem in a1 if isinstance(elem, dict)]
    print(a1)
    last_surebet1()
    last_surebet()
    try:
        home_half_betkeen = data1[0]["Back1Odds"]
        away_half_betkeen = data1[1]["Back1Odds"]
        draw_half_betkeen = data1[2]["Back1Odds"]
        home_half_1xbet = list(filter(lambda x: x["G"] == 1 and x["T"] == 1, a1))[0]["C"]
        away_half_1xbet = list(filter(lambda x: x["G"] == 1 and x["T"] == 3, a1))[0]["C"]
        draw_half_1xbet = list(filter(lambda x: x["G"] == 1 and x["T"] == 2, a1))[0]["C"]
        b["home_half_betkeen"] = home_half_betkeen
        b["away_half_betkeen"] = away_half_betkeen
        b["draw_half_betkeen"] = draw_half_betkeen
        b["home_half_1xbet"] = home_half_1xbet
        b["away_half_1xbet"] = away_half_1xbet
        b["draw_half_1xbet"] = draw_half_1xbet
    except Exception as e:
        print(f"le probleme vien surement de 1xbet {e}")
        return None
    value_home_half_1xbet=""
    value_away_half_1xbet=""
    value_draw_half_1xbet=""
    p_home_half_betkeen=(1/home_half_betkeen)
    p_away_half_betkeen=(1/away_half_betkeen)
    p_draw_half_betkeen=(1/draw_half_betkeen)

    marge=(p_home_half_betkeen+p_away_half_betkeen+p_draw_half_betkeen) -1
    if marge<0.07 and home_half_betkeen<12 and away_half_betkeen<12 and draw_half_betkeen<12:
        m_home_half_betkeen=(3*home_half_betkeen)/(3-marge*home_half_betkeen)
        m_away_half_betkeen=(3*away_half_betkeen)/(3-marge*away_half_betkeen)
        m_draw_half_betkeen=(3*draw_half_betkeen)/(3-marge*draw_half_betkeen)

        if (home_half_1xbet > m_home_half_betkeen) and (home_half_1xbet - m_home_half_betkeen > 0.02):
            value_home_half_1xbet = home_half_1xbet
            print(value_home_half_1xbet)
        if (away_half_1xbet > m_away_half_betkeen) and (away_half_1xbet - m_away_half_betkeen > 0.02):
            value_away_half_1xbet = away_half_1xbet
            print(value_away_half_1xbet)
        if (draw_half_1xbet > m_draw_half_betkeen) and (draw_half_1xbet - m_draw_half_betkeen > 0.02):
            value_draw_half_1xbet = draw_half_1xbet
            print(value_draw_half_1xbet)
        print(f"le dictionnaire est le {b}")
        v=b.copy()
        v[f"m_home_half_betkeen"]=m_home_half_betkeen
        v[f"m_away_half_betkeen"]=m_away_half_betkeen
        v[f"m_draw_half_betkeen"]=m_draw_half_betkeen
        print(v)
        value={}
        if value_home_half_1xbet:
            value["value_home_half_1xbet"]=value_home_half_1xbet
            value["ecart"]=value_home_half_1xbet-home_half_betkeen
            v["valeur"]=value_home_half_1xbet

        if value_away_half_1xbet:
            value["value_away_half_1xbet"]=value_away_half_1xbet
            value["ecart"]=value_away_half_1xbet-away_half_betkeen
            v["valeur"]=value_away_half_1xbet

        if value_draw_half_1xbet:
            value["value_draw_half_1xbet"]=value_draw_half_1xbet
            value["ecart"]=value_draw_half_1xbet-draw_half_betkeen
            v["valeur"]=value_draw_half_1xbet

        print(value)
        v["valuebet"]=value
        v["last_update"]=time.time()
        if value:

            collection3=db_match_odd["valuebet"]
            if list(collection3.find({'id_half_1xbet': v["id_half_1xbet"],"market":v["market"],"events_1xbet":v["events_1xbet"]},{"_id":0})):
                filtre={'id_half_1xbet': v["id_half_1xbet"],"market":v["market"],"events_1xbet":v["events_1xbet"]}
                mise_a_jour={'$set':  {k: v[k] for k in v if k != 'id'}}
                resultat= collection3.update_one(filtre, mise_a_jour)
                if resultat.modified_count > 0:
                    print("Mise à jour effectuée avec succès.")
                else:
                    print("Aucun document mis à jour.")
            else:
                resultat=collection3.insert_one(v)
                inserted_id = resultat.inserted_id
                print("Identifiant inséré :", inserted_id)



            collection4=db_match_odd["storage"]
            if list(collection4.find({'id_half_1xbet': v["id_half_1xbet"],"market":v["market"],"events_1xbet":v["events_1xbet"]},{"_id":0})):
                filtre={'id_half_1xbet': v["id_half_1xbet"],"market":v["market"],"events_1xbet":v["events_1xbet"]}
                mise_a_jour={'$set':  {k: v[k] for k in v if k != 'id'}}
                resultat= collection4.update_one(filtre, mise_a_jour)
                if resultat.modified_count > 0:
                    print("Mise à jour effectuée avec succès.")
                else:
                    print("Aucun document mis à jour.")
            else:
                resultat=collection4.insert_one(v)
                inserted_id = resultat.inserted_id
                print("Identifiant inséré :", inserted_id)            



    # Ici, on cherche le maximum entre les cotes des deux bookmakers
    if b["home_half_betkeen"] > b["home_half_1xbet"]:
        t["home_half_betkeen"] = b["home_half_betkeen"]
    else:
        t["home_half_1xbet"] = b["home_half_1xbet"]

    if b["away_half_betkeen"] > b["away_half_1xbet"]:
        t["away_half_betkeen"] = b["away_half_betkeen"]
    else:
        t["away_half_1xbet"] = b["away_half_1xbet"]

    if b["draw_half_betkeen"] > b["draw_half_1xbet"]:
        t["draw_half_betkeen"] = b["draw_half_betkeen"]
    else:
        t["draw_half_1xbet"] = b["draw_half_1xbet"]

    inverse_sum = reduce(lambda x, y: x + (1 / y), t.values(), 0)
    print(t)
    print(inverse_sum)
    if inverse_sum < 1:
        b["possible_surebet"] = t
        b["last_update"] = time.time()
        b["ratio"]=inverse_sum
        collection2 = db_match_odd["surebet"]



        
        if list(collection2.find({'id_half_1xbet': b["id_half_1xbet"],"market":b["market"],"events_1xbet":b["events_1xbet"]},{"_id":0})):
            filtre={'id_half_1xbet': b["id_half_1xbet"],"market":b["market"],"events_1xbet":b["events_1xbet"]}
            mise_a_jour={'$set':  {k: b[k] for k in b if k != 'id'}}
            resultat= collection2.update_one(filtre, mise_a_jour)
            if resultat.modified_count > 0:
                print("Mise à jour effectuée avec succès.")
            else:
                print("Aucun document mis à jour.")
        else:
            resultat=collection2.insert_one(b)
            inserted_id = resultat.inserted_id
            print("Identifiant inséré :", inserted_id)
        pprint(list(collection2.find({}, {"_id": 0})))
        last_surebet()









# Fonction asynchrone pour traiter un ensemble de données (lot) avec une taille de lot spécifiée
async def process_data_set(resultat, batch_size, max_concurrent_tasks):
    # Créer un sémaphore pour contrôler le nombre maximum de tâches actives simultanément
    semaphore = asyncio.Semaphore(max_concurrent_tasks)
    # Liste pour stocker les tâches asynchrones
    tasks = []
    # Liste pour stocker le lot courant de données
    current_batch = []

    for data in resultat:
        # Ajouter l'élément de données au lot courant
        current_batch.append(data)
        # Si le lot courant atteint la taille spécifiée
        if len(current_batch) == batch_size:
            # Traiter le lot courant
            await process_batch(current_batch, tasks, semaphore)
            # Réinitialiser le lot courant
            current_batch = []

    # Traiter le dernier lot s'il en reste
    if current_batch:
        await process_batch(current_batch, tasks, semaphore)

    # Attendre la fin de toutes les tâches asynchrones
    await asyncio.gather(*tasks)

# Fonction asynchrone pour traiter un lot de données
async def process_batch(batch, tasks, semaphore):
    # Liste pour stocker les tâches asynchrones du lot
    batch_tasks = []

    for data in batch:
        # Acquérir le sémaphore pour contrôler le nombre maximum de tâches actives simultanément
        await semaphore.acquire()
        # Créer une tâche asynchrone pour traiter l'élément de données
        task = asyncio.create_task(process_data(data, tasks, semaphore))
        # Ajouter la tâche au lot de tâches du lot
        batch_tasks.append(task)

    # Attendre la fin de toutes les tâches du lot
    await asyncio.gather(*batch_tasks)

# Fonction asynchrone pour traiter un élément de données
async def process_data(data, tasks, semaphore):
    try:
        # Appeler la fonction de récupération des cotes d'un match
        await match_odd_recuperation(data)
    except Exception as e:
        # Gérer les exceptions liées au traitement des données
        print(f"Erreur lors du traitement de {data}: {e}")
    finally:
        # Libérer le sémaphore pour permettre à une autre tâche d'être exécutée
        semaphore.release()

# Ensemble de données pour itérer de manière asynchrone

# Taille du lot de données à traiter en une fois
batch_size = 10

# Nombre maximum de tâches actives simultanément
max_concurrent_tasks = 10

# Appel de la fonction asynchrone pour traiter l'ensemble de données
loop = asyncio.get_event_loop()
loop.run_until_complete(process_data_set(resultat, batch_size, max_concurrent_tasks))


client.close()
import gc
gc.collect()

sys.exit()


