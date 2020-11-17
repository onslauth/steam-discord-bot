# Steam-Discord-Bot

This is a Discord bot that can connect to the RCON port on a Steam SRCDS server and run commands.

## Installation

```
pip3 install -r requirements.txt
```

## Config

Please add your Discord Bot Client Token to `main.py` in the specified location.
Change the server list in `bot.py`. You can add multiple servers and ports, but each needs to have a unique server name.

## Running

To run the bot:
```
python3 ./main.py
```

## Debug

The code has a few `print` statements that have been commented out that can be uncommented for debugging, or new print statements added.
