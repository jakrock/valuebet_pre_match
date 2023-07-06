import pymongo

client=pymongo.MongoClient('localhost',27017)
db=client["bet_live"]


db_match_odd=client["finale"]
collection1=db_match_odd["Match Odds"]
data=list(collection1.find({},{"_id":0}))
from pprint import pprint
collection2=db_match_odd["surebet"]
collection3=db_match_odd["valuebet"]
collection4=db_match_odd["storage"]
#resultat=list(collection1.find({},{"_id":0}))
#print(list(resultat))
pprint(len(list(collection4.find({},{"_id":0}))))

#print(list(collection2.find({})))
h=[1,3,5,4,6,78,96,2,8,5,26,14,45,75,35,85]
print(h[2:None])
