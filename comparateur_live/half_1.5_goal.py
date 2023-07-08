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
import aiohttp
from functools import reduce
import uuid
import sys
#sys.stdout = open("NUL", "w")



client=pymongo.MongoClient('localhost',27017)
db=client["bet_live"]


contenu=''




db=client["info_betkeen"]
#collection= db["cookie_desktop"]
#collection1=db["cookie_mobile"]
con=db["liste_match_betkeen_live"]

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

db_over_under=client["finale"]
collection1=db_over_under["First Half Goals 1.5"]
data=list(collection1.find({},{"_id":0}))

collection2=db_over_under["surebet"]

collection3=db_over_under["valuebet"]
collection4=db_over_under["storage"]
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
            if response.status == 200:
                return await response.json()

def flatten(l):
    for item in l:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item
#cette fonction sert a supprimer les surebet qui on 5minut d exitant sans etre updater
def last_surebet():
    cinq_minute=time.time()-300
    result = collection2.delete_many({"last_update": {"$lt": cinq_minute}})

def last_surebet1():
    cinq_minute=time.time()-300
    result = collection3.delete_many({"last_update": {"$lt": cinq_minute}})

betkeen=''
_1xbet=''
async def over_under_traitement(lien,lien1,unxbet,ligue,a,data1,a1,*args,**kwargs):
    global betkeen
    global _1xbet
    last_surebet()
    last_surebet1()
    t={}
    #print(data1)
    #print(a1)
    goal=kwargs["goal"]
    b=[]
    b=a.copy()
    #print(goal)
    b["lien"]=lien
    b["lien1"]=lien1
    b["unxbet"]=unxbet
    b["ligue"]=ligue
    b["LI"]=LI
    b["betkeen"]=betkeen
    b["1xbet"]=_1xbet
    b["id"]=str(uuid.uuid4())
    over_betkeen=list(filter(lambda x: x["SelectionName"]==f"Over {goal} Goals",data1))[0]["Back1Odds"]
    under_betkeen=list(filter(lambda x: x["SelectionName"]==f"Under {goal} Goals",data1))[0]["Back1Odds"]
    




    over_1xbet=list(filter(lambda x: x["G"]==kwargs["G"] and x["T"]==kwargs["over_T"] and x["P"]==kwargs["goal"],a1))[0]["C"]
    under_1xbet=list(filter(lambda x: x["G"]==kwargs["G"] and x["T"]==kwargs["under_T"] and x["P"]==kwargs["goal"],a1))[0]["C"]

    b[f"over_half_betkeen {goal}".replace(".",",")]=over_betkeen
    b[f"under_half_betkeen {goal}".replace(".",",")]=under_betkeen

    b[f"over_half_1xbet {goal}".replace(".",",")]=over_1xbet
    b[f"under_half_1xbet {goal}".replace(".",",")]=under_1xbet
    
    value_over_1xbet=""
    value_under_1xbet=""

    p_over_betkeen = (1 / over_betkeen) 
    p_under_betkeen = (1 / under_betkeen) 
    marge =  (p_under_betkeen + p_over_betkeen)-1
    if marge <0.07 and over_betkeen<9 and under_betkeen<9:
        m_over_betkeen = (2 * over_betkeen) / (2 - marge * over_betkeen)
        m_under_betkeen = (2 * under_betkeen) / (2 - marge * under_betkeen)

        if (over_1xbet > m_over_betkeen) and (over_1xbet - m_over_betkeen > 0.02):
            value_over_1xbet = over_1xbet
            print(value_over_1xbet)

        if (under_1xbet > m_under_betkeen) and (under_1xbet - m_under_betkeen) > 0.02:
            value_under_1xbet = under_1xbet
            print(value_under_1xbet)

        


        print(f"le dictionnaire est le {b}")
        v=b.copy()
        v[f"m_over_half_betkeen {goal}".replace(".",",")]=m_over_betkeen
        v[f"m_under_half_betkeen {goal}".replace(".",",")]=m_under_betkeen
        print(v)
        value={}
        if value_over_1xbet:
            value[f"value_over_half_1xbet {goal}".replace(".",",")]=value_over_1xbet
            value["ecart"]=value_over_1xbet-over_betkeen
        if value_under_1xbet:
            value[f"value_under_half_1xbet {goal}".replace(".",",")]=value_under_1xbet
            value["ecart"]=value_under_1xbet-under_betkeen
        if value:
            v["valuebet"]=value
            v["but"]=goal
            v["last_update"]=time.time()


            collection3=db_over_under["valuebet"]
            if list(collection3.find({'id_half_1_5_1xbet': v["id_half_1_5_1xbet"],"market":v["market"],"events_1xbet":v["events_1xbet"],"but":v["but"]},{"_id":0})):
                filtre={'id_half_1_5_1xbet': v["id_half_1_5_1xbet"],"market":v["market"],"events_1xbet":v["events_1xbet"],"but":v["but"]}
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


            collection4=db_over_under["storage"]
            if list(collection4.find({'id_half_1_5_1xbet': v["id_half_1_5_1xbet"],"market":v["market"],"events_1xbet":v["events_1xbet"],"but":v["but"]},{"_id":0})):
                filtre={'id_half_1_5_1xbet': v["id_half_1_5_1xbet"],"market":v["market"],"events_1xbet":v["events_1xbet"],"but":v["but"]}
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






    b["but"]=goal
    if b[f"over_half_betkeen {goal}".replace(".",",")] > b[f"over_half_1xbet {goal}".replace(".",",")]:
        t[f"over_half_betkeen {goal}".replace(".",",")] = b[f"over_half_betkeen {goal}".replace(".",",")]
    else:
        t[f"over_half_1xbet {goal}".replace(".",",")] = b[f"over_half_1xbet {goal}".replace(".",",")]

    if b[f"under_half_betkeen {goal}".replace(".",",")] > b[f"under_half_1xbet {goal}".replace(".",",")]:
        t[f"under_half_betkeen {goal}".replace(".",",")] = b[f"under_half_betkeen {goal}".replace(".",",")]
    else:
        t[f"under_half_1xbet {goal}".replace(".",",")] = b[f"under_half_1xbet {goal}".replace(".",",")]


    inverse_sum = reduce(lambda x, y: x + (1 / y), t.values(), 0)
    print(t,inverse_sum)

    if inverse_sum<1:
        b["possible_surebet"]=t
        b["last_update"]=time.time()
        b["ratio"]=inverse_sum
        collection2=db_over_under["surebet"]


        collection2=db_over_under["surebet"]
        if list(collection2.find({'id_half_1_5_1xbet': b["id_half_1_5_1xbet"],"market":b["market"],"events_1xbet":b["events_1xbet"],"but":b["but"]},{"_id":0})):
            filtre={'id_half_1_5_1xbet': b["id_half_1_5_1xbet"],"market":b["market"],"events_1xbet":b["events_1xbet"],"but":b["but"]}
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




        collection6=db_over_under["storage surebet"]
        if list(collection6.find({'id_half_1_5_1xbet': b["id_half_1_5_1xbet"],"market":b["market"],"events_1xbet":b["events_1xbet"],"but":b["but"]},{"_id":0})):
            filtre={'id_half_1_5_1xbet': b["id_half_1_5_1xbet"],"market":b["market"],"events_1xbet":b["events_1xbet"],"but":b["but"]}
            mise_a_jour={'$set':  {k: b[k] for k in b if k != 'id'}}
            resultat= collection6.update_one(filtre, mise_a_jour)
            if resultat.modified_count > 0:
                print("Mise à jour effectuée avec succès.")
            else:
                print("Aucun document mis à jour.")
        else:
            resultat=collection6.insert_one(b)
            inserted_id = resultat.inserted_id
            print("Identifiant inséré :", inserted_id)
        pprint(list(collection2.find({},{"_id":0})))



#over_under_traitement(goal=0.5,G=4,over_T=9,under_T=10)


#over_under_traitement(home_handicap=-4,away_handicap=4,G=3,T_home=7,T_away=8)
async def over_under_recuperation(a):
    global betkeen
    global _1xbet
    Id = a["id_half_1_5_1xbet"]
    # Le lien ici est pour les matchs en direct (liveFeed)
    url = f"https://1xbet.mobi/LiveFeed/GetGameZip?id={Id}&lng=fr&tzo=2&isSubGames=true&GroupEvents=true&countevents=2500&grMode=2&country=182&marketType=1&mobi=true"
    try:
        data=await fetch(url)
    except Exception as e:
        print(f"probleme {e} au niveau de l api 1xbet")



    Id1=a["id_half_1_5_betkeen"]
    url1=f"https://mob.easysport.bet/Home/GetUpdateForm/?isaustralien=true&marketid={Id1}"
    try:
        data1= await fetch_data(url1)
    except Exception as e:
        print(f'Probleme {e} au niveau de l api betkeen')
        return None
    betkeen=data1["EventMarket"]
    O1=data["Value"]["O1"]
    O2=data["Value"]["O2"]
    _1xbet=f"{O1} v {O2}"
    
    unxbet=f"{O1} {O2}".replace(" ","-")
    ligue=data["Value"]["LE"].replace(" ","-").replace(".","")
    LI=data["Value"]["LI"]
    lien=f"https://1xbet.mobi/fr/live/football/{LI}-{ligue}/{Id}-{unxbet}"
    print(lien)
    lien1=f"https://desk.easysport.bet/Home/FormBet/{Id1}"
    data1=data1["Selections"]
    if data1==[]:
        print("il n y a de data au niveau de l'api betkeen"  )
        return None
    #print(data1)
    t={}
    try:
        a1=[list(x.values()) for  x in data["Value"]["SG"][0]["GE"]]
    except Exception as e:
        print(f"le probleme {e} est survenu au niveau de <<a1=[list(x.values()) for x in data['Value']['GE']]>>")
        return None
    a1=flatten(a1)
    a1= [elem for elem in a1 if isinstance(elem, dict)]
    #print(a1)


    try:
        await over_under_traitement(lien,lien1,unxbet,ligue,LI,a,data1,a1,goal=1.5,G=4,over_T=9,under_T=10)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de over_under_traitement")
    
#asyncio.run(over_under_recuperation(resultat[10]))






#asyncio.run(over_under_recuperation(resultat[1]))
#asyncio.run(over_under_recuperation(resultat[0]))





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
        await over_under_recuperation(data)
    except Exception as e:
        # Gérer les exceptions liées au traitement des données
        print(f"Erreur lors du traitement de {data}: {e}")
    finally:
        # Libérer le sémaphore pour permettre à une autre tâche d'être exécutée
        semaphore.release()

# Ensemble de données pour itérer de manière asynchrone

# Taille du lot de données à traiter en une fois
batch_size = 20

# Nombre maximum de tâches actives simultanément
max_concurrent_tasks = 20

# Appel de la fonction asynchrone pour traiter l'ensemble de données
loop = asyncio.get_event_loop()
loop.run_until_complete(process_data_set(resultat, batch_size, max_concurrent_tasks))


client.close()

import gc
gc.collect()

sys.exit()
