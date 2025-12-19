from database_connection import get_database_connection
from playerinfo import Player

def initialize_matches_table():
    """
    Creates the necessary tables in the database
    Args:
        None
    Returns:
        None
    WARNING: Drops the existing 'All_matches' table if it exists, 
    resulting in complete data loss for that table.
    """
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute('DROP TABLE IF EXISTS All_matches')
    cursor.execute("""CREATE TABLE All_matches
                   (date text, 
                   match_type text, 
                   division text, 
                   player_name text, 
                   player_club text, 
                   opponent_name text, 
                   opponent_club text, 
                   score text, total text, 
                   outcome text)""")
    connection.commit()


def get_players(cursor):
    """
    Creates Player -class variables from all the players in the ratinglist
    Args:
        cursor: executable cursor of a database connection
    Returns:
        list of Player -class variables
    """
    players = []
    cursor.execute('SELECT * FROM Ratinglist')
    rows = cursor.fetchall()
    for row in rows:
        players.append(Player(row[0], row[1].strip(), row[2], row[3], row[4]))
    return players

def get_nth_players(rank, cursor):
    """
    Creates Player -class variables from the first n players in the ratinglist
    Args:
        rank: int
        cursor: executable cursor of a database connection
    Returns:
        list of Player -class variables
    """
    players = []
    cursor.execute('SELECT * FROM Ratinglist WHERE rank <= ?', (rank,))
    rows = cursor.fetchall()
    for row in rows:
        players.append(Player(row[0], row[1].strip(), row[2], row[3], row[4]))
    return players


def get_player_base_stats(name, cursor):
    """
    Calculates all the wins, losses and winrate of a given player
    Args:
        name: player name in string format
        cursor: executable cursor of a database connection
    Returns:
        String of the player name, all time wins, losses and winrate
    """
    name = name.strip()
    cursor.execute('SELECT * FROM Ratinglist WHERE name == ?', (name ,))
    row = cursor.fetchall()
    if not row:
        return f"Couldn't find player named {name}"
    row = row[0]
    player = Player(row[0], row[1], row[2], row[3], row[4])
    cursor.execute('SELECT * FROM All_matches WHERE player_name == ? ORDER BY date', (player.name,))
    rows = cursor.fetchall()
    if not rows:
        return f"Couldn't find matches for {name}"
    wins = 0
    losses = 0
    for row in rows:
        if row[9] == 'win':
            wins += 1
        elif row[9] == 'lose':
            losses += 1
        else:
            return f'{row} error while parsing outcome'
    winrate = (wins / (wins + losses)) * 100
    winrate = str(round(winrate, 2))
    return f"""{str(player)}
    all time wins: {wins}
    all time losses: {losses}
    All time win rate: {winrate}% """


def top_10_base_stats(cursor):
    """
    Calculates all the wins, losses and winrate 
    of the first 10 ranked players in the ratinglist
    Args:
        cursor: executable cursor of a database connection
    Returns:
        String of the players names, all time wins, losses and winratea
    """
    cursor.execute('SELECT * FROM Ratinglist WHERE rank <= 10')
    rows = cursor.fetchall()
    playerlist = []
    for row in rows:
        playerlist.append(row[1])
    stats = []
    for player in playerlist:
        stats.append(get_player_base_stats(player, cursor))
    return stats


def get_h2h_record(player1, player2, cursor):
    """
    Searches the database for all the matches two give players have played
    Args:
        player1: name of the first player in string format
        player2: name of the second player in string format
        cursor: executable cursor of a database connection
    Returns:
        String of the record of the two given players
    """
    cursor.execute("""SELECT * FROM All_matches WHERE player_name == ?
                   AND opponent_name == ?""",
                   (player1, player2))
    rows = cursor.fetchall()
    if len(rows) == 0:
        return f'{player1} and {player2} have played {len(rows)} times'
    player1_wins = 0
    player2_wins = 0
    for row in rows:
        if row[9] == 'win':
            player1_wins += 1
        elif row[9] == 'lose':
            player2_wins += 1
        else:
            return 'Error calculating wins'
    return (f"{player1} and {player2} have played {len(rows)} "
        f"times and {player1} has won {player1_wins} "
        f"of them and {player2} {player2_wins}")


def get_seasonal_matches(name, season: str, cursor):
    """
    Searches the database for all the matches a given player has played in a given season
    Args:
        name: name of the player in string format
        season: season in string format
        cursor: executable cursor of a database connection
    Returns:
        List of matches
    """
    start_date = f'20{season[:2]}-07-01'
    end_date = f'20{season[2:]}-06-30'
    cursor.execute('SELECT * FROM All_matches WHERE player_name == ?' \
    ' AND date >= ? AND date <= ? ORDER BY date;',
                    (name, start_date, end_date))
    rows = cursor.fetchall()
    return rows

def get_seasonal_stats(name, cursor):
    """
    Calculates all the wins, losses and winrate 
    of a given player for every season
    Args:
        name: player name in string format
        cursor: executable cursor of a database connection
    Returns:
        String of the player name, seasonal wins, losses and seasonal winrate
    """
    seasons = ['2526',
               '2425',
               '2324',
               '2223',
               '2122',
               '2021',
               '1920',
               '1819',
               '1718',
               '1617',
               '1516',
               '1415',
               '1314',
               '1213',
               '1112']
    seasonal_matches = {}

    for season in seasons:
        wins = 0
        losses = 0
        matches = get_seasonal_matches(name, season, cursor)
        if len(matches) == 0:
            seasonal_matches[season] = ['No matches played', '', '', '']
            continue
        for match in matches:
            if match[9] == 'win':
                wins += 1
            else:
                losses +=1
        winrate = (wins / (wins + losses)) * 100
        winrate = str(round(winrate, 2))
        total = wins + losses
        seasonal_matches[season] = [total, wins, losses, f'{winrate}%']
    return seasonal_matches

def get_name(name, cursor):
    """
    Returns the first name in ranking order that most closely matches to a given string
    Args:
        name: string
        cursor: executable cursor of a database connection
    Returns:
        A player name in string format
    """
    name = cursor.execute('SELECT * FROM Ratinglist WHERE name LIKE ? ORDER BY rank',
                           (f'%{name}%', )).fetchone()
    if not name:
        return None
    return name[1]
