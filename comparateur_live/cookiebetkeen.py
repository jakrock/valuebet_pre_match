import asyncio
import time
from pprint import pprint
import json
import pymongo
import pickle

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.keys import Keys
import time


from selenium.webdriver.common.proxy import Proxy, ProxyType


from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import re
#from google.cloud import firestore

# Initialisez une instance du client Firestore
#db = firestore.Client()





client = pymongo.MongoClient("mongodb://localhost:27017/")
db=client["info_betkeen"]
collection= db["cookie_desktop"]
collection1=db["cookie_mobile"]

service1=Service(ChromeDriverManager().install())
option = webdriver.ChromeOptions()
option.add_argument("--headless")  # Exécution en mode headless pour éviter l'affichage du navigateur
browser = webdriver.Chrome(service=service1, options=option)
url = "https://desk.easysport.bet/Account/LogIn?ReturnUrl=%2fHome%2fbetfair"
browser.execute_script("window.performance.setResourceTimingBufferSize(10000);")    

browser.get(url)

wait = WebDriverWait(browser, 50)

username = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='UserName']")))
username.send_keys("jakrock50")
password = browser.find_element(By.XPATH, "//input[@id='Password']")
password.send_keys("hubertine50")
connect = browser.find_element(By.XPATH, "//button[@class='btn btn-primary my-15']")
connect.click()



soccerListing = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'/home/sports/1')]")))
soccerListing.click()
soccerListing1 = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='example_info']"))).text


rows = browser.find_element(By.XPATH, "//select[@name='example_length']")
select = Select(rows)
select.select_by_value("500")
time.sleep(7)

#browser.execute_script("window.performance.setResourceTimingBufferSize(2000);")

log_entries = browser.execute_script("return window.performance.getEntries();")

# Parcourir les entrées du journal
for entry in log_entries:
    # Vérifier si l'entrée est une requête HTTP
    if entry['entryType'] == 'resource':
        # Récupérer le lien de la requête
        url = entry['name']
        #print(url



performance_data = browser.execute_script("return window.performance.getEntriesByType('resource');")

for entry in performance_data:
    url = entry['name']


    if "https://desk.easysport.bet/Home/AjaxHandlerSport" in url:
    	with open('fichierajax.txt', "w") as fichier:
    		fichier.write(url)



    print("URL : ", url)
    print("Paramètres : ", entry['initiatorType'])
    print("URL : ", url)
    print("Paramètres : ", entry['initiatorType'])



cookies = browser.get_cookies()

#print(cookies)
with open("keen.deskto.json","w") as f:
	json.dump(cookies,f)
b=db.collection.delete_many({})
a=db.collection.insert_many(cookies)	

#print(list(db.collection.find({"name":".ASPXAUTH"})))

#print(cookies)
time.sleep(7)
browser.quit()






option = webdriver.ChromeOptions()
option.add_argument("--headless")  # Exécution en mode headless pour éviter l'affichage du navigateur
browser = webdriver.Chrome(service=service1, options=option)
url = "https://mob.easysport.bet/Account/Login"
    

browser.get(url)

wait = WebDriverWait(browser, 50)

username = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='UserName']")))
username.send_keys("jakrock50")
password = browser.find_element(By.XPATH, "//input[@id='Password']")
password.send_keys("hubertine50")
connect = browser.find_element(By.XPATH, "//input[@class='btn btn-main btn-lg btn-block']")
connect.click()


soccerListing = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='btn btn-success btn-sm btn-block']")))
soccerListing.click()

log_entries = browser.execute_script("return window.performance.getEntries();")

# Parcourir les entrées du journal
for entry in log_entries:
    # Vérifier si l'entrée est une requête HTTP
    if entry['entryType'] == 'resource':
        # Récupérer le lien de la requête
        url = entry['name']
        #print(url)

performance_data = browser.execute_script("return window.performance.getEntriesByType('resource');")


for entry in performance_data:
    url = entry['name']

    if "https://desk.easysport.bet/Home/AjaxHandlerSport" in url:
    	with open('fichierajax1.txt', "w") as fichier:
    		fichier.write(url)
    print("URL : ", url)
    print("Paramètres : ", entry['initiatorType'])


cookies = browser.get_cookies()

pprint(cookies)
with open("keen.mobil.json","w") as f:
	json.dump(cookies,f)

b=db.collection1.delete_many({})
a=db.collection1.insert_many(cookies)	

print(list(db.collection.find({"name":".ASPXAUTH"})))

#print(cookies)
time.sleep(7)
browser.quit()

'''
with open('nbrerow.pickle', 'wb') as f:
    pickle.dump(recuperer_chiffre(soccerListing1), f)
'''
client.close()







