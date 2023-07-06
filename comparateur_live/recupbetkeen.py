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
import itertools
from pprint import pprint
import json
import pymongo
import httpx
import requests
from datetime import datetime
import pickle

import sys
#sys.stdout = open("NUL", "w")

import subprocess
subprocess.run(['python3', 'cookiebetkeen.py'])
def timestamp(x):
    # Convertir la date en format datetime
    x=x.replace(":"," ")
    day, month, year, hour, minute = x.split()
     
    month_num = {
         
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "juil.": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
    }
    month = month_num[month]
    date_obj = datetime(int(year), month, int(day), int(hour), int(minute))
 
    # Convertir la date en timestamp
    timestamp = int(date_obj.timestamp())+7200
    return timestamp


def replace_i_display_length(url):
    # Recherche le paramètre "iDisplayLength" dans l'URL
    old_value = "iDisplayLength=200"
    old_value1 = "iDisplayLength=500"
    new_value = "iDisplayLength=9000"
    if old_value in url:
        new_url = url.replace(old_value, new_value)

    elif old_value1 in url:
        new_url=url.replace(old_value1, new_value) 
        return new_url
    else:
        return url






contenu=''
with open('fichierajax.txt', "r") as fichier:
    contenu=str(fichier.read())
# URL de la requête
url = str(replace_i_display_length(contenu))

print(url)

client = pymongo.MongoClient("mongodb://localhost:27017/")
db=client["info_betkeen"]
#collection= db["cookie_desktop"]
#collection1=db["cookie_mobile"]
con=db["liste_match_betkeen_live"]

c=client.info_betkeen.collection
#__r=c.find()

__r=c.find({"name":"__RequestVerificationToken_Lw__"},{"value":1,"_id":0})
aspnet=c.find({"name":"ASP.NET_SessionId"},{"value":1,"_id":0})
#print(list(aspnet)[0]["value"])
ASPXAUTH=c.find({"name":".ASPXAUTH"},{"value":1,"_id":0})
#print(list(ASPXAUTH)[0]["value"])
#print(list(__r)[0]["value"])
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
print(headers)

response = requests.get(url, headers=headers)

# Vérifier le code de statut de la réponse

#print(response.content)
# Récupérer le corps de la réponse décompressé et décodé
content = response.content.decode("utf-8")
#print(content)

# Utiliser le contenu de la réponse pour vos besoins
content=json.loads(content)
#content=list(map(lambda x: x[1].split("\\"), content))

#print(content)
timestamp_now = datetime.timestamp(datetime.now())
print(timestamp_now)

h1=["I","S","1","5","4","L","events","market"]
def normal(content):
    for k,i in enumerate(content):
        j=i[1].split("\\")
        for h in j:
            i.append(h)
        i.pop(1)    
        #i=list(itertools.chain.from_iterable(i))
        content[k]=dict(zip(h1,i))
    return content    
valeur=normal(content["aaData"])

#valeur =[x for x in valeur if timestamp(x["S"])<timestamp_now or timestamp(x["S"])<timestamp_now+660]
valeur =[x for x in valeur if (timestamp(x["S"])<timestamp_now or timestamp(x["S"])<timestamp_now+660) and timestamp_now<timestamp(x["S"])+7200]
#print(valeur)
print((valeur))

# stocker la liste des match dans la base de donne liste_match_betkeen
s=db.con.delete_many({})
x=db.con.insert_one({"events":valeur})
import subprocess 
subprocess.run(['python3', 'donnee.py'])
subprocess.run(['python3', 'traitement.py'])

client.close()





import gc
gc.collect()

sys.exit()
