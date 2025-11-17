**Ohjelmistotekniikka**
Teen tänne kurssin *ohjelmistotekniikka* palautuksia
By **OttoSFelix**
[gitlog.txt](https://github.com/OttoSFelix/ot-harjoitustyo/blob/main/laskarit/viikko1/gitlog.txt)
[komentorivi.txt](https://github.com/OttoSFelix/ot-harjoitustyo/blob/main/laskarit/viikko1/komentorivi.txt)

# Player Statistics app

- 
## Dokumentaatio

- [vaatimusmäärittely](./harjoitustyo/dokumentaatio/vaatimusmaarittely.md)
- [työaikakirjanpito](./harjoitustyo/dokumentaatio/tyoaikakirjanpito.md)
- [changelog](./harjoitustyo/dokumentaatio/changelog.md)


## Asennus

1. Asenna riippuvuudet komennolla:

```bash
poetry install
```

2. Sovelluksen saa käyntiin komennolla:
komennolla:

```bash
poetry run invoke start
```


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

