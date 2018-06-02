# joinCLI

This is as linux client for the [Join app](https://joaoapps.com/join/).

Please read the section "What this repo contains", **please**.

Instructions:

```shell
$ git clone https://github.com/timoteohss/joincli.git
$ cd joincli
$ python3 joincliSetup.py -ak <YOUR_API_KEY>
$ python3 joincliSetup.py -re
>Follow instructions, use port 1820 for now
$ python3 joincliServer.py
```

You should have the server running listening on port 1820.
If you want to have it working from external (outside your LAN) sources, open the port 1820 on your router.

Hack away the funcion `handleMessage` on joincliHandler.py to do your bidding, included is a very, very crute implementation os clipboard setting and any URL opening pushed from your devices, also notifications.

Not working with Chrome pushes tho, figures.



Pre-pre-alpha description, full on documentation "comming soon"™.

# What this repo contains:

1. Spaghetti v0.01 code
2. Rushed methods
  * ~~pls fork and help me~~

MIT license