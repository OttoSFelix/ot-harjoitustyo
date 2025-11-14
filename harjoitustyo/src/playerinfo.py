class Player:
    def __init__(self, rank, name, id, club, rating):
        self.rank = rank
        self.name = name
        self.club = club
        self.rating = rating
        self.id = id

    def __str__(self):
        return(f'{self.rank}, {self.name}, {self.id}, {self.club}, {self.rating}')
        