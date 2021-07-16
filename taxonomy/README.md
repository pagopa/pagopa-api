## Conversione Tassonomia

La presente utility permette di ottenere la versione `JSON` della Tabella Tassonomica (`.xlsx`) presente presso il sito [PagoPA](https://drive.google.com/file/d/13xOd__Qd4pwKHr3wjE-73NAB2O7UKmIt/view
)

## Prerequisiti 

- [xlsx2csv](https://pypi.org/project/xlsx2csv/)
- [wget](https://www.gnu.org/software/wget/)

Installare i seguenti pacchetti:
```
$ pip install xlsx2csv
```
> Valido su sistemi *nix like
```
$ brew install wget
```
> Valido per sistemi MacOS che hanno [brew](https://brew.sh/index_it)

## Conversione 

Eseguire da terminale: 

```
$ make all
```

Esempio risultato:

```json
[
    {
      "TIPO SERVIZIO": "Rendite catastali (ICI, IMU, TUC, ecc.)",
      "DESCRIZIONE TIPO SERVIZIO": "L'Imu dal 2012 ha sostituito l'ICI. La legge 147/2013 inserisce l'IMU, insieme alla Tasi e alla Tari nella IUC (imposta unica comunale). La legge di bilancio 2020 ha modificato la disciplina dell'Imu-Tasi eliminando quest'ultima e accorpandola allaa \"nuova IMU\". Il presupposto dell'IMU \u00e8 il possesso di fabbricati, escluse le abitazioni principali; aree fabbricabili e terreni agricoli.",
      "VERSIONE TASSONOMIA": "08",
      "DATI SPECIFICI DI INCASSO": "9/0101100IM/",
      "DATA INIZIO VALIDITA": "01/01/1900",
      "DATA FINE VALIDITA": "01/01/2080"
    },
	...
]
```

All'interno dello script `convert_to_json.py` è possibile modificare i campi/colonne del file `.xlsx` da convertire.





