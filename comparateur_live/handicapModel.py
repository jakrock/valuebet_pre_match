import sqlite3
import pandas as pd
import pymongo
import pathlib



import asyncio
from datetime import datetime, timedelta





from pprint import pprint

# Charger un fichier CSV
df = pd.read_csv('data1.csv')


dict_df = df.to_dict('records')



client=pymongo.MongoClient('localhost',27017)
db=client["bet_live"]
collection=db["betkeen_live"]



def recuperation_id_handicap(data):
	liste=[]
	Id={}
	for i in data:
		Id["events_1xbet"]=i['events1xbet'] or None
		Id["events_betkeen"]=i["events"] or None
		Id["heure_debut"]=i["S"] or None
		Id["id_handicap_1xbet"]=i["Id1xbet"] or None
		#Id["4"]=i["4"]

		r1=list(collection.find({"4":str(i["4"])},{"_id":0}))

		db=client["bet_live"]
		collection1=db["stock_temp_live"]
		resultat2=collection1.delete_many({})
		resultat=collection1.insert_many(r1)
		t=list(collection1.find({"market":'Asian Handicap'},{"_id":0,"I":1}))
		#print(t)
		try:
			Id["id_handicap_betkeen"]=t[0]["I"] or None
			Id["market"]="handicap"
			liste.append(Id.copy())
			Id.clear()
		except:
			pass
	return liste
a=recuperation_id_handicap(dict_df)	



def mongodbParking():
	db_handicap=client["finale"]
	collection1=db_handicap["handicap"]


	# Obtention de l'heure actuelle moins 2 heures
	deux_heures_avant = datetime.now() - timedelta(hours=2)
	deux_heures_avant = deux_heures_avant.timestamp()

	print(deux_heures_avant)
	# Suppression des documents avec un timestamp inférieur à deux_heures_avant
	result = collection1.delete_many({"heure_debut": {"$lt": deux_heures_avant}})

	# Affichage du nombre de documents supprimés
	print(f"{result.deleted_count} documents ont été supprimés.")

	for i in a:
		# Vérification si le document existe déjà
		existing_document = collection1.find_one({'id_handicap_1xbet':i["id_handicap_1xbet"]},{"_id:0"})

		# Exécution de l'opération d'upsert
		if existing_document is None:
		    document = i
		    result = collection1.insert_one(document)
		    print("Document inséré avec succès.")
		else:
		    print("Le document existe déjà et n'a pas été mis à jour.")


	print(list(collection1.find()))

mongodbParking()


