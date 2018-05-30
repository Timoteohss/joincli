import argparse
import json
import urllib.request
import urllib.parse
import os
import socket
import requests


def arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-te", "--text", help="Text (Tasker Command or notification text)", nargs="*")
    ap.add_argument("-ti", "--title", help="Title (If set will create notification)", nargs="*")
    ap.add_argument("-mv", "--mediaVolume", help="Media Volume - number from 0 to 15", type=int, choices=range(0, 16))
    ap.add_argument("-fi", "--find", help="Set to true to make your device ring loudly")
    
    return vars(ap.parse_args())

def push_to_device(arguments,devices):
    #print(arguments)
    arguments["apikey"] = devices["apikey"]
    arguments["deviceId"] = devices[devices["pref"]]["deviceId"]

    encoded = []
    for key, value in arguments.items():
        if type(value) is list:
            value = " ".join(value)
        if value is not None:
            encoded.append("=".join([key, str(value)]))

    url = "https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?&"

    print(encoded)
    urllib.request.urlopen(url + "&".join(encoded).replace(" ","+")).read().decode("utf-8")

    
def devices():
    try:  # loads device json into a dictionary
        with open("devices.json", "r") as device:
            deviceData = json.loads(device.read())
    except:
        #TODO move into main and check for devices
        os.system("python3 joincliSetup.py")
        with open("devices.json", "r") as device:
            deviceData = json.loads(device.read())
    return deviceData


push_to_device(arguments(),devices())