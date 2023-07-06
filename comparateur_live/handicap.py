
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

db_handicap=client["finale"]
collection1=db_handicap["handicap"]
data=list(collection1.find({},{"_id":0}))

collection2=db_handicap["surebet"]


collection3=db_handicap["valuebet"]
collection4=db_handicap["storage"]

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
	cinq_minute=time.time()-100
	result = collection3.delete_many({"last_update": {"$lt": cinq_minute}})


import aiohttp
betkeen=''
_1xbet=''
from functools import reduce

async def handicap_Traitement(a, data1, a1, *args, **kwargs):
    t = {}
    b=a.copy()
    #pprint(a1)
    global betkeen
    global _1xbet
    b["betkeen"]=betkeen
    b["1xbet"]=_1xbet
    b["id"]=str(uuid.uuid4())
    print(kwargs.get("home_handicap"))
    print(kwargs.get("away_handicap"))
    home_handicap_betkeen = list(filter(lambda x: x["HandicapMatch"] == kwargs.get("home_handicap"), data1))[0]["Back1Odds"]
    print(home_handicap_betkeen)
    home_id=list(filter(lambda x: x["HandicapMatch"] == kwargs.get("home_handicap"), data1))[0]["SelectionId"]
    away_handicap_betkeen = list(filter(lambda x: x["HandicapMatch"] == kwargs.get("away_handicap"), data1))[0]["Back1Odds"]
    print(away_handicap_betkeen)
    away_id=list(filter(lambda x: x["HandicapMatch"] == kwargs.get("away_handicap"), data1))[0]["SelectionId"]
    
    filtered_list = list(filter(lambda x: x["G"] == kwargs.get("G") and x["T"] == kwargs.get("T_home") and ("P" in x.keys() and x["P"] == kwargs.get("home_handicap")), a1))
    if filtered_list:
        home_handicap_1xbet = filtered_list[0]["C"]
        print(home_handicap_1xbet)
    
    filtered_list = list(filter(lambda x: x["G"] == kwargs.get("G") and x["T"] == kwargs.get("T_away") and ("P" in x.keys() and x["P"] == kwargs.get("away_handicap")) , a1))
    if filtered_list:
        away_handicap_1xbet = filtered_list[0]["C"]
        print(away_handicap_1xbet)


    h=kwargs["home_handicap"]
    a1=kwargs["away_handicap"]
    
    b[f"home_handicap_betkeen {h}"]=home_handicap_betkeen
    b[f"away_handicap_betkeen {a1}"]=away_handicap_betkeen

    b[f"home_handicap_1xbet {h}"]=home_handicap_1xbet
    b[f"away_handicap_1xbet {a1}"]=away_handicap_1xbet
    value_home_handicap_1xbet=""
    value_away_handicap_1xbet=""


    p_home_handicap_betkeen=(1/home_handicap_betkeen)
    p_away_handicap_betkeen=(1/away_handicap_betkeen)
    marge=(p_away_handicap_betkeen+p_home_handicap_betkeen)-1
    if marge<0.08 and home_handicap_betkeen<12 and away_handicap_betkeen<12:
        m_home_handicap_betkeen=(2*home_handicap_betkeen)/(2-marge*home_handicap_betkeen)
        m_away_handicap_betkeen=(2*away_handicap_betkeen)/(2-marge*away_handicap_betkeen)


        if (home_handicap_betkeen>m_home_handicap_betkeen) and ( home_handicap_betkeen - m_home_handicap_betkeen > 0.02):
            value_home_handicap_1xbet=home_handicap_1xbet
            print(value_home_handicap_1xbet)


        if (away_handicap_betkeen>m_away_handicap_betkeen) and ( away_handicap_betkeen - m_away_handicap_betkeen > 0.02):
            value_away_handicap_1xbet=away_handicap_1xbet
            print(value_away_handicap_1xbet)

        print(f"le dictionnaire est le {b}")
        v=b.copy() 
        v[f"m_home_handicap_betkeen {h}".replace(".",",")]=m_home_handicap_betkeen
        v[f"m_away_handicap_betkeen {a1}".replace(".",",")]=m_away_handicap_betkeen

        print(v)
        value={}
        if value_home_handicap_1xbet:
            value[f"value_home_handicap_1xbet {h}".replace(".",",")]=value_home_handicap_1xbet
            value["ecart"]=value_home_handicap_1xbet-home_handicap_betkeen

        if value_away_handicap_1xbet:
            value[f"value_away_handicap_1xbet {a1}".replace(".",",")]=value_away_handicap_1xbet
            value["ecart"]=value_away_handicap_1xbet-away_handicap_betkeen

        if value:
            v["valuebet"]=values
            v["h"]=h
            v["a1"]=a1
            collection3=db_handicap["valuebet"]


            if list(collection3.find({'id_handicap_1xbet': v["id_handicap_1xbet"],"market":v["market"],"events_1xbet":v["events_1xbet"],"a1":v["a1"]},{"_id":0})):
                filtre={'id_handicap_1xbet': v["id_handicap_1xbet"],"market":v["market"],"events_1xbet":v["events_1xbet"],"a1":v["a1"]}
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



            collection4=db_handicap["storage"]


            if list(collection4.find({'id_handicap_1xbet': v["id_handicap_1xbet"],"market":v["market"],"events_1xbet":v["events_1xbet"],"a1":v["a1"]},{"_id":0})):
                filtre={'id_handicap_1xbet': v["id_handicap_1xbet"],"market":v["market"],"events_1xbet":v["events_1xbet"],"a1":v["a1"]}
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





    if b[f"home_handicap_betkeen {h}"] > b[f"home_handicap_1xbet {h}"]:
        t[f"home_handicap_betkeen {h}"] = b[f"home_handicap_betkeen {h}"]
    else:
        t[f"home_handicap_1xbet {h}"] = b[f"home_handicap_1xbet {h}"]

    if b[f"away_handicap_betkeen {a1}"] > b[f"away_handicap_1xbet {a1}"]:
        t[f"away_handicap_betkeen {a1}"] = b[f"away_handicap_betkeen {a1}"]
    else:
        t[f"away_handicap_1xbet {a1}"] = b[f"away_handicap_1xbet {a1}"]
    b["h"]=h
    b["a1"]=a1

    inverse_sum = reduce(lambda x, y: x + (1 / y), t.values(), 0)
    print(t,inverse_sum)
    if inverse_sum<1:
        b["possible_surebet"]=t
        b["last_update"]=time.time()
        b["ratio"]=inverse_sum
        collection2=db_handicap["surebet"]


        if list(collection2.find({'id_handicap_1xbet': v["id_handicap_1xbet"],"market":v["market"],"events_1xbet":v["events_1xbet"],"a1":v["a1"]},{"_id":0})):
            filtre={'id_handicap_1xbet': v["id_handicap_1xbet"],"market":v["market"],"events_1xbet":v["events_1xbet"],"a1":v["a1"]}
            mise_a_jour={'$set':  {k: v[k] for k in v if k != 'id'}}
            resultat= collection2.update_one(filtre, mise_a_jour)
            if resultat.modified_count > 0:
                print("Mise à jour effectuée avec succès.")
            else:
                print("Aucun document mis à jour.")
        else:
            resultat=collection2.insert_one(v)
            inserted_id = resultat.inserted_id
            print("Identifiant inséré :", inserted_id)




        collection6=db_handicap["storage surebet"]


        if list(collection6.find({'id_handicap_1xbet': v["id_handicap_1xbet"],"market":v["market"],"events_1xbet":v["events_1xbet"],"a1":v["a1"]},{"_id":0})):
            filtre={'id_handicap_1xbet': v["id_handicap_1xbet"],"market":v["market"],"events_1xbet":v["events_1xbet"],"a1":v["a1"]}
            mise_a_jour={'$set':  {k: v[k] for k in v if k != 'id'}}
            resultat= collection6.update_one(filtre, mise_a_jour)
            if resultat.modified_count > 0:
                print("Mise à jour effectuée avec succès.")
            else:
                print("Aucun document mis à jour.")
        else:
            resultat=collection6.insert_one(v)
            inserted_id = resultat.inserted_id
            print("Identifiant inséré :", inserted_id)
        pprint(list(collection2.find({},{"_id":0})))


#handicap_traitement(home_handicap=-4,away_handicap=4,G=3,T_home=7,T_away=8)
'''
async def handicap_recuperation(a):
    Id = a["id_handicap_1xbet"]
    # Le lien ici est pour les matchs en direct (liveFeed)
    url = f"https://1xbet.mobi/LiveFeed/GetGameZip?id={Id}&lng=fr&tzo=2&isSubGames=true&GroupEvents=true&countevents=250&grMode=2&country=182&marketType=1&mobi=true"
    data=await fetch(url)


    Id1=a["id_handicap_betkeen"]
    url1=f"https://mob.easysport.bet/Home/GetUpdateForm/?isaustralien=true&marketid={Id1}"
    data1= await fetch_data(url1)
    data1=data1["Selections"]
    print(data1)
    t={}
    a1=[list(x.values()) for  x in data["Value"]["GE"]]
    a1=flatten(a1)
    a1= [elem for elem in a1 if isinstance(elem, dict)]
    print(a1)
    #handicap_Traitement(a,data1,a1,home_handicap=-1.5,away_handicap=1.5,G=3,T_home=7,T_away=8)

'''


async def handicap_recuperation(a):

    global betkeen
    global _1xbet
    Id = a["id_handicap_1xbet"]
    # Le lien ici est pour les matchs en direct (liveFeed)
    url = f"https://1xbet.mobi/LiveFeed/GetGameZip?id={Id}&lng=fr&tzo=2&isSubGames=true&GroupEvents=true&countevents=250&grMode=2&country=182&marketType=1&mobi=true"
    try:
        data=await fetch(url)
    except Exception as e:
        print(f"probleme {e} au niveau de l api 1xbet")



    Id1=a["id_handicap_betkeen"]
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
    data1=data1["Selections"]
    if data1==[]:
        print("il n y a de data au niveau de l'api betkeen"  )
        return None
    #print(data1)
    t={}
    try:
        a1=[list(x.values()) for  x in data["Value"]["GE"]]
    except Exception as e:
        print(f"le probleme {e} est survenu au niveau de <<a1=[list(x.values()) for x in data['Value']['GE']]>>")
        return None
    a1=flatten(a1)
    a1= [elem for elem in a1 if isinstance(elem, dict)]
    #pprint(a1)
    try:
        await handicap_Traitement(a,data1,a1,home_handicap=-1,away_handicap=1,G=3,T_home= 7,T_away= 8)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1[len(data1)//2:],a1,home_handicap=1,away_handicap=-1,G=3,T_home= 7,T_away= 8)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")

    
    try:
        await handicap_Traitement(a,data1,a1,home_handicap=0,away_handicap=0,G=3,T_home= 7,T_away= 8)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1,a1,home_handicap=-1.5,away_handicap=1.5,G=3,T_home= 7,T_away= 8)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")

    try:
        await handicap_Traitement(a,data1[len(data1)//2:],a1,home_handicap=1.5,away_handicap=-1.5,G=3,T_home= 7,T_away= 8)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    

    try:
        await handicap_Traitement(a,data1,a1,home_handicap=-2,away_handicap=2,G=3,T_home= 7,T_away= 8)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1[len(data1)//2:],a1,home_handicap=2,away_handicap=-2,G=3,T_home= 7,T_away= 8)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1,a1,home_handicap=-2.5,away_handicap=2.5,G=3,T_home= 7,T_away= 8)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1[len(data1)//2:],a1,home_handicap=2.5,away_handicap=-2.5,G=3,T_home= 7,T_away= 8)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1,a1,home_handicap=-3,away_handicap=3,G=3,T_home= 7,T_away= 8)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1[len(data1)//2:],a1,home_handicap=3,away_handicap=-3,G=3,T_home= 7,T_away= 8)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1,a1,home_handicap=-3.5,away_handicap=3.5,G=3,T_home= 7,T_away= 8)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1[len(data1)//2:],a1,home_handicap=3.5,away_handicap=-3.5,G=3,T_home= 7,T_away= 8)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1,a1,home_handicap=-4,away_handicap=4,G=3,T_home= 7,T_away= 8)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1[len(data1)//2:],a1,home_handicap=4,away_handicap=-4,G=3,T_home= 7,T_away= 8)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")



    try:
        await handicap_Traitement(a,data1,a1,home_handicap=-1.25,away_handicap=1.25,G=1008,T_home= 3829,T_away= 3830)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1[len(data1)//2:],a1,home_handicap=1.25,away_handicap=-1.25,G=1008,T_home= 3829,T_away= 3830)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")

    try:
        await handicap_Traitement(a,data1,a1,home_handicap=-0.5,away_handicap=0.5,G=3,T_home= 7,T_away= 8)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1[len(data1)//2:],a1,home_handicap=0.5,away_handicap=-0.5,G=3,T_home= 7,T_away= 8)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")


    try:
        await handicap_Traitement(a,data1,a1,home_handicap=-0.25,away_handicap=0.25,G=1008,T_home= 3829,T_away= 3830)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1[len(data1)//2:],a1,home_handicap=0.25,away_handicap=-0.25,G=1008,T_home= 3829,T_away= 3830)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")


    try:
        await handicap_Traitement(a,data1,a1,home_handicap=-0.75,away_handicap=0.75,G=1008,T_home= 3829,T_away= 3830)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1[len(data1)//2:],a1,home_handicap=0.75,away_handicap=-0.75,G=1008,T_home= 3829,T_away= 3830)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")


    try:
        await handicap_Traitement(a,data1,a1,home_handicap=-1.25,away_handicap=1.25,G=1008,T_home= 3829,T_away= 3830)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1[len(data1)//2:],a1,home_handicap=1.25,away_handicap=-1.25,G=1008,T_home= 3829,T_away= 3830)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")


    try:
        await handicap_Traitement(a,data1,a1,home_handicap=-1.75,away_handicap=1.75,G=1008,T_home= 3829,T_away= 3830)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1[len(data1)//2:],a1,home_handicap=1.75,away_handicap=-1.75,G=1008,T_home= 3829,T_away= 3830)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")


    try:
        await handicap_Traitement(a,data1,a1,home_handicap=-0.25,away_handicap=0.25,G=1008,T_home= 3829,T_away= 3830)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1[len(data1)//2:],a1,home_handicap=0.25,away_handicap=-0.25,G=1008,T_home= 3829,T_away= 3830)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")


    try:
        await handicap_Traitement(a,data1,a1,home_handicap=-2.75,away_handicap=2.75,G=1008,T_home= 3829,T_away= 3830)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1[len(data1)//2:],a1,home_handicap=2.75,away_handicap=-2.75,G=1008,T_home= 3829,T_away= 3830)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")


    try:
        await handicap_Traitement(a,data1,a1,home_handicap=-3.25,away_handicap=3.25,G=1008,T_home= 3829,T_away= 3830)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1[len(data1)//2:],a1,home_handicap=3.25,away_handicap=-3.25,G=1008,T_home= 3829,T_away= 3830)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")


    try:
        await handicap_Traitement(a,data1,a1,home_handicap=-3.75,away_handicap=3.75,G=1008,T_home= 3829,T_away= 3830)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")
    try:
        await handicap_Traitement(a,data1[len(data1)//2:],a1,home_handicap=3.75,away_handicap=-3.75,G=1008,T_home= 3829,T_away= 3830)

    except Exception as e :
        print(f"l erreur {e} est survenue lors de l execution de handicap_traitement")

















#asyncio.run(handicap_recuperation(resultat[3]))














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
        await handicap_recuperation(data)
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
