# Testausdokumentti
Ohjelmalle on tehty yksikkötestit pääsovelluslogiikan testaamiseen. Sovelluksen excel tiedoston generointi on vaikeaa testata, joten sille ei ole tehty testejä

## Yksikkötestit
Yksikkötestit draw.py, playerinfo.py, db_search.py, web_search.py, match_algoritms.py ja draw_generator.py tiedostoille ovat tässä:
- [Draw_test.py](https://github.com/OttoSFelix/ot-harjoitustyo/blob/main/harjoitustyo/src/tests/Draw_test.py)
- [Pelaaja_test.py](https://github.com/OttoSFelix/ot-harjoitustyo/blob/main/harjoitustyo/src/tests/Pelaaja_test.py)
- [db_search_test.py](https://github.com/OttoSFelix/ot-harjoitustyo/blob/main/harjoitustyo/src/tests/db_search_test.py)
- [web_search_test.py](https://github.com/OttoSFelix/ot-harjoitustyo/blob/main/harjoitustyo/src/tests/web_search_test.py)
- [match_algoritms_test.py](https://github.com/OttoSFelix/ot-harjoitustyo/blob/main/harjoitustyo/src/tests/match_algoritms_test.py)
- [draw_generator_test.py](https://github.com/OttoSFelix/ot-harjoitustyo/blob/main/harjoitustyo/src/tests/draw_generator_test.py)

Kaikkia luokkia ja funktioita on testattu standardeilla yksikkötesteillä, mutta luokkaa Draw on mockattu MagicMock luokkamuuttujalla, koska se hakee tietoa netistä.

## Testikattavuus
Testikattavuus ilman käyttöliittymää on noin 65%. Tämä on hieman alhainen, johtuen siitä, että excel tiedostojen lukemista ja generoimista on vaikea testata.
Alla näkyy testikattavuus:
![](.harjoitustyo/kuvat/testikattavuus.png)


## Järjestelmätestaus
Sovelluksen järjestelmätestaukset on tehty manuaalisesti.

## Asennus ja kongigurointi
Sovellus on kloonattu Cubbli Linuxille virtuaalityöasemassa ja melkinpaasin ssh yhteyden kautta. Sovellus on asennettu [käyttöohjeen](https://github.com/OttoSFelix/ot-harjoitustyo/blob/main/harjoitustyo/dokumentaatio/kayttoohje.md) mukaisella tavalla ja kaikki on toiminut oletetusti.


## Toiminnallisuudet
Kaikki toiminnallisuudet, jotka on listattu [vaatimusmäärittelyyn](https://github.com/OttoSFelix/ot-harjoitustyo/blob/main/harjoitustyo/dokumentaatio/vaatimusmaarittely.md) on testattu manuaalisesti ja kaikki on toiminut kuin pitääkin.
Nämä toiminnallisuudet on käyty läpi paikallisesti, Cubbli Linux virtuaalityöasemassa ja ssh yhteyden kautta toisella koneella. Windowsilla sovellusta ei ole testattu.
