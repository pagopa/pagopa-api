# Configurazione di un PSP

La configurazione di un PSP all'interno della piattaforma pagoPA avviene tramite la trasmissione di:

- Il CatalogoDatiInformativi ( CDI) , file xml il cui schema è rappresentato dal file CatalogoDatiInformativi.xsd
- Report della configurazione, file html dove vengono riassunte le iformazioni essenziali dei servizi configurati

## pre-requisite
Il progetto fa uso di due submodules necessari per la generazione del form e per la generazione della documentazione a partire da un xsd.

`git submmodule update --remote xs3p xsd2html2xml` 

## building

all'interno della directory `conf` eseguire i comandi

`xslproc -o ./out/CatalogoDatiInformativi.html ./xs3p/xs3p.xsl CatalogoDatiInformativi.xsd`
Per la compilazione della pagina di documentazione

`xslproc -o ./out/form_CatalogoDatiInformativi.html ./xs2html2xml/form_CatalogoDatiInformativi.html`
per la creazione di una form dinamica.

oppure utilizzare lo script `./build.sh`

## Documentazione

La documentazione del formato CDI è specificata tramite il file CatalogodatiInformativi.xsd , e documentata all'interno della pagina

`./out/CatalogoDatiInformativi.html`

## Compilazione del Catalogo Dati

Per compulare un catalogo dati è possibile aprire tramite il proprio Browser la pagina `./out/form_CatalogoDatiInformativi.html` , compilare il form e presemere il taso `Download`.

Verrà scaricato un file nominato CDISample.xml.
rinominatelo con lo stesso valore del campo IdentificativoFlusso.

## Creazione del Report

Per evidenziare i servizi configurati ,è possibile generare un report HTML utilizzando

`./cdi2html.sh <filenameXML>`

creerà il file
`/out/<filenameXML>.html`

## Invio dei dati di configurazione

Il CDI ed annesso report, devono  essere inviati all'indirizzo helpdesk@pagopa.gov.it da un PSP o da un Mandatario Qualificato nominato dal PSP stesso. L'invio di CDI da soggetti diversi non sarà preso in considerazione.
