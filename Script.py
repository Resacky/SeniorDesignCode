import asyncio
import aioschedule as schedule
import datetime
import json
import aiohttp

async def fetch_data_from_api(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

async def job():
    try:
        # This will be the API URL...
        api_url = "YOUR_API_ENDPOINT_HERE"
        response = await fetch_data_from_api(api_url)
        json_data = json.loads(response)
        
        # For testing & debugging purposes...
        # with open("./test_input/SignalK_testInput.json", "r") as file:
            # json_data = json.load(file)
        
        # Extract boat's speed
        speed_path = json_data["vessels"]["urn:mrn:signalk:uuid:521ae5ac-f557-4c7f-a225-e0e3de666ecb"]["navigation"]["speedThroughWater"]["value"]
        speed_path_timestamp = json_data["vessels"]["urn:mrn:signalk:uuid:521ae5ac-f557-4c7f-a225-e0e3de666ecb"]["navigation"]["speedThroughWater"]["timestamp"]

        print(f"Boat's speed: {speed_path} at {speed_path_timestamp}")
    except Exception as e:
        print(f"Error reading the file or extracting speed: {e}")
 
async def main():
    schedule.every(10).seconds.do(job)  # Schedule job every 10 seconds

    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)  # Sleep 1 second between checks

if __name__ == '__main__':
    asyncio.run(main())
