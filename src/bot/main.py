import hikari
from pathlib import Path


TOKEN_FILE = Path(__file__).parent / "token"

file = open(TOKEN_FILE)
token = file.readline()
file.close()


bot = hikari.GatewayBot(token)


@bot.listen()
async def ping(event: hikari.GuildMessageCreateEvent) -> None:
    if event.is_human:
        if bot.get_me().id in event.message.user_mentions_ids:
            await event.message.respond(event.author.mention)


bot.run()
