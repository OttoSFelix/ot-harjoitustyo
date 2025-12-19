#Arkkitehtuurikuvaus

## Rakenne

Alla on korkean tason arkkitehtuurikuvaus sovelluksen pääsovelluslogiikasta

```mermaid
graph TD
    User((User)) -->|Interacts with| GUI

    subgraph View_Layer [User Interface]
        direction TB
        GUI[gui.py<br>Main Interface Manager]
        HomeView[home_view.py]
        DrawView[drawview.py]
        RatingView[rating_view.py]
        H2HView[h2h_view.py]
    end

    subgraph Logic_Layer [Application Logic]
        direction TB
        Draw[draw.py<br>Draw Logic Core]
        DrawGen[draw_generator.py<br>Visual Generation]
        Algo[match_algoritms.py<br>Math/Sorting Logic]
        Init[initialize.py<br>System Setup]
    end

    subgraph Data_Layer [Data Access]
        direction TB
        DBConn[database_connection.py<br>SQLite Connection]
        Entries[entries.py<br>Entry Repository]
        PlayerInfo[playerinfo.py<br>Player Model]
        DBSearch[db_search.py<br>Local Search]
        WebSearch[web_search.py<br>Web Scraper]
    end

    subgraph External [External Storage]
        SQLite[(SQLite Database)]
        TxtFiles[Text files<br>possible_classes.txt]
        WebWorld[Internet]
    end

    GUI --> HomeView
    GUI --> DrawView
    GUI --> RatingView
    GUI --> H2HView

    DrawView --> DrawGen
    RatingView --> DBSearch
    RatingView --> WebSearch
    H2HView --> WebSearch

    DrawGen --> Draw
    Draw --> Entries
    Draw --> PlayerInfo
    Draw --> SQLite
    Draw --> TxtFiles
    Entries -->|Writes| DBConn
    
    DBSearch --> DBConn
    DBSearch --> PlayerInfo
    Init -->|Creates Tables| DBConn
    DBConn <--> SQLite

    WebSearch <-->|Fetches Data| WebWorld
    WebSearch --> Algo


```

Sovellus toimii lähinnä tietokantatoiminnoilla, tietokantakyselyillä ja statistiikkoja laskevilla algoritmeilla, tärkein luokkamuuttuja on Player, johon tallennetaan pelaajan perustiedot.
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
  UI->User: display head to head record to user
  UI->UI: display head to head record
```


##Sovelluslogiikka

Applikaation pääsovelluslogiikan hoitaa lähinnä kolme tiedostoa: db_search.py, web_search.py ja match_algoritms.py.
db_search.py nimensä mukaisesti hakee tietoja tietokannasta ja palauttaa niitä ylempien tasojen komponenteille, esim. jos käytetään head to head calculatoria. web_search.py hakee pelaajien pelaamia matseja ja ratinglistoja netistä. Pelaajien pelaamat matsit haetaan kun suoritetaan initialize.py (invoke init).
web_search.py tekee pyyntöjä match_algoritms.py:lle jäsentääkseen matsien tuloksia tietokantaan kirjoittamista varten. 
Näiden kolmen tiedoston toiminta on kuvattu alla:

```mermaid
flowchart TD
   db_search---|reads|[(database)]
   web_search-- inserts -->[(database)]
   web_search --- match_algoritms
```
  
