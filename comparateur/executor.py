import threading
from apscheduler.schedulers.background import BackgroundScheduler
import time 
import subprocess

import sys
#sys.stdout = open("NUL", "w")

def task1():
    print("Exécution de la tâche 1")
    subprocess.run(['python3', 'recup1xbet.py'])

def task2():
    print("Exécution de la tâche 2")
    subprocess.run(['python3', 'recupbetkeen.py'])
    

def main():
    # Créez un planificateur en arrière-plan
    scheduler = BackgroundScheduler()

    # Planifiez l'exécution des fonctions avec un intervalle spécifique (par exemple, toutes les 5 secondes)
    scheduler.add_job(task1, 'interval', seconds=11550, max_instances=5)
    scheduler.add_job(task2, 'interval', seconds=11555, max_instances=5)

    # Démarrez le planificateur en arrière-plan
    scheduler.start()

    try:
        # Exécutez en continu jusqu'à ce qu'une interruption clavier (Ctrl+C) soit détectée
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Arrêtez le planificateur en arrière-plan
        scheduler.shutdown()

# Lancez la fonction principale
if __name__ == "__main__":
    main()
'''
from pprint import pprint
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db=client["info_betkeen"]

db_over_under=client["finale"]
collection1=db_over_under["over_under"]
data=list(collection1.find({},{"_id":0}))

collection2=db_over_under["surebet"]

collection3=db_over_under["valuebet"]

collection4=db_over_under["storage"]
collection5=db_over_under["brouillon"]
p=list(collection4.find({},{}))[10]
#resultat1=collection5.insert_one(p)
pprint(list(collection5.find()))
b={}
over_1xbet=5,56
goal=4.5
b[f"over_1xbet {goal}".replace(".",",")]=over_1xbet


print(b)


'''