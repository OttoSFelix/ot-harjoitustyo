#Arkkitehtuurikuvaus

## Rakenne

Sovellus toimii lähinnä tietokantatoiminnoilla, tietokantakyselyillä ja statistiikkojen laskemisella, jolloin tällä hetkellä on vain yksi luokkamuuttuja Player, johon tallennetaan pelaajan perustiedot.
Alla näkyy luokan toiminta muiden funktioiden kanssa:

```mermaid
 classDiagram
      Player "*" -->  get_players
      class Player{
          rank
          name
	  id
	  club
	  rating
      }
      get_players --> get_player_matches
      get_player_matches --> rating_database.db
      rating_database.db -- get_h2h_record
      rating_database.db -- get_player_base_stats
      rating_database.db -- top_10_base_stats
```
## Käyttöliittymä

Sovelluksessa kaikki ovat normaaleja käyttäjiä ja sovelluksessa on neljä näkymää; kotinäkymä, ratinglista, draw generator ja head to head calculator
Kotinäkymässä on napit:
- `Ratinglist`
- `Head to head calculator`
- `Draw generator`

Ratinglist käyttää db_search.py:n funktiota get_player_basestats(name) ja palauttaa jokaisen top 100 pelaajan perustatistiikat alkunäkymään. Head to head calculator käyttää db_search.py:n funktiota get_h2h_record(player1, player2) ja palauttaa kahden pelaajan välisen ottelusuhteen näkymään.
Draw generator käyttää draw_generator.py:n funktiota generate(filename, date), joka luo Draw luokkamuuttujan ja kutsuu draw.py:n funktioita luomaan arvonnan. Ennen tätä kutsutaan entries.py:n funktiota get_player_classes_from_file(file_path), joka lukee ilmoittautumiset annetusta ilmoittautumis excel tiedostosta.

 
Head to head recordin näyttäminen käyttäjälle on kuvattu seuraavassa sekvenssikaaviossa:

```mermaid
sequenceDiagram
  actor User
  participant UI
  participant search.py
  participant rating_database.db
  User->>UI: click "Head to head calculator" button
  UI->>search.py: get_h2h_record("Räsänen Aleksi", "Pihkala Arttu")
  search.py->>rating_database.db: SELECT * FROM All_matches WHERE player_name == 'Räsänen Aleksi' AND opponent_name == 'Pihkala Arttu';
  rating_database.db-->>search.py: matches
  search.py-->>UI: head to head record
  UI->UI: display head to head record
```
