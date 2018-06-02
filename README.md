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
```

## Listening for pushes:
```shell
$ python3 joincliServer.py
```

You should have the server running listening on port 1820.
If you want to have it working from external (outside your LAN) sources, open the port 1820 on your router.

Hack away the funcion `handleMessage` on joincliHandler.py to do your bidding, included is a very, very crute implementation os clipboard setting and any URL opening pushed from your devices, also notifications.

Not working with Chrome pushes tho, figures.

## Pushing:
```shell
$ joincli.py [-h] [-ti] TITLE [-te] TEXT [-fi] FIND [-mv] MEDIAVOLUME
```

It should work with any device, for now tho youre pushing only for your prefered device you have chosen on setup.

## Dependencies:
```
python3
pyperclip (if you want the clipboard working hasslefree)
```



Pre-pre-alpha description, full on documentation "comming soon"™.

# What this repo contains:

1. Spaghetti v0.01 code
2. Rushed methods
  * ~~pls fork and help me~~

MIT license