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

import itertools


timestamp = datetime.timestamp(datetime.now())



conn = sqlite3.connect('database.db')
cursor = conn.cursor()

'''
df=pd.read_csv("data1x2.csv")
dict_df = df.to_dict('records')
a=dict_df[50]
print(a)
'''



import httpx
#cette requete sert a recurterer toute les donne de la base de donnee
#les donnee recupere son t des dictionnaire contenant l id,l identifiant de match de 1xbet et betkeen l heure ect ....
from sqlite_utils import Database
db = Database("database.db")
resultat1=list(db["id_1x2general_pre_match"].rows)



client=pymongo.MongoClient('localhost',27017)
db=client["bet_live"]
collection=db["1x2_live"]




contenu=''



client = pymongo.MongoClient("mongodb://localhost:27017/")
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

def fill_betkeen(a):
    Id=a["id_1x2_betkeen"]
    url=f"https://mob.easysport.bet/Home/GetUpdateForm/?isaustralien=false&marketid={Id}&modegame=Gambling"
    response = requests.get(url ,headers=headers)
    print(response)
    r3=[]
    # Vérifier si la réponse est valide (code de réponse 200)
    if response.status_code == 200:
        # Transformer la réponse en JSON
        data=response.json()["Selections"]
        r3.append({"domicile":data[0]["Back1Odds"]})
        r3.append({"draw":data[2]["Back1Odds"]})
        r3.append({"exterieur":data[1]["Back1Odds"]})
        #print(r3[0]["domicile"])
        query=f'''INSERT OR REPLACE INTO odd_1x2_betkeen (id_pre_match ,domicile,exterieur,draw,heure_debut)VALUES ({a["id"]},{r3[0]["domicile"]},{r3[2]["exterieur"]},{r3[1]["draw"]},{a["heure_debut"]});'''
        cursor.execute(query)
        conn.commit()               
        
    if response.status_code == 302:
        new_url = response.headers['Location']
        print(f'La nouvelle URL est : {new_url}')
        
#for i in resultat1:
    #fill_betkeen(i)


async def fetch_data(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url,headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            response.raise_for_status()




async def fetch_betkeen(url):
    async with httpx.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            
            if response.status == 200:
                data= response.json()
                print("haaa")
            else:
                response.raise_for_status()
                print("hooo")
async def process_url_betkeen(a):
    Id=a["id_1x2_betkeen"]
    url=f"https://mob.easysport.bet/Home/GetUpdateForm/?isaustralien=false&marketid={Id}&modegame=Gambling"
    r3=[]
    try:
        data= await fetch_data(url)
        data=data["Selections"]
        r3.append({"domicile":data[0]["Back1Odds"]})
        r3.append({"draw":data[2]["Back1Odds"]})
        r3.append({"exterieur":data[1]["Back1Odds"]})
        #print(r3[0]["domicile"])
    except Exception as e:
        print(f"le code est {e}")    
        return None
    query=f'''INSERT OR REPLACE INTO odd_1x2_betkeen (id_pre_match ,domicile,exterieur,draw,heure_debut)VALUES ({a["id"]},{r3[0]["domicile"]},{r3[2]["exterieur"]},{r3[1]["draw"]},{a["heure_debut"]});'''
    cursor.execute(query)
    conn.commit()

#loop = asyncio.get_event_loop()
beg = time.time()
#loop.run_until_complete(process_url_betkeen(resultat1[0]))
async def fetch_urls_betkeen(data):
    y=await asyncio.gather(*(process_url_betkeen(a) for a in data)) 
    loop = asyncio.get_event_loop()
    beg = time.time()
    loop.run_until_complete(y)
async def process_final(resultat1):

    taille_lot=8
    lot=[resultat1[i : i+taille_lot] for i in range(0,len(resultat1),taille_lot)]
    n=0
    while n<len(lot):
        try:
            await fetch_urls_betkeen(lot[n])
        except Exception as e:
            
            #print(f"l erreur es au niveau de fetch_urls_betkeen{e}")
            pass 
        n+=1
        await asyncio.sleep(0.5)

loop = asyncio.get_event_loop()
beg = time.time()
loop.run_until_complete(process_final(resultat1))

print(len(resultat1))






#permet d aplatir la liste imbriquer dans le contenu values.GE de la reponse 1xbet

def flatten(l):
    for item in l:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item
#cette fonction sert a assigner les cote au evenement possible quand on les aura recuperer par 'G'
def func1(a):
    d=[]
    for i in range(len(a)):
        if i==0:
            d.append({"domicile":a[i]["C"]})
        elif i==1:
            d.append({"draw":a[i]["C"]})
        elif i==2:
            d.append({"exterieur":a[i]["C"]})
    return d



def fill11(a):
    Id = a["id_1x2_1xbet"]
    url = f"https://1xbet.mobi/LiveFeed/GetGameZip?id={Id}&lng=fr&tzo=2&isSubGames=true&GroupEvents=true&countevents=50&grMode=2&country=182&marketType=1&mobi=true"
    # Envoyer la requête HTTP GET
    response = httpx.get(url)

    # Vérifier si la réponse est valide (code de réponse 200)
    if response.status_code == 200:
        # Transformer la réponse en JSON
        data = response.json()
        print(data)
        # Afficher le contenu du JSON
        #pprint(data["Value"]["GE"])#["E"])
        a1=[list(x.values()) for  x in data["Value"]["GE"]]
        a1=list(flatten(a1))
        a1= [elem for elem in a1 if isinstance(elem, dict)]
        pprint(a1)
        r=collection.delete_many({})
        r1=collection.insert_many(a1)
        r2 = collection.find({"G":1},{"C":1 ,"_id":0,})
        r3=func1(list(r2))
        print(r3[0]["domicile"])
        query=f'''INSERT OR REPLACE INTO odd_1x2_1xbet (id_pre_match, domicile,exterieur,draw,heure_debut)VALUES ({a["id"]}, {r3[0]["domicile"]},{r3[2]["exterieur"]},{r3[1]["draw"]},{a["heure_debut"]});'''
        cursor.execute(query)
        conn.commit()

        print('La requête a échoué avec le code de réponse :', response.status_code)

#bet keen
#fill11(resultat1[0])

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()


async def process_url (a):
    Id = a["id_1x2_1xbet"]
    #le lien ic est in liveFeed pour les macht en live 
    url = f"https://1xbet.mobi/LiveFeed/GetGameZip?id={Id}&lng=fr&tzo=2&isSubGames=true&GroupEvents=true&countevents=50&grMode=2&country=182&marketType=1&mobi=true"
    # Envoyer la requête HTTP GET
    data = await fetch(url)
    if data:
        try:
            a1=[list(x.values()) for  x in data["Value"]["GE"]]
        except Exception as e:
            #print(e)
            return None
        a1=list(flatten(a1))
        a1= [elem for elem in a1 if isinstance(elem, dict)]
        #pprint(a1)
        r=  collection.delete_many({})
        r1=  collection.insert_many(a1)
        r2 = collection.find({"G":1},{"C":1 ,"_id":0,})
        r3=func1(list(r2))
        print(r3[0]["domicile"])
        query=f'''INSERT OR REPLACE INTO odd_1x2_1xbet (id_pre_match, domicile,exterieur,draw,heure_debut)VALUES ({a["id"]}, {r3[0]["domicile"]},{r3[2]["exterieur"]},{r3[1]["draw"]},{a["heure_debut"]});'''
        cursor.execute(query)
        conn.commit()
    else:
        return None



#loop = asyncio.get_event_loop()
beg = time.time()
#loop.run_until_complete(process_url(resultat1[1]))
async def fetch_urls(data):
    y=await asyncio.gather(*(process_url(a) for a in data)) 
    loop = asyncio.get_event_loop()
    beg = time.time()
    loop.run_until_complete(y) 

async def process_final(resultat1):
    taille_lot=8
    lot=[resultat1[i : i+taille_lot] for i in range(0,len(resultat1),taille_lot)]
    n=0
    while n<len(lot):
        try:
           await fetch_urls(lot[n])
        except Exception as e:
            
            print(e)
            pass 
        n+=1
        await asyncio.sleep(0.5)
loop = asyncio.get_event_loop()
beg = time.time()
loop.run_until_complete(process_final(resultat1))




client.close()
