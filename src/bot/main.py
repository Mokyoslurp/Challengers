import hikari
from pathlib import Path


TOKEN_FILE = Path(__file__).parent / "token"

file = open(TOKEN_FILE)
token = file.readline()
file.close()


bot = hikari.GatewayBot(token)

bot.run()
