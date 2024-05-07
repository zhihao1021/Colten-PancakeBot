from asyncio import create_task, gather, run

from api import run as run_api
from bot import run as run_bot
from database.database import setup_db

async def main():
    await setup_db()

    tasks = [
        create_task(run_api(), name="API Task"),
        create_task(run_bot(), name="Discord Bot Task"),
    ]
    await gather(*tasks)

if __name__ == "__main__":
    run(main=main())
