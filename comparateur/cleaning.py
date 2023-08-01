
import sqlite3
import pandas as pd
import pymongo
import pathlib
import os

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
import httpx
import time
import aiohttp
from functools import reduce
import uuid
import sys
#sys.stdout = open("NUL", "w")




client=pymongo.MongoClient('localhost',27017)

db_over_under=client["finale_pre"]
collection1=db_over_under["over_under"]
data=list(collection1.find({},{"_id":0}))

collection2=db_over_under["surebet"]

collection3=db_over_under["valuebet"]
collection4=db_over_under["storage"]
collection5=db_over_under["storage surebet"]

resultat=list(collection5.find({},{"_id":0}))
#pprint(list(resultat))

data=list(collection4.find({},{"_id":0}))
#pprint(list(resultat))

with open(f"depot/donneesValuebet{str(uuid.uuid4())}--{time.time()}.json", "w") as f:
    json.dump(data, f)

r=collection4.delete_many({})


with open(f"depot/donneesSurebet{str(uuid.uuid4())}--{time.time()}.json", "w") as f:
    json.dump(resultat, f)

r=collection5.delete_many({})


