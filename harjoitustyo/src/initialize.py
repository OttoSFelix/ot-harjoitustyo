import os
import requests
from db_search import get_players, initialize_matches_table
from web_search import get_rating, get_player_matches
from database_connection import get_database_connection
session = requests.Session()
connection = get_database_connection()
cursor = connection.cursor()
get_rating(connection=connection)
if os.path.exists("ratinglist"):
    os.remove("ratinglist")
initialize_matches_table()
players = get_players(cursor)[:100]
for player in players:
    get_player_matches(player, connection, session)
    print(f'\rInitializing database {player.rank}% done', end='', flush=True)
connection.close()
session.close()
