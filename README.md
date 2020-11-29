# Ucopia connect
## Why
This is the wifi system used at the [St Felicity's Hospital](https://www.maternite-catholique-sainte-felicite.fr/).

The Ucopia portal system is a bit painful to use. As soon as you disconnect you wifi
for a minute it breaks.

## How it works
It checks regularly if you are logged in and if not reconnects you.

## How to use
You need to register and define the following environment variable:
- `PORTAL_LOGIN`
- `PORTAL_PASSWORD`

The following config is optional with these default value:
- `PORTAL_ADDRESS=https://controller.access.network`
- `CHECK_PERIOD=20`

The best option is probably to run it with docker:
```bash
docker run --name=wifi-autoconnect -ti -e PORTAL_LOGIN=$MCSF_LOGIN -e PORTAL_PASSWORD=$MCSF_PASSWORD --restart=always fclairamb/ucopia-connect
```

It should give you something like that:
```
docker logs wifi-autoconnect -f
2020-11-29 17:41:27,623 | INFO | Checking current step
2020-11-29 17:41:27,911 | INFO | Current step: LOGON
2020-11-29 17:41:27,912 | INFO | Attempting login !
2020-11-29 17:41:28,305 | INFO | We're connected !
2020-11-29 17:41:48,326 | INFO | Checking current step
2020-11-29 17:41:49,222 | INFO | Current step: FEEDBACK
2020-11-29 17:41:49,222 | INFO | All good
2020-11-29 17:42:09,343 | INFO | Checking current step
2020-11-29 17:42:10,066 | INFO | Current step: FEEDBACK
2020-11-29 17:42:10,067 | INFO | All good
```
