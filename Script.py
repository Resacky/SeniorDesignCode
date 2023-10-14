import json
import serial
import asyncio

# Open the serial connection outside of the job function.
# This will ensure that the serial connection is opened only once.
try:
    ser = serial.Serial('/dev/serial0', 9600)  # Open serial port at 9600 bps
except Exception as e:
    print(f"Error opening serial port: {e}")

async def job():
    try:
        # This will be the API URL in the future...
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
                
                # Send the data to the serial port
                ser.write(string.encode())  # Convert the string to bytes
                
    except Exception as e:
        print(f"Error processing data or sending to serial port: {e}")

async def main():
    while True:
        await job()  # Run the job
        await asyncio.sleep(10)  # Sleep for 10 seconds before running the job again

if __name__ == '__main__':
    try:
        asyncio.run(main())
    finally:
        ser.close()  # Ensure the serial connection is closed when the program exits