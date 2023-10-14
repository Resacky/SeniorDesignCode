import asyncio
import aioschedule as schedule
import datetime

async def job():
    print("Job running at", datetime.datetime.now())

async def main():
    schedule.every(10).seconds.do(job)  # Schedule job every 10 seconds

    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)  # Sleep 1 second between checks

if __name__ == '__main__':
    asyncio.run(main())
