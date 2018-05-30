import json
import subprocess
import pyperclip
import webbrowser
import joincli

def handleMessage(message):
    if 'clipboard' in message:
        subprocess.Popen(['notify-send', 'Clipboard set to:' , message['clipboard']])
        pyperclip.copy(message['clipboard'])

        
