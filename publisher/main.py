import signal
import sys
import time
import adafruit_dht
import board
import RPi.GPIO as GPIO
import threading
import socket 
import json

api_host = 'erwor.me'
api_port = 24121

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

SENSOR_PIN = board.D4
dht11 = adafruit_dht.DHT11(SENSOR_PIN, use_pulseio=False)

last_temp = 0
last_hum = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send(temp, hum):
    data = {
        "temp": temp,
        "hum": hum,
    }
    [_, _, _, _, address] = socket.getaddrinfo(api_host, api_port, socket.AF_INET, socket.SOCK_DGRAM).pop()
    message = json.dumps(data)
    sock.sendto(message.encode('ascii', message), address)

def weather_loop():
    while True:
        try:
            dht11.measure()
        except RuntimeError:
            continue
        temp = dht11.temperature
        hum = dht11.humidity
        if temp is not None and hum is not None:
            print(f'Temp: {temp}C   Hum: {hum}%')
            send_thread = threading.Thread(target=send, args=(temp, hum)) 
            send_thread.daemon = True
            send_thread.start()
            last_temp = temp
            last_hum = hum
        else:
            print("Sensor failure. Check wiring.")
        time.sleep(10)
 
def exit(a,b):
    GPIO.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit)

    weather_thread = threading.Thread(target=weather_loop)
    weather_thread.daemon = True

    weather_thread.start()
    weather_thread.join()
