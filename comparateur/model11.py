import threading
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import time 


async def run_file1(file_path):
    process = await asyncio.create_subprocess_exec('python3', file_path, stdout=asyncio.subprocess.PIPE)
    output, _ = await process.communicate()
    return output.decode().strip()

async def main1():
    file_path =  'macth odd.py'
    output = await run_file1(file_path)
    #print(output)


import asyncio

async def run_file2(file_path):
    process = await asyncio.create_subprocess_exec('python3', file_path, stdout=asyncio.subprocess.PIPE)
    output, _ = await process.communicate()
    return output.decode().strip()

async def main2():
    file_path = 'over_under.py'
    output = await run_file2(file_path)
    #print(output)








async def main():
    # Créez un planificateur asyncio
    scheduler = AsyncIOScheduler()

    # Planifiez l'exécution des fonctions avec un intervalle spécifique (par exemple, toutes les 5 secondes)
    scheduler.add_job(main1, 'interval', seconds=23, max_instances=15)
    scheduler.add_job(main2, 'interval', seconds=21, max_instances=15)



    # Démarrez le planificateur asyncio
    scheduler.start()

    try:
        # Exécutez la boucle en continu
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        # Arrêtez le planificateur asyncio
        scheduler.shutdown()

asyncio.run(main())
client.close()
