import board
import wifi
import socketpool
import ampule
import time
import adafruit_dht
from digitalio import DigitalInOut, Direction

led = DigitalInOut(board.IO2)
led.direction = Direction.OUTPUT
led.value = False
dht = adafruit_dht.DHT22(board.IO42)

headers = {
    "Content-Type": "application/json; charset=UTF-8",
    "Access-Control-Allow-Origin": '*',
    "Access-Control-Allow-Methods": 'GET, POST',
    "Access-Control-Allow-Headers": 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
}

@ampule.route("/on")
def light_set(request):
    led.value = True
    return (200, headers, '{"enabled": true}')

@ampule.route("/off")
def light_status(request):
    led.value = False
    return (200, headers, '{"enabled": false}')

@ampule.route("/blink")
def light_status(request):
    for i in range(5):
        led.value = True
        time.sleep(0.5)
        led.value = False
        time.sleep(0.5)
    return (200, headers, '{"enabled": blink}')

@ampule.route("/dht22")
def light_status(request):
    temperature = dht.temperature
    humidity = dht.humidity
    return (200, headers, "Temp: {:.1f} °C \t Humidity: {}%".format(temperature, humidity))

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets not found in secrets.py")
    raise

try:
    print("Connecting to %s..." % secrets["ssid"])
    print("MAC: ", [hex(i) for i in wifi.radio.mac_address])
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    for i in range(10):
        led.value = True
        time.sleep(0.3)
        led.value = False
        time.sleep(0.3)
except:
    print("Error connecting to WiFi")
    raise

pool = socketpool.SocketPool(wifi.radio)
socket = pool.socket()
socket.bind(['0.0.0.0', 80])
socket.listen(1)
print("Connected to %s, IPv4 Addr: " % secrets["ssid"], wifi.radio.ipv4_address)

while True:
    ampule.listen(socket)
