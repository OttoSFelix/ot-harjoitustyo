import requests
from bs4 import BeautifulSoup
from database_connection import get_database_connection
from playerinfo import Player

def initialize_matches_table():
    """
    Creates the necessary tables in the database
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


def top_date():
    
    """
    Fetches the date of the most recent rating publish from www.sptl.fi 
    Returns:
        str: The text content of the date element if found (e.g., "1.1.2023").
        None: If the date element could not be found or if a request error occurred.
    """
    url = "https://www.sptl.fi/sptl_uudet/?page_id=7344"

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        selector = ".entry-content tr:nth-child(2) td a"

        date_element = soup.select_one(selector)

        if date_element:
            date_text = date_element.get_text()
            return date_text
        else:
            print("Could not find the date")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")

def get_newest_rating(cursor):
    """
    Inserts the most recent dating publish into the database
    """
    date = top_date().split('.')
    date.reverse()
    seperator = '-'
    date = seperator.join(date)
    main = 'https://www.sptl.fi'
    url = f"{main}/sptl_uudet/wp-content/plugins/sptl-plugin/ratingjulkaisut.php?pvm={date}"

    payload = {
        "csv": "csv"
    }

    print(f"Submitting form to {url}...")

    lista = []
    response = requests.post(url, data=payload)
    response.raise_for_status()

    with open('ratinglist', 'wb') as file:
        file.write(response.content)

    with open('ratinglist') as file:
        for row in file:
            lista.append(row.strip())

    lista.pop(0)
    lista.pop(0)
    lista.pop(0)
    lista.pop(0)
    cursor.execute('DROP TABLE IF EXISTS Ratinglist')
    cursor.execute('CREATE TABLE Ratinglist(rank int, name text, id text, club text, rating int)')
    for row in lista:
        row = row.split(';')
        rank = row[0]
        name = row[1]
        id = row[2]
        club = row[4]
        rating = row[5]
        if not name or not club:
            continue
        # tee mahdolliset pelaaja luokat
        cursor.execute("""INSERT INTO Ratinglist(rank, name, id, club, rating)
                       values(?, ?, ?, ?, ?)""",
                       (rank, name, id, club, rating))


def total_score(score):
    """
    Returns the total score of a match based on the points
    
    Args:
        score: point score of a match in string format eg. '7, -8, 9, 6'
    
    Returns:
        total score in sets eg. 3-1 if no points given in an acceptable format
        fail if points not given in an acceptable format
    """
    score = score.split(',')
    try:
        for n, s in enumerate(score):
            if s == '':
                score[n] = 0
            score[n] = int(score[n])
        player = 0
        opponent = 0
        for s in score:
            if s >= 0:
                player += 1
            else:
                opponent +=1
        if player > opponent:
            outcome = 'win'
        else:
            outcome = 'lose'
        return (f'{player}-{opponent}', outcome)
    except:
        return ('fail', 'fail')



def reverse_score(score):
    
    try:
        score = score.split(',')
        for n, s in enumerate(score):
            if s == '':
                score[n] = 0
            score[n] = int(score[n])
            score[n] = -score[n]
        for n, s in enumerate(score):
            score[n] = str(s)
        return ','.join(score)
    except:
        return 'fail'


def get_players(cursor):
    players = []
    cursor.execute('SELECT * FROM Ratinglist')
    rows = cursor.fetchall()
    for row in rows:
        players.append(Player(row[0], row[1].strip(), row[2], row[3], row[4]))
    return players

def get_nth_players(rank, cursor):
    players = []
    cursor.execute('SELECT * FROM Ratinglist WHERE rank <= ?', (rank,))
    rows = cursor.fetchall()
    for row in rows:
        players.append(Player(row[0], row[1].strip(), row[2], row[3], row[4]))
    return players

def get_player_matches(player: Player, connection, session):
    cursor = connection.cursor()
    url = "https://www.sptl.fi/sptl_uudet/wp-content/plugins/sptl-plugin/httpreq/lataa_csv.php"
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
    for season in seasons:
        data = {
            "alkupvm": "17.08.2000",
            "loppupvm": "25.10.2100",
            "kausi": season,
            "sarjaottelut": "1",
            "kilpailut": "1",
           "seura": player.club,
            "tunnus": player.id,
            "kilpailu": ""
        }
        try:
            r = session.post(url, data=data, timeout=10)
        except requests.exceptions.Timeout:
            print(f"  -> Timeout error for season {season}. Skipping.")
            continue
        except requests.exceptions.RequestException as e:
            print(f"  -> Network error: {e}")
            continue
        r.raise_for_status()
        content = r.text.strip()
        matches = content.splitlines()

        if len(matches) <= 1:
                continue

        for row in matches:
            row = row.split('|')
            if len(row) > 5 and row[8] == '  ':
                date = row[0].strip()
                if '00:00:00' in date:
                    date = date.removesuffix(' 00:00:00')
                match_type = row[1].strip()
                division = row[2].strip()

                if 'wo' in row[6].strip() or 'wo' in row[10].strip():
                    continue

                if row[6].strip() == player.name:
                    score = row[14].strip()
                    if 'wo' in score or 'rtd' in score:
                        continue
                    player_name = row[6].strip()
                    player_club = row[7].strip()
                    opponent_name = row[10].strip()
                    opponent_club = row[11].strip()
                    total, outcome = total_score(score)
                    if total == 'fail':
                        print('parsing error')
                        continue

                elif row[10].strip() == player.name:
                    score = row[14].strip()
                    if 'wo' in score or 'rtd' in score:
                        continue
                    player_name = row[10].strip()
                    player_club = row[11].strip()
                    opponent_name = row[6].strip()
                    opponent_club = row[7].strip()
                    score = reverse_score(score)
                    if score == 'fail':
                        print('parsing error')
                        continue
                    total, outcome = total_score(score)
                    if total == 'fail':
                        print('parsing error')
                        continue
                else:
                    print('virhe playername osiossa')
                    continue
                cursor.execute("""INSERT INTO All_matches
                               (date, match_type, division, player_name, player_club, opponent_name, opponent_club, score, total, outcome)
                                values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                (date, match_type, division, player_name, player_club,
                                 opponent_name, opponent_club, score, total, outcome))
            else:
                continue
    connection.commit()


def get_player_base_stats(name, cursor):
    name = name.strip()
    cursor.execute('SELECT * FROM Ratinglist WHERE name == ?', (name ,))
    row = cursor.fetchall()
    if not row:
        return f"Couldn't find player named {name}"
    row = row[0]
    player = Player(row[0], row[1], row[2], row[3], row[4])
    cursor.execute('SELECT * FROM All_matches WHERE player_name == ? ORDER BY date', (player.name, ))
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
    return f'{player1} and {player2} have played {len(rows)} times and {player1} has won {player1_wins} of them and {player2} {player2_wins}'


def get_seasonal_matches(name, season: str, cursor):
    start_date = f'20{season[:2]}-07-01'
    end_date = f'20{season[2:]}-06-30'
    cursor.execute('SELECT * FROM All_matches WHERE player_name == ? AND date >= ? AND date <= ? ORDER BY date;', (name, start_date, end_date))
    rows = cursor.fetchall()
    return rows

def get_seasonal_stats(name, cursor):
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
    name = cursor.execute('SELECT * FROM Ratinglist WHERE name LIKE ? ORDER BY rank', (f'%{name}%', )).fetchone()
    if not name:
        return None
    return name[1]