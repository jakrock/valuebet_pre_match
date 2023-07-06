import pymongo



client=pymongo.MongoClient('localhost',27017)
db=client["bet_live"]
import json
import uuid
from pymongo import MongoClient



db_match_odd=client["finale"]
collection1=db_match_odd["Match Odds"]
data=list(collection1.find({},{"_id":0}))
from pprint import pprint
collection2=db_match_odd["surebet"]
collection3=db_match_odd["valuebet"]
collection4=db_match_odd["storage"]
resultat=collection3.delete_one({})
resultat=list(collection3.find({},{"_id":0}))
pprint(list(resultat))

