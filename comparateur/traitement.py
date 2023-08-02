



import pickle
import pymongo
import pandas as pd
#import pandas_dedupe
from pprint import pprint
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import itertools

import datetime
import subprocess

import sys
#sys.stdout = open("NUL", "w")


def timestamp_to_date(timestamp):
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    return dt_object.strftime("%d %b %Y %H:%M")




# Ouvrir le fichier pickle en mode lecture binaire
with open('matchbetkeen.pickle', 'rb') as f:
    # Charger l'objet à partir du fichier
    matchbetkeen = pickle.load(f)

# Utiliser l'objet chargé


matchbetkeen1= list(itertools.chain.from_iterable(matchbetkeen))
#print(matchbetkeen1)

client=pymongo.MongoClient('localhost',27017)
db=client["bet"]
collection=db["betkeen_live"]

resultat2=collection.delete_many({})
resultat=collection.insert_many(matchbetkeen1)
#print(resultat.inserted_ids)

#print(matchbetkeen)
newlistekeen=[]
for i ,j in enumerate(matchbetkeen):
    try:
        a=j[0]
    except:
        continue
    
    #a["entier"]=matchbetkeen[i]
    #print(a)
    newlistekeen.append(a)

for i in newlistekeen:
    i["date"]=timestamp_to_date(i["S"])


#pprint(newlistekeen)

data1=pd.DataFrame(newlistekeen)
#print(process.extractOne('Al-Ittihad v Al' ,data1["events"]))




# Ouvrir le fichier pickle en mode lecture binaire
with open('match1xbet.pickle', 'rb') as f:
    # Charger l'objet à partir du fichier
    mon_objet = pickle.load(f)

for i in mon_objet:
    i["date"]=timestamp_to_date(i["S"])

# Utiliser l'objet chargé

mb=sorted(mon_objet,key=lambda x:x["events"])
pprint(mb)
newlistekeen= sorted(newlistekeen, key=lambda x: x["S"])
mb=pd.DataFrame(mb)

#print(mb['date'].value_counts())


#data1["1xbetEvents"]=data1["events"].map(lambda x : process.extractOne(x,mb["events"]))
#data1["1xbetEvents"] = data1["events"].apply(lambda x: mb.loc[mb['events'].apply(lambda y: fuzz.token_sort_ratio(x, y)).idxmax()]['events'])
data1["1xbetEvents"] = data1["events"].apply(lambda x: (process.extract(x, mb["events"], scorer=lambda s1, s2: (0.4 * fuzz.token_set_ratio(s1, s2)) + (0.6 * fuzz.partial_ratio(s1, s2)), limit=2)[0]))

#ic on cree des colonne de dataframe divers en ce basans sur l indexxe recuperer dans data 1 que lon inject dans  md

data1["1xbetligue"] = data1["1xbetEvents"].apply(lambda x: mb["L"][x[2]])
data1["1xbetdate"] = data1["1xbetEvents"].apply(lambda x: mb["date"][x[2]])
data1["1xbetstamp"] = data1["1xbetEvents"].apply(lambda x: mb["S"][x[2]])
data1["Id1xbet"] = data1["1xbetEvents"].apply(lambda x: mb["I"][x[2]])
data1["events1xbet"] = data1["1xbetEvents"].apply(lambda x: mb["events"][x[2]])
#data1["MT"] = data1["1xbetEvents"].apply(lambda x: mb["MG"][x[2]])
didi={"nombre":[],"ok":[]}
didi=pd.DataFrame(didi)
import pandas as pd

# Créer les deux DataFrames
df1 = pd.DataFrame({'key1': ['A', 'B', 'C', 'D'],
                    'value1': [1, 2, 3, 4]})
df2 = pd.DataFrame({'key2': ['B', 'D', 'E', 'F'],
                    'value2': [5, 6, 7, 8]})

# Fusionner les deux DataFrames en spécifiant les colonnes à fusionner dans chaque DataFrame
merged_df = pd.concat([df1, df2])

# Afficher le résultat
#print(merged_df)






data1.reset_index()




pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

#mb.groupby(["S"]).count().max()
#print(data1)
#print(data1["date"].value_counts())
#print(data1["1xbetEvents"][1][1])

data1.to_csv('data1.csv', index=False)

dict_df = data1.to_dict('records')


#d=data1.loc[data1["1xbetEvents"].apply(lambda x: x[1]) > 70]
d = data1.loc[(data1["1xbetEvents"].apply(lambda x: x[1]) > 50) & (data1["S"] == data1["1xbetstamp"])]


print(d)
print(len(d))
d.to_csv('data1.csv', index=False)

dict_df = d.to_dict('records')
print(dict_df)
print(len(d))



subprocess.run(['python3', 'over_underModel.py'])
subprocess.run(['python3', 'model1.py'])
subprocess.run(['python3', 'handicapModel.py'])
#subprocess.run(['python3', 'over_under_0_5model.py'])
#subprocess.run(['python3', 'over_under_1_5model.py'])
subprocess.run(['python3', 'half_0.5_model.py'])
subprocess.run(['python3', 'half_1.5_model.py'])
subprocess.run(['python3', 'half_2.5_model.py'])
subprocess.run(['python3', 'halfmodel.py'])
#subprocess.run(['python3', 'over_under_2_5model.py'])
#subprocess.run(['python3', 'over_under_3.5_model.py'])
#subprocess.run(['python3', 'over_under_4.5_model.py'])






client.close()



import gc
gc.collect()

sys.exit()



