import copy
import itertools
import pymongo
from pprint import pprint

from datetime import datetime

import datetime

def timestamp_to_date(timestamp):
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    return dt_object.strftime("%d %b %Y %H:%M")



client = pymongo.MongoClient("mongodb://localhost:27017/")
db=client["info_match_1xbet_live"]
r=db.id_1xbet_live.find({},{"_id:0"})
print(list(r))


db=client["info_betkeen"]
#collection= db["cookie_desktop"]
#collection1=db["cookie_mobile"]
con=db["liste_match_betkeen"]

a=[{"1":4},{"2":5},{"6":8},{"j":7}]

f=[7,8,5,4,2,6,9]

l=["Asian Handicap","Goal Lines","Match Odds","Over/Under 0.5 Goals", "Over/Under 1.5 Goals", "Over/Under 2.5 Goals" ,"Over/Under 3.5 Goals", "Over/Under 4.5 Goals" ,"Over/Under 5.5 Goals" ,"Over/Under 6.5 Goals", "Over/Under 7.5 Goals", "Over/Under 8.5 Goals","Half Time", "First Half Goals 0.5","First Half Goals 1.5","First Half Goals 2.5",'Both teams to Score?' ]

for i in range(len(a)):
	a[i]=[{**copy.deepcopy(a[i]), "event":f[_]} for _ in range(7)]

resultat = list(itertools.chain.from_iterable(a))

from datetime import datetime
 
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
        "août": 8,
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
 
timestamp("12 May 2023 01:00")





x=db.con.find({},{"_id":0})

betkeen=list(x[0]["events"])

#betkeen=sorted(betkeen,key= lambda x:x)
pprint(betkeen)

#betkeen=list(filter(lambda x:x["market"] in l,betkeen))
betkeen = [x for x in betkeen if x.get("market") in l]

'''

betkeen1=itertools.groupby(betkeen,key=lambda x:x[1][1])

betkeen1=[([l for l in x]) for z,x in betkeen1]
pprint(betkeen1)
print(len(betkeen1))
'''
# je transform la date des matchs de betkeen en time stamp
for i in betkeen:
	i["S"]=timestamp(i["S"])
p=sorted(betkeen,key=lambda x:x["events"])


f=itertools.groupby(p,key=lambda x:x["events"])

f1=[[k for k   in x ] for z ,x in f]
print(f1)
import pickle
# Sauvegarder la liste dans un fichier binaire
with open('matchbetkeen.pickle', 'wb') as f:
    pickle.dump(f1, f)
    





import random
from datetime import datetime, timedelta




