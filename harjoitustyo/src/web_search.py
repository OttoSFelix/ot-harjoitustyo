import requests
from bs4 import BeautifulSoup
from datetime import datetime
from playerinfo import Player
from match_algoritms import total_score, reverse_score


def top_date():
    """
    Fetches the date of the most recent rating publish from www.sptl.fi
    Args:
        None
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
        print("Could not find the date")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")

def get_rating(date = None, connection = None):
    """Inserts the most recent ratinglist into the database if no date is given.
    If a date is given, inserts a dated ratinglist into the database for draw generation
    Args:
        date: a given date for draw generation
        connection: database connection
    Returns:
        None
    """

    cursor = connection.cursor()
    if not date:
        dated = False
    else:
        dated = True
    date = top_date().split('.')
    date.reverse()
    seperator = '-'
    date = seperator.join(date)

    url = f"https://www.sptl.fi/sptl_uudet/wp-content/plugins/sptl-plugin/ratingjulkaisut.php?pvm={date}"

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
    if not dated:
        cursor.execute('DROP TABLE IF EXISTS Ratinglist')
        cursor.execute('CREATE TABLE Ratinglist(rank int, name text,' \
        ' id text, club text, rating int)')
    else:
        cursor.execute('DROP TABLE IF EXISTS Competitionrating')
        cursor.execute('CREATE TABLE Competitionrating(rank int, name text,' \
        ' id text, club text, rating int)')
    for row in lista:
        row = row.split(';')
        rank = row[0]
        name = row[1]
        id = row[2]
        club = row[4]
        rating = row[5]
        if not name or not club:
            continue
        if not dated:
            cursor.execute('INSERT INTO Ratinglist(rank, name, id, club, rating) values(?, ?, ?, ?, ?)',
                            (rank, name, id, club, rating))
        else:
            cursor.execute('INSERT INTO Competitionrating(rank, name, id, club, rating) values(?, ?, ?, ?, ?)',
                           (rank, name, id, club, rating))
        connection.commit()


def validate_date(date = top_date()):
    try:
        # %d = day, %m = month, %Y = 4-digit year
        datetime.strptime(date, '%d.%m.%Y')
        return
    except ValueError:
        return 'Invalid date, using newest rating'

def get_player_matches(player: Player, connection, session):
    """
    Fetches all the matches of a given player from www.sptl.fi
    Args:
        player: Player -class variable
        connection: database connection
        session: Session -class variable that establishes a network communication session
    Returns:
        None
    """
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
