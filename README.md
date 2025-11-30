**Ohjelmistotekniikka**
Teen tänne kurssin *ohjelmistotekniikka* palautuksia
By **OttoSFelix**

# Player Statistics app
Applikaatiolla pystyy tällä hetkellä hakemaan top 100 pelaajien perustatistiikkoja ja pelaajien välisiä ottelusuhteita
 
## Dokumentaatio

- [arkkitehtuurikuvaus](./harjoitustyo/dokumentaatio/arkkitehtuuri.md)
- [käyttöohje](./harjoitustyo/dokumentaatio/kayttoohje.md)
- [vaatimusmäärittely](./harjoitustyo/dokumentaatio/vaatimusmaarittely.md)
- [työaikakirjanpito](./harjoitustyo/dokumentaatio/tyoaikakirjanpito.md)
- [changelog](./harjoitustyo/dokumentaatio/changelog.md)


## Asennus

1. Asenna riippuvuudet komennolla:

```bash
poetry install
```

2. Ennen käynnistämistä valmistele tietokanta komennolla:
```bash
poetry run invoke init
```
*tähän menee muutama minuutti*

3. Sovelluksen saa käyntiin komennolla:
komennolla:

```bash
poetry run invoke start
```

Tämä avaa ikkunan (kotinäyttöön) jossa pyörii sovelluksen graafinen käyttöliittymä

## Muut komentorivitoiminnot

### Testaus

Testit suoritetaan komennolla:

```bash
poetry run invoke test
```

### Testikattavuus

Testikattavuusraportin saa komennolla:

```bash
poetry run invoke coverage-report
```

