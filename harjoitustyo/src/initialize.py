import os
import requests
from search import get_newest_rating, get_players, get_player_matches, initialize_matches_table
from database_connection import get_database_connection
session = requests.Session()
connection = get_database_connection()
cursor = connection.cursor()
get_newest_rating(cursor)
if os.path.exists("ratinglist"):
    os.remove("ratinglist")
initialize_matches_table()
players = get_players(cursor)[:100]
for player in players:
    get_player_matches(player, connection, session)
    print(f'\rInitializing database {player.rank}% done', end='', flush=True)
connection.close()
session.close()
