import requests
from bs4 import BeautifulSoup
from database_connection import get_database_connection
from playerinfo import Player


def initialize_matches_table():
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute('DROP TABLE IF EXISTS Matches')
    cursor.execute('CREATE TABLE Matches(date text, match_type text, division text, player_name text, player_club text, opponent_name text, opponent_club text, score text, total text, outcome text)')
    connection.commit()
    print('init tehty')


def top_date():

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

def get_newest_rating():

    date = top_date().split('.')
    date.reverse()
    seperator = '-'
    date = seperator.join(date)
    print(date)

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

    connection = get_database_connection()
    cursor = connection.cursor()
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
        cursor.execute('INSERT INTO Ratinglist(rank, name, id, club, rating) values(?, ?, ?, ?, ?)', (rank, name, id, club, rating))
        connection.commit()


def total_score(score):
    score = score.split(',')
    for s in range(len(score)):
        if score[s] == '':
            score[s] = 0
        score[s] = int(score[s])
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
    return(f'{player}-{opponent}', outcome)
    



def reverse_score(score):
    score = score.split(',')
    for s in range(len(score)):
        score[s] = int(score[s])
        score[s] = -score[s]
    for s in range(len(score)):
        score[s] = str(score[s])
    return ','.join(score)


def get_players():
    players = []
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Ratinglist')
    rows = cursor.fetchall()
    for row in rows:
        players.append(Player(row[0], row[1].strip(), row[2], row[3], row[4]))
    return players

def get_player_matches_test(id, name):
    url = "https://www.sptl.fi/sptl_uudet/wp-content/plugins/sptl-plugin/httpreq/lataa_csv.php"

    seasons = ['2526', '2425', '2324', '2223', '2122', '2021', '1920', '1819', '1718', '1617', '1516', '1415', '1314', '1213', '1112']

    for season in seasons:
        print(season)
        data = {
            "alkupvm": "17.08.2000",   
            "loppupvm": "25.10.2100",  
            "kausi": season,           
            "sarjaottelut": "1",
            "kilpailut": "1",
            "seura": "PT Espoo",
            "tunnus": id,     
            "kilpailu": ""
        }

        r = requests.post(url, data=data)
        r.raise_for_status()
        with open('player.txt', 'wb') as file:
            file.write(r.content)
        
        matches = []
        with open('player.txt') as file:
            for row in file:
                matches.append(row.strip())
        
        if len(matches) == 0:
            continue
        matches.pop(0)


        for row in matches:
            row = row.split('|')
            lista = []
            print(row)
            if len(row) > 5 and row[8] == '  ':
                date = row[0].strip()
                if '00:00:00' in date:
                    date = date.removesuffix(' 00:00:00')
                match_type = row[1].strip()
                division = row[2].strip()
                lista.append(row[6].strip())
                print(lista)

                if 'wo' in row[6].strip() or 'wo' in row[10].strip():
                    continue
                
                if row[6].strip() == name:
                    score = row[14].strip()
                    if 'wo' in score or 'rtd' in score:
                        continue
                    player_name = row[6].strip()
                    player_club = row[7].strip()
                    opponent_name = row[10].strip()
                    opponent_club = row[11].strip()
                    total, outcome = total_score(score)

                elif row[10].strip() == name:
                    score = row[14].strip()
                    if 'wo' in score or 'rtd' in score:
                        continue
                    player_name = row[10].strip()
                    player_club = row[11].strip()
                    opponent_name = row[6].strip()
                    opponent_club = row[7].strip()
                    score = reverse_score(score)
                    total, outcome = total_score(score)
                
                
                else:
                    print('virhe playername osiossa')
                
                connection = get_database_connection()
                cursor = connection.cursor()
                cursor.execute('INSERT INTO Matches(date, match_type, division, player_name, player_club, opponent_name, opponent_club, score, total, outcome) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (date, match_type, division, player_name, player_club, opponent_name, opponent_club, score, total, outcome))
            else:
                continue
        connection.commit()
        

def get_player_matches(player: Player):
    connection = get_database_connection()
    cursor = connection.cursor()
    url = "https://www.sptl.fi/sptl_uudet/wp-content/plugins/sptl-plugin/httpreq/lataa_csv.php"

    seasons = ['2526', '2425', '2324', '2223', '2122', '2021', '1920', '1819', '1718', '1617', '1516', '1415', '1314', '1213', '1112']

    for season in seasons:
        data = {
            "alkupvm": "17.08.2000",   
            "loppupvm": "25.10.2100",  
            "kausi": season,           
            "sarjaottelut": "1",
            "kilpailut": "1",
            "seura": "PT Espoo",
            "tunnus": player.id,     
            "kilpailu": ""
        }

        r = requests.post(url, data=data)
        r.raise_for_status()
        with open('player.txt', 'wb') as file:
            file.write(r.content)
        
        matches = []
        with open('player.txt') as file:
            for row in file:
                matches.append(row.strip())
        
        if len(matches) == 0:
            continue
        matches.pop(0)


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

                elif row[10].strip() == player.name:
                    score = row[14].strip()
                    if 'wo' in score or 'rtd' in score:
                        continue
                    player_name = row[10].strip()
                    player_club = row[11].strip()
                    opponent_name = row[6].strip()
                    opponent_club = row[7].strip()
                    score = reverse_score(score)
                    total, outcome = total_score(score)
                else:
                    print('virhe playername osiossa')
                
                cursor.execute('INSERT INTO Matches(date, match_type, division, player_name, player_club, opponent_name, opponent_club, score, total, outcome) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (date, match_type, division, player_name, player_club, opponent_name, opponent_club, score, total, outcome))
            else:
                continue
        connection.commit()
        

initialize_matches_table()
x = 1
for player in get_players():
    get_player_matches(player)
    print(x)
    x += 1

