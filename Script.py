import json
import aiohttp
import serial
import asyncio
# for converting radians to degrees
import math 

# API endpoint URL.
# URL endpoint: http://localhost:3000/signalk/v1/api/
api_url = "http://localhost:3000/signalk/v1/api/"

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
                speed = round(vessel_data["navigation"]["speedThroughWater"]["value"], 1)

                # Grab the speedThroughWater timestamp and save it onto a variable
                speed_timestamp = vessel_data["navigation"]["speedThroughWater"]["timestamp"]

                # Grab the headingMagnetic value and save it onto a variable
                heading_magnetic = vessel_data["navigation"]["headingMagnetic"]["values"]["can0.1"]["value"]
                heading_magnetic_degrees = round(heading_magnetic * (180 / math.pi))

                # Grab the windAngle & windSpeed value and save it onto a variable
                wind_angle = vessel_data["environment"]["wind"]["angleApparent"]["value"]
                wind_angle_degrees = round(wind_angle * (180 / math.pi))
                wind_speed = vessel_data["environment"]["wind"]["speedApparent"]["value"]
                wind_speed_knots = round(wind_speed * 1.94384, 1)

                # Create a string w/ the relevant data to then print onto the console, and send it to the serial port
                print(f"Boat with UUID: {vessel_uuid}'s data at {speed_timestamp}")

                # This is the actual string to be sent to the serial port
                string = f"Heading {heading_magnetic_degrees} degrees, boat speed {speed} knots, wind angle {wind_angle_degrees} degrees, wind speed {wind_speed_knots} knots\r"
                print(string)
                
                # Send the data to the serial port, converting the string into bytes.
                ser.write(string.encode())
                
    except Exception as e:
        print(f"Error processing data or sending to serial port: {e}")

async def main():
    # Indefinitely run whatever is within the main function.
    while True:
        await job()  # Run the job
        await asyncio.sleep(12)  # Sleep for 10 seconds before running the job again

if __name__ == '__main__':
    try:
        asyncio.run(main())
    finally:
        ser.close()  # Ensure the serial connection is closed when the program exits