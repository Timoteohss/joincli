import urllib.request, json, sys, os, argparse, re
import urllib.parse, socket, requests

def api_regex(s, pat=re.compile(r"\w{32}")):
    if not pat.match(s):
        raise argparse.ArgumentTypeError
    return s

def str2bool(arg):
    if arg.lower() in ('yes','true','t','y','1'):
        return True
    if arg.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected!')

def arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-ak", "--apikey", help="Your api key, get it at ...", type=api_regex)
    ap.add_argument("-up", "--update", help="Set to true so you can update your devices",
                    type=str2bool, nargs="?", const=True, default=False)

    return vars(ap.parse_args())

def open_remote_devices(apikey):
    try:
        devices = urllib.request.urlopen("https://joinjoaomgcd.appspot.com/_ah/api"
                                        "/registration/v1/listDevices?apikey=" +
                                        apikey).read()
        try:
            return json.loads(decode_UTF8(devices))
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
    
def open_local_devices():
    try:
        with open("devices.json","r") as deviceJSON:
            device_data_old = json.loads(deviceJSON.read())
            return device_data_old
    except:
        return None

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

def decode_UTF8(data):
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    except Exception as e:
        raise(e)

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
    reg["deviceType"] = "13"

    print("Sending request...")    

    try:
        response = requests.post(url, json.dumps(reg), headers=headers)
        response = response.json()
    except requests.exceptions.HTTPError as e:
        raise(e)
    
    #TODO handle device already registered
    #print(response["errorMessage"])

    update_devices(device)
    

#setup_devices(arguments(),open_local_devices())
register_new_device(open_local_devices())
    
    
    