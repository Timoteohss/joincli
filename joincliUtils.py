import re, argparse, json

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

def open_local_devices():
    try:
        with open("devices.json","r") as deviceJSON:
            device_data_old = json.loads(deviceJSON.read())
            return device_data_old
    except:
        return None

def decode_UTF8(data):
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    except Exception as e:
        raise(e)
