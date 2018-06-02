import urllib.request, json, sys, os, argparse, re
import urllib.parse, socket, requests
import joincliUtils as ju

def arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-ak", "--apikey", help="Your api key, get it at ...", type=ju.api_regex)
    ap.add_argument("-up", "--update", help="Set to true so you can update your devices",
                    type=ju.str2bool, nargs="?", const=True, default=False)
    ap.add_argument("-re", "--register", help="Register this device",
                    type=ju.str2bool, nargs="?", const=True, default=False)

    return vars(ap.parse_args())

def open_remote_devices(apikey):
    try:
        devices = urllib.request.urlopen("https://joinjoaomgcd.appspot.com/_ah/api"
                                        "/registration/v1/listDevices?apikey=" +
                                        apikey).read()
        try:
            return json.loads(ju.decode_UTF8(devices))
        except Exception as e:
            print("Bad unicode from server.")
            sys.exit(1)

    except urllib.error.HTTPError as e:
        print("Error code: ",e.code)
        sys.exit(1)
    except urllib.error.URLError as e:
        print("Are you connected to the internet?")
        print("Check your connection and try again")
        sys.exit(1)
    
def setup_devices(arguments, device):
    #If devices.json already exists
    if device is not None:
        if arguments["update"]:
            update_devices(device)
            sys.exit(1)
        else:
            print("Apikey already exists, use argument -up to update devices!")
            sys.exit(1)

    data = open_remote_devices(arguments["apikey"])

    if data['success']:
        device_data = {}
        device_data["apikey"] = arguments["apikey"]

        print("Registered devices under apikey: ")
        for item in data["records"]:
            device_data[item["deviceName"]] = {}
            device_data[item["deviceName"]]['deviceId'] = item['deviceId']
            device_data[item["deviceName"]]['deviceType'] = item['deviceType']
            #TODO Add another fields if needed
            print(item["deviceName"])

        pref = input("Choose the prefered device: ")
        while pref not in device_data:
            print("Device not listed as registered, try again:")
            pref = input("Choose the prefered device: ")

        device_data["pref"] = pref

        data = json.dumps(device_data, sort_keys=True, indent=4)

        with open("devices.json","w") as f:
            f.write(str(data))

        print("Device data gattered sussesfully!")
        sys.exit(1)

    
    else:
        print("Error returned from server: ",data['errorMessage'])
        print("Are you sure your API key is correct?")
        sys.exit(1)

def update_devices(device):
    devices_update = open_remote_devices(device["apikey"])

    if devices_update['success']:
        device_data = {}
        device_data["apikey"] = device["apikey"]

        for item in devices_update["records"]:
            device_data[item["deviceName"]] = {}
            device_data[item["deviceName"]]['deviceId'] = item['deviceId']
            device_data[item["deviceName"]]['deviceType'] = item['deviceType']
            #TODO Add another fields if needed

        device_data["pref"] = device["pref"]

        data = json.dumps(device_data, sort_keys=True, indent=4)

        with open("devices.json","w") as f:
            f.write(str(data))

        print("Device data updated sussesfully!")
        sys.exit(1)

def register_new_device(device):
    url = "https://joinjoaomgcd.appspot.com/_ah/api/registration/v1/registerDevice/"
    headers = {'content-type': 'application/json'}
    port = input("Which port should I listen to? [Default: 1820]") or "1820"
    name = input("Name this device: [Default: %s]" % socket.gethostname()) or socket.gethostname()
        
    print("Obtaining IP address...")
    ip_local = socket.gethostbyname(socket.gethostname()) + ":" + port
    ip_external = requests.get('https://api.ipify.org').text + ":" + port

    reg = {}
    reg["apikey"] = device["apikey"]
    reg["deviceName"] = name
    reg["regId"] = ip_external
    reg["regId2"] = ip_local
    #1 is Android
    #3 is Chrome
    #4 is Windows
    #6 is Firefox
    #12 is IFFT
    #13 is node-red
    reg["deviceType"] = "13"

    print("Sending request...")    

    try:
        response = requests.post(url, json.dumps(reg), headers=headers)
        response = response.json()
    except requests.exceptions.HTTPError as e:
        raise(e)
    
    #TODO handle device already registered
    print(response["errorMessage"])

    update_devices(device)
    


if __name__ == "__main__":
    import sys

    arguments = arguments()
    devices = ju.open_local_devices()

    if devices is None:
        if arguments["apikey"] is None:
            print("No local data received and no apikey given")
            print("Use -ak and feed me your apikey!")
            sys.exit(1)
        else:
            setup_devices(arguments, devices)
    elif arguments["update"]:
        update_devices(devices)
    elif arguments["register"]:
        register_new_device(devices)
    else:
        print("No arguments!")

       
    
    