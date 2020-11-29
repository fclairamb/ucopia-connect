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
docker run -ti -e PORTAL_LOGIN=$YOUR_LOGIN -e PORTAL_PASSWORD=$YOUR_PASSWORD --restart=always fclairamb/utopia-connect
```
