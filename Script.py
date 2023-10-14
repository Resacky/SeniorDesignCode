import asyncio
import aioschedule as schedule
import datetime
import json
import aiohttp
import serial

async def fetch_data_from_api(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

async def job():
    try:
        # Set up the serial connection. The port might vary so you'd have to check that.
        ser = serial.Serial('/dev/serial0', 9600)  # Open serial port at 9600 bps

        # This will be the API URL...
        # api_url = "YOUR_API_ENDPOINT_HERE"
        # response = await fetch_data_from_api(api_url)
        # json_data = json.loads(response)
        
        # For testing & debugging purposes...
        with open("./test_input/SignalK_testInput.json", "r") as file:
            json_data = json.load(file)
        
        # Dynamically iterate over vessels
        for vessel_uuid, vessel_data in json_data["vessels"].items():
            if "navigation" in vessel_data and "speedThroughWater" in vessel_data["navigation"]:
                speed = vessel_data["navigation"]["speedThroughWater"]["value"]
                speed_timestamp = vessel_data["navigation"]["speedThroughWater"]["timestamp"]
                string = f"Boat with UUID {vessel_uuid}'s speed: {speed} at {speed_timestamp}"
                print(string)
                # To send the data to the serial port
                ser.write(string.encode())  # Convert the string to bytes
                ser.close()  # Close the serial connection
    except Exception as e:
        print(f"Error reading the file or extracting speed: {e}")
 
async def main():
    schedule.every(10).seconds.do(job)  # Schedule job every 10 seconds

    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)  # Sleep 1 second between checks

if __name__ == '__main__':
    asyncio.run(main())
