# Torretxea euskal torrent zerbitzari scripta

Torrent zerbitzariko media fitxategiak automatikoki irakurri eta sailkatu ostean dagokien torrent fitxategia sortu eta partekatzen duen kode zatia da honako hau.

## Dependentziak

* Python 2.7
* Transmission-daemon
* Delegator

## Konfigurazio fitxategia

Sortu script karpetaren barruan conf.yml izeneko fitxategi bat. Ondorengo egitura izan behar du:
```
paths:
  FILM_PATH_TO_SHARE: ""
  FILM_PATH_MEDIA_STORE: ""
  SERIES_PATH_TO_SHARE: ""
  SERIES_PATH_MEDIA_STORE: ""

transmission:
  TORRENT_STORE_PATH: ""
  TRANSMISSION_AUTH: ""
  COMMENT: ""
```

## Torrent izenen egitura

Automatizazioak funtziona dezan, beharrezkoa da fitxategiek egitura hau errespetatzea.

### Filmeak

American_beauty-(1999)-[1080p][EU][Sub_EN][Torretxea].mkv

`Filemearen_izena`-(`Urtea`)-[`Bereizmena`][`Audio_hizkuntza`][Sub_`Azpitituluen_hizkuntza`][Torretxea]

### Telesailak

One_Piece-S01E11-(1999)-[720p][JP_EU][Sub_EN][Torretxea].avi

`Telesailaren_izena`-`Denboraldi_eta_atal_zenbakia`-(`Urtea`)-[`Bereizmena`][`Audio_hizkuntza`][Sub_`Azpitituluen_hizkuntza`][Torretxea]

## Exekutatzeko

```python scripts/create_torrent.py```
