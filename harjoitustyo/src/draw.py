from entries import get_player_classes_from_file
from playerinfo import Player
import os
import random

script_dir = os.path.dirname(os.path.abspath(__file__))

class Draw:
    def __init__(self, file_name, connection):
            self.file_name = file_name
            self.connection = connection
            self.cursor = self.connection.cursor()
            self.success = True
            self.create_classes()

    def get_possible_classes(self):
        """
        Gets all the possible classes from possible_classes.txt
        Returns:
            list of all the possible classes
        """
        classes = []
        with open(script_dir + '/possible_classes.txt') as file:
            for row in file:
                classes.append(row.strip())
        return classes

    def create_classes(self):
        """
        Inserts each player entry per class as a row in the database
        """
        TIEDOSTO_POLKU = os.path.join(script_dir, self.file_name)
        entries = get_player_classes_from_file(TIEDOSTO_POLKU)
        cursor = self.cursor
        cursor.execute('DROP TABLE IF EXISTS Entries')
        cursor.execute('CREATE TABLE Entries(class, player)')
        all_classes = set()
        possible_classes = self.get_possible_classes()
        try:
            for player, classes in entries.items():
                for c in classes:
                    if ',' in c:
                        cls = c.split(',')
                        for luokka in cls:
                            all_classes.add(luokka.strip())
                            cursor.execute('INSERT INTO Entries(class, player) values(?, ?)', (luokka.strip(), player.strip()))
                    else:
                        all_classes.add(c.strip())
                        cursor.execute('INSERT INTO Entries(class, player) values(?, ?)', (c.strip(), player.strip()))
            self.connection.commit()
        except:
            self.success = False
            return

        all_classes = list(all_classes)
        for c in all_classes:
            c = c.strip()
            if c not in possible_classes:
                cursor.execute('DELETE FROM Entries WHERE class == ?', (c, ))

            
            cursor.execute('SELECT * FROM Entries WHERE class == ? GROUP BY player', (c, ))
            rows = cursor.fetchall()
            self.connection.commit()
            if len(rows) < 4:
                cursor.execute('DELETE FROM Entries WHERE class == ?', (c, ))
        self.connection.commit()


    def next_pool_size(self, player_count):
        """
        Determines the size of the next pool 
        depending on the amount of players left
        Args:
            player_count: remaining players
        Returns:
            integer of the size of the next pool 
        """
        if player_count == 0:
            return 0
        if player_count % 4 == 0:
            return 4
        if player_count % 5 == 0:
            return 5
        if player_count >= 7:
            return 4
        if player_count % 3 == 0:
            return 3

    def pool_sizes(self, total_players):
        """
        Determines the size of every pool
        Args:
            total_players: total amount of players in a class
        Returns:
            list of the integers of the pool sizes sorted
        """
        remaining = total_players
        next_size = self.next_pool_size(total_players)
        pools = []
        while next_size > 0:
            remaining -= next_size
            pools.append(next_size)
            next_size = self.next_pool_size(remaining)
        return sorted(pools, reverse=True)

    def player_rating(self, player):
        """
        Gets the rating of a given player from the database
        Args:
            player: player name
        Returns:
            Integer of the rating of the player

        """
        self.cursor.execute('SELECT rating FROM Competitionrating WHERE name LIKE ? ORDER BY rating DESC', (f'%{player}%', ))
        row = self.cursor.fetchone()
        if row:
            rating = row[0]
        else:
            rating = 700
        return rating

    def get_player(self, player):
        """
        Creates a Player -class variable from a player 
        that is most similar to a given string in ranking order
        Args:
            player: string
        Returns:
            Player -class variable
        """
        self.cursor.execute('SELECT * FROM Competitionrating WHERE name LIKE ? ORDER BY rating DESC', (f'%{player}%', ))
        row = self.cursor.fetchone()
        if row:
            player = Player(row[0], row[1].strip(), row[2], row[3], row[4])
        else:
            player = Player(0, player, 'PlaceholderID', 'ei seuraa', 700)
        return player


    def draw_for_class(self, clas):
        """
        Creates the draw for a class
        Args:
            clas: the name of the class in string format
        Returns:
            dictionary of all the pools containing the players
            from the given class

        """
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Å', 'Ä', 'Ö']

        cursor = self.cursor
        cursor.execute('SELECT * FROM Entries WHERE class == ? GROUP BY player', (clas, ))
        rows = cursor.fetchall()
        players = [row[1] for row in rows]
        players.sort(key=lambda x: self.player_rating(x), reverse=True)

        pools = self.pool_sizes(len(players))
        seedings = []
        remaining = False
        x = len(pools)

        if x == 0:
            return {}
            
        start_index = 0
        while start_index + x <= len(players):
            seedings.append(players[start_index:start_index + x])
            start_index += x
        
        if start_index < len(players):
            remaining = players[start_index:]
        # poolien ykkössijoitetut saavat järjestyksessä ensimmäiset sijat
        final_draw = {f'Pooli {letters[x]}': [] for x in range(len(pools))}
        for x in range(len(pools)):
            player = seedings[0][x]
            player = self.get_player(player)
            final_draw[f'Pooli {letters[x]}'].append({'name': player.name, 'rating': player.rating, 'club': player.club})
        seedings.pop(0)

        # muut poolien pelaajat jaetaan sattuman varaisesti
        for seed in seedings:
            for x in range(len(seed)):
                player_name = random.choice(seed)
                player = self.get_player(player_name)
                final_draw[f'Pooli {letters[x]}'].append({'name': player.name, 'rating': player.rating, 'club': player.club})
                seed.remove(player_name)
        
        #jäljelle jääneet pelaajat sijoitetaa ensimmäisiin mahdollisiin pooleihin
        if remaining:
            random.shuffle(remaining)
            for x in range(len(remaining)):
                player = remaining[x]
                player = self.get_player(player)
                final_draw[f'Pooli {letters[x]}'].append({'name': player.name, 'rating': player.rating, 'club': player.club})

        return final_draw
