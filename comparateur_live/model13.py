import threading
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import time 



async def run_file5(file_path):
    process = await asyncio.create_subprocess_exec('python3', file_path, stdout=asyncio.subprocess.PIPE)
    output, _ = await process.communicate()
    return output.decode().strip()

async def main5():
    file_path = 'half_1.5_goal.py'
    output = await run_file5(file_path)
    #print(output)

async def run_file6(file_path):
    process = await asyncio.create_subprocess_exec('python3', file_path, stdout=asyncio.subprocess.PIPE)
    output, _ = await process.communicate()
    return output.decode().strip()

async def main6():
    file_path = 'half_2.5_goal.py'
    output = await run_file6(file_path)
    #print(output)



async def main():
    # Créez un planificateur asyncio
    scheduler = AsyncIOScheduler()

    # Planifiez l'exécution des fonctions avec un intervalle spécifique (par exemple, toutes les 5 secondes)

    scheduler.add_job(main5, 'interval', seconds=20, max_instances=16)
    scheduler.add_job(main6, 'interval', seconds=20, max_instances=16)



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
