# Kayttoohje

Katso ensin readme.md tiedostosta käynnistys
Varmista, että invoke init on runattu, ennen sovelluksen ensimmäistä käyttöä
## Toiminta
- *Huom nimet tulee antaa formaatissa Sukunimi Etunimi*
- Sovelluksella pystyy hakemaan pelaajan perusstatistiikat nimen mukaan, hakea kahden pelaajan välisen ottelusuhteen ja luoda arvontoja kilpailuihin ilmottautumislistan perusteella. Perusstatistiikkojen katselua varten painetaan nappia `Ratinglist`, ottelusuhdetta varten painetaan nappia `Head to head record calculator`. 

### Ratinglist näkymä
Tässä näkymässä on listattuna suomen top 100 pelaajan voittoprosentit, voitot ja häviöt. Oikeassa reunassa on scroll bar jolla voidaan scrollata näkymää. 
- Yksittäisen pelaajan kausikohtaiset statistiikat voidaan hakea oikeasta yläkulmasta olevasta hakukentästä.
- Kaikki pelaajat saadaan taas näkyviin painamalla `Show All` painiketta.
- Uusimpaan ratinglistaan voidaan päivittää painamalla oikeasta yläkulmasta nappia `Update to newest rating`.
- Takaisin kotinäyttöön päästään painamalla `Home` painiketta.
- Mikä tahansa nimi Ratinglist sivun top-100 sisällä pitäisi toimia hakukentässä. Nimet tulee antaa formaatissa Sukunimi Etunimi.

### Head to head record calculator näkymä
Tässä näkymässä haetaan kahden pelaajan välinen ottelusuhde
- Nimet pitää antaa muodossa Sukunimi Etunimi


### Draw generator näkymä
Tässä näkymässä voidaan luoda arvontoja kilpailuihin. Tätä varten tarvitaan vain ilmoittautumislista ja päivämäärä.
- Ilmoittautumislista täytyy olla excel tyylinen taulukko, jossa yhden pelaajan pelaamat luokat ovat yhdellä rivillä.
- Samalla rivillä voi myös lukea pelaajan seura, sähköposti ym. turhaa, mutta se ei ole tarpeellista, eikä häiritse generointia.
- Nimet ilmoittautumislistassa täytyy olla Sukunimi Etunimi formaatissa. Nimien ei tarvitse olla ratinlistan top 100 sisällä, vaan nimet voivat olla mitä tahansa [ratinglistasta](https://www.sptl.fi/sptl_uudet/?page_id=7339) löytyviä.
- Mahdolliset luokat näkyvät tiedostossa [possible_classes.txt](https://github.com/OttoSFelix/ot-harjoitustyo/blob/main/harjoitustyo/src/possible_classes.txt)
- Esimerkki riittävästä ilmoittautumislistan formaatista on näkyy tässä [tiedostossa](https://docs.google.com/spreadsheets/d/1j0SGmPF6JZUfQkB186y4-JKSjH8D8fcN4k2_D1CT_Qs/edit?gid=0#gid=0)
- Luokassa pitää olla vähintään 4 osallistujaa, jotta luokka järjestetään.

- Arvonnan generointia varten liitetään ilmoittautumislista napista `Select file`, lisätään päivämäärä (kannattaa käyttää 30.11.2025. Voi myös käyttää vanhempaa [ratingjulkaisua](https://www.sptl.fi/sptl_uudet/?page_id=7344)), painetaan nappia `Generate` ja generoitu excel tiedosto pitäisi avautua itsestään.
- Tässä hyvä [ilmoittautumislista](https://docs.google.com/spreadsheets/d/1I24b7MyYIPJGKOY6xnsREIiVlbcUpDfXaoaAagiFpWo/edit?gid=1493718920#gid=1493718920) jota voi käyttää arvontojen generoinnin testaamiseen.
- Takaisin kotinäyttöön päästään painamalla `Home` painiketta.
