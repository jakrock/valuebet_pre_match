

import pandas as pd
t={1:75,2:85,3:56,4:84}
print(max(t[1],t[2]))
print(list(filter(lambda x:max(x[1],x[1]),t.items())))

from functools import reduce
a={}
t = {
    "home_betkeen": 10,
    "away_betkeen": 15,
    "draw_betkeen": 8,
    "home_1xbet": 12,
    "away_1xbet": 9,
    "draw_1xbet": 11
    }


if t["home_betkeen"]>t["home_1xbet"]:
	a["home_betkeen"]=t["home_betkeen"]
else:
	a["home_1xbet"]=t["home_1xbet"]

if t["away_betkeen"]>t["away_1xbet"]:
	a["away_betkeen"]=t["away_betkeen"]
else:
	a["away_1xbet"]=t["away_1xbet"]

if t["draw_betkeen"]>t["draw_1xbet"]:
	a["draw_betkeen"]=t["draw_betkeen"]
else:
	a["draw_1xbet"]=t["draw_1xbet"]
inverse_sum = reduce(lambda x, y: x + (1 / y), t.values(), 0)
#if inverse_sum<0.99:
print(inverse_sum)
		
from functools import reduce

my_dict = {"a": 2, "b": 4, "c": 8}

inverse_sum = reduce(lambda x, y: x + (1 / y), my_dict.values(), 0)

print(inverse_sum)
a1=[{'C': 9.99, 'G': 3, 'P': -1.5, 'T': 7}]

def handicap_Traitement( a1, *args, **kwargs):
	filtered_list = list(filter(lambda x: x["G"] == kwargs.get("G") and x["T"] == kwargs.get("T_home") and ("P" in x.keys() and x["P"] == kwargs.get("home_handicap")) or ("CE" in x.keys() and x["CE"] == kwargs.get("home_handicap")), a1))
	print(filtered_list)
handicap_Traitement(a1,home_handicap=-1.5,away_handicap=1.5,G=3,T_home= 7,T_away= 8)

import pymongo
from pprint import pprint
d=[1.3,5]
d1=d.copy()
d1.append(4)
print(d1)

client = pymongo.MongoClient("mongodb://localhost:27017/")
db=client["info_betkeen"]
#collection= db["cookie_desktop"]
#collection1=db["cookie_mobile"]
con=db["liste_match_betkeen_live"]

db_over_under=client["finale"]
collection1=db_over_under["over_under"]
data=list(collection1.find({},{"_id":0}))

collection2=db_over_under["surebet"]

collection3=db_over_under["storage"]
resultat=list(collection1.find({},{"_id":0}))
pprint(list(resultat))



pprint(len(list(collection3.find())))

over_betkeen=2.56
under_betkeen=1.54

p_over_betkeen = (1 / over_betkeen) 
p_under_betkeen = (1 / under_betkeen) 
marge =  (p_under_betkeen + p_over_betkeen)-1
m_over_betkeen = (2 * over_betkeen) / (2 - marge * over_betkeen)
m_under_betkeen = (2 * under_betkeen) / (2 - marge * under_betkeen)

print(m_over_betkeen)
print(m_under_betkeen)
home_betkeen=6.22
away_betkeen=2.22
draw_betkeen=1.73
p_home_betkeen=(1/home_betkeen)
p_away_betkeen=(1/away_betkeen)
p_draw_betkeen=(1/draw_betkeen)

marge=(p_home_betkeen+p_away_betkeen+p_draw_betkeen) -1
m_home_betkeen=(3*home_betkeen)/(3-marge*home_betkeen)
m_away_betkeen=(3*away_betkeen)/(3-marge*away_betkeen)
m_draw_betkeen=(3*draw_betkeen)/(3-marge*draw_betkeen)

print(marge)


print("lol")
import re

def enlever_caracteres_speciaux0(chaine):
    chaine = re.sub(r'[^\w\s]', '', chaine)
    return chaine

chaine_originale = "Étudiez l'étranger!"
chaine_sans_caracteres_speciaux = enlever_caracteres_speciaux0(chaine_originale)
print(chaine_sans_caracteres_speciaux)  # Affiche "Etudiez letranger"
import unicodedata

def enlever_caracteres_speciaux(chaine):
    chaine = unicodedata.normalize('NFKD', chaine).encode('ASCII', 'ignore').decode('utf-8')
    return chaine

chaine_originale = "Étudiez l'étranger!"
chaine_sans_caracteres_speciaux = enlever_caracteres_speciaux(enlever_caracteres_speciaux0(chaine_originale))
print(chaine_sans_caracteres_speciaux)  # Affiche "Etudiez l'etranger!"
