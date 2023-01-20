# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")


def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"

    return cpuserial

pins = [17,27,22,5,6,13,19,26,23,24,25,16,20,21]

client = mqtt.Client()
client.on_connect = on_connect
client.connect("hbg-lmdsd01.americas.phoenixcontact.com", 1883, 60)

serial =  getserial()
print("PI SerialNumber: ", serial)
butPin = 17  # Broadcom pin 17 (P1 pin 11)
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
for pin in pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button pin set as input w/ pull-up

print("Here we go! Press CTRL+C to exit")
try:
    while 1:
        for pin in pins:
            print(pin, GPIO.input(pin))
            client.publish('IIOT/' + serial + '/GPIO'+str(pin), payload=i, qos=0, retain=False)
            print(f"send {i} to raspberry/topic")

            time.sleep(0.075)
        client.loop_forever()

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:

    GPIO.cleanup() # cleanup all GPIO




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
