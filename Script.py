import json
import aiohttp
import serial
import asyncio

# API endpoint URL.
# URL endpoint: http://localhost:3000/signalk/v1/api/
api_url = "YOUR_API_ENDPOINT_HERE"

# Open the serial connection outside of the job function.
# This will ensure that the serial connection is opened only once.
try:
    ser = serial.Serial('/dev/serial0', 9600)  # Open serial port at 9600 bps
except Exception as e:
    print(f"Error opening serial port: {e}")

# This function is responsible for retrieving the data from the API and returning the json data.
async def fetch_data_from_api(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

async def job():
    try:
        # This code will retrieve the data from the API
        response = await fetch_data_from_api(api_url)
        # load the data to a variable
        json_data = json.loads(response)
        
        # For testing & debugging purposes...
        # with open("./test_input/SignalK_testInput.json", "r") as file:
            # json_data = json.load(file)
        
        # Dynamically iterate over vessels, should be only one vessel in this case.
        for vessel_uuid, vessel_data in json_data["vessels"].items():
            if "navigation" in vessel_data and "speedThroughWater" in vessel_data["navigation"]:
                # Grab the speedThoughWater value and save it onto a variable
                speed = vessel_data["navigation"]["speedThroughWater"]["value"]
                # Grab the speedThroughWater timestamp and save it onto a variable
                speed_timestamp = vessel_data["navigation"]["speedThroughWater"]["timestamp"]
                # Create a string w/ the relevant data to then print onto the console, and send it to the serial port.
                print(f"Boat with UUID {vessel_uuid}'s speed: {speed} at {speed_timestamp}")
                # This is the actual string to be sent to the serial port
                string = f"boat speed {speed} knots"
                print(string)
                
                # Send the data to the serial port, converting the string into bytes.
                ser.write(string.encode())
                
    except Exception as e:
        print(f"Error processing data or sending to serial port: {e}")

async def main():
    # Indefinitely run whatever is within the main function.
    while True:
        await job()  # Run the job
        await asyncio.sleep(10)  # Sleep for 10 seconds before running the job again

if __name__ == '__main__':
    try:
        asyncio.run(main())
    finally:
        ser.close()  # Ensure the serial connection is closed when the program exits