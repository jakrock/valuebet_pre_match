from fastapi import FastAPI,Request
from fastapi.responses import FileResponse
import pymongo


app = FastAPI()

client=pymongo.MongoClient('localhost',27017)

@app.get("/mini")
async def read_root1():
    return FileResponse("/home/romualdjja/projet1/projet1/fast_api/templates/indexmini.html")


@app.get("/mini1/mini")
async def datapi():
    db=client["finale"]
    collection6=db['valuebet']
    data=list(collection6.find({},{"_id":0}))
    newdata=list(filter(lambda x:x["valeur"]<2.21,data))
    return newdata
   


# @app.get("/mini")
# async def read_root1():
#     return FileResponse("/home/romualdjja/projet1/projet1/fast_api/templates/indexmini.html")


@app.post("/item/retour")
async def create_item(request: Request):
    # Récupérer les données brutes du corps de la requête
    

    db=client["finale"]
    collection5=db["data supprimer"]
    item_data = await request.body()

    import json

    item_data_json = item_data.decode()  # Décodez les données en tant que chaîne JSON
    item_data_dict = json.loads(item_data_json)  # Convertissez la chaîne JSON en un dictionnaire Python

    result = collection5.insert_one(item_data_dict[0])

    # Traiter les données ou effectuer les opérations souhaitées
    # ...

    return {"message": "Item created successfully"}


@app.post("/item/retour/surebet")
async def create_item1(request: Request):
    # Récupérer les données brutes du corps de la requête
    
    db=client["finale"]
    collection6=db["data supprimer1"]
    item_data = await request.body()

    import json

    item_data_json = item_data.decode()  # Décodez les données en tant que chaîne JSON
    item_data_dict = json.loads(item_data_json)  # Convertissez la chaîne JSON en un dictionnaire Python

    result = collection6.insert_one(item_data_dict[0])

    # Traiter les données ou effectuer les opérations souhaitées
    # ...

    return {"message": "Item created successfully"}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8001)
