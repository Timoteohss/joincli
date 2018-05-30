import json, subprocess, pyperclip, webbrowser, sys

# This function handles Messages received by the server,
# modify it according to your needs, some message fields are described below:

# date - Time of the message being sent in epoch
# deviceId - The ID of this device
# find - (Android only) Ring the device full volume
# id - The ID of the push, for History purposes
# location - (Android only) Location data
# requestId - The ID of the request on Join servers, for History purposes
# senderId - The ID of the device that pushed this message
# text - The body of a message
# title - The title of a message
# clipboard - The clipboard in case that's what you're into, 
#             interchangeable with 'text' field.
# toTasker - (Android only) This message is sent to tasker?
# fromTasker - This message is sent from tasker?
# files - An array containing urls to google drive files uploaded by join
# url - A single URL


def handleMessage(message):
    if message is False:
        subprocess.Popen(['notify-send','JoinCLI server died',
                        'Restart daemon to continue listening'])
        sys.exit(1)
    
    if 'files' in message:
        if (len(message['files']) > 0):
            subprocess.Popen(['notify-send','Opening file on a browser'])
            webbrowser.open_new_tab(message['files'][0])
            return
    
    #Example of copying the message clipboard to system clipboard and notifying it.
    if 'clipboard' in message:
        subprocess.Popen(['notify-send', 'Clipboard set to:' , message['clipboard']])
        pyperclip.copy(message['clipboard'])
        
    if 'url' in message:
        subprocess.Popen(['notify-send','Opening page:', message['url']])
        webbrowser.open_new_tab(message['url'])

        
