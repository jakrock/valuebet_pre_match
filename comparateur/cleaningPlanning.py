import threading
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import time 



async def run_file7(file_path):
    process = await asyncio.create_subprocess_exec('python3', file_path, stdout=asyncio.subprocess.PIPE)
    output, _ = await process.communicate()
    return output.decode().strip()

async def main7():
    file_path = 'cleaning.py'
    output = await run_file7(file_path)
    #print(output)




async def main():
    # Créez un planificateur asyncio
    scheduler = AsyncIOScheduler()

    # Planifiez l'exécution des fonctions avec un intervalle spécifique
    scheduler.add_job(main7, 'interval', seconds=20000, max_instances=10)


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
