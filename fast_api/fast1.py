from fastapi import FastAPI,Request
from fastapi.responses import FileResponse
import pymongo


app = FastAPI()

client=pymongo.MongoClient('localhost',27017)

@app.get("/mini")
async def read_root1():
    return FileResponse("/home/romualdjja/projet1/projet1/fast_api/templates/indexmini.html")


@app.get("/mini")
async def datapi(item_id1:str):
    db=client["finale"]
    collection6=db['valuebet']
    data=list(collection6.find({},{"_id":0}))
    newdata=list(filter(lambda x:x["valeur"]<1.89,data))
    return newdata
   




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=80)
