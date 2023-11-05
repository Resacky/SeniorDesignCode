import time
import board
import busio
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_mqtt import MQTT

# WiFi settings
WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"

# MQTT settings
MQTT_BROKER = "mqtt_broker_address"
MQTT_PORT = 1883
MQTT_TOPIC = "esp32s2/instructions"

# Define ESP32 pins
esp32_cs = DigitalInOut(board.D9)
esp32_ready = DigitalInOut(board.D10)
esp32_reset = DigitalInOut(board.D5)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

def connect_wifi():
    while not esp.is_connected:
        try:
            print("Connecting to WiFi...")
            esp.connect_AP(WIFI_SSID, WIFI_PASSWORD)
            print("Connected!")
        except RuntimeError as e:
            print("Cannot connect to WiFi:", e)
            time.sleep(1)
            continue

def message_callback(topic, payload):
    print("Received message:", payload, "on topic:", topic)
    instruction = payload.decode('utf-8')
    
    # Add your code here to handle different instructions, e.g.,
    # if instruction == "LED_ON":
    #     turn_on_led()

# Connect to WiFi
connect_wifi()

# Initialize MQTT
client_id = "ESP32S2_MQTTClient"
mqtt_client = MQTT(socket, broker=MQTT_BROKER, port=MQTT_PORT, client_id=client_id)

# Connect MQTT callbacks
mqtt_client.callback_message = message_callback

# Connect to MQTT broker
mqtt_client.connect()
mqtt_client.subscribe(MQTT_TOPIC)

while True:
    mqtt_client.loop()
    time.sleep(0.1)
