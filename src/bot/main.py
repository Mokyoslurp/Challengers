import hikari
from pathlib import Path

from challengers.game import Tournament, Player
from challengers.main import CARD_DATA_FILE_PATH, TROPHY_DATA_FILE_PATH


TOKEN_FILE = Path(__file__).parent / "token"

file = open(TOKEN_FILE)
token = file.readline()
file.close()


bot = hikari.GatewayBot(token)

started = False
player = Player(0, "TestP")


async def main():
    tournament = Tournament(1)
    tournament.load_game_cards(CARD_DATA_FILE_PATH)
    tournament.load_game_trophies(TROPHY_DATA_FILE_PATH)

    tournament.set_new_player(player)

    winner = await tournament.play()

    if winner:
        print("Winner is " + winner)

        tournament.print_scores()


@bot.listen()
async def ping(event: hikari.GuildMessageCreateEvent) -> None:
    global started
    global player
    if event.is_human:
        if bot.get_me().id in event.message.user_mentions_ids:
            await event.message.respond(event.author.mention)

            if not started:
                started = True
                await main()
            else:
                if player.has_to_manage_cards:
                    player.done_managing_cards()
                if player.has_to_play:
                    player.play()


bot.run()
