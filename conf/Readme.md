# Configurazione di un PSP

La configurazione di un PSP all'interno della piattaforma pagoPA avviene tramite la trasmissione di:

- Il CatalogoDatiInformativiPerPSP ( CDI) , file xml il cui schema è rappresentato dal file `CatalogoDatiInformativiPerPSP.xsd`
- Report della configurazione, file html dove vengono riassunte le iformazioni essenziali dei servizi configurati

## Prerequisiti

- [xsltproc](http://xmlsoft.org/XSLT/xsltproc.html) installato sulla propria macchina 
 
Il progetto inoltre fa uso di due [Git-Tools-Submodules](https://git-scm.com/book/it/v2/Git-Tools-Submodules) necessari per la generazione del form e per la generazione della documentazione a partire da un `xsd`.

Da terminale lanciare il seguente comandio : 

```
git submodule update --init --remote xs3p xsd2html2xml
```

## Build

all'interno della directory `conf` eseguire i comandi

```
xsltproc -o ./out/CatalogoDatiInformativiPerPSP.html ./xs3p/xs3p.xsl CatalogoDatiInformativiPerPSP.xsd
```
> Per la compilazione della pagina di documentazione del _CDI_.

```
xsltproc -o ./out/form_CatalogoDatiInformativiPerPSP.html ./xsd2html2xml/xsd2html2xml.xsl CatalogoDatiInformativiPerPSP.xsd
```
> per la creazione di una form dinamica per il _CDI_.

oppure utilizzare lo script `./build.sh` che fà tutto in automatico.

Se tutto va bene 👍 sotto la dir `out` appariranno i seguenti file `html` : 

```
out/
├── CatalogoDatiInformativiPerPSP.html
└── form_CatalogoDatiInformativiPerPSP.html
```

che possono essere aperti da un qualsiasi browser

## Documentazione

La documentazione del formato CDI è specificata tramite il file `CatalogoDatiInformativiPerPSP.xsd` , e documentata all'interno della pagina

`./out/CatalogoDatiInformativiPerPSP.html`

## Compilazione del Catalogo Dati

Per compilare un catalogo dati è possibile aprire tramite il proprio browser la pagina [form_CatalogoDatiInformativiPerPSP.html](./out/form_CatalogoDatiInformativiPerPSP.html), 
compilare il form e premere il tasto **OK**.

Verrà scaricato un file nominato `CDISample.xml`, rinominarlo con lo stesso valore del campo _IdentificativoFlusso_.

## Creazione del Report

Per evidenziare i servizi configurati ,è possibile generare un report HTML utilizzando

`./cdi2html.sh <filenameXML>`

creerà il file
`/out/<filenameXML>.html`

## Invio dei dati di configurazione

Il CDI ed annesso report, devono  essere inviati all'indirizzo `helpdesk@pagopa.gov.it` da un PSP o da un Mandatario Qualificato nominato dal PSP stesso. 
L'invio di _CDI_ da soggetti diversi non sarà preso in considerazione.
