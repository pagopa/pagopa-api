# Configurazione di un PSP

La configurazione di un PSP all'interno della piattaforma pagoPA avviene tramite la trasmissione di un file xml il cui schema è riportato all'intenro di CatalogoDatiInformativi.xsd

## Premessa

Per poter essere configurati all'interno della piattaforma è necessario che sia stata abilitata la connessione e l'autenticazione.

### Connessione ed autenticazione

La piattaforma pagoPA è raggiungibile via :

- public-internet
- VPN dedicata

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
Verrà scaricato un file nominato CDISample.xml , rinominatelo con lo stesso valore del campo IdentificativoFlusso.

## Invio del Catalogo Dati

Il CDI deve essere inviato all'indirizzo helpdesk@pagopa.gov.it da un PSP o da un Mandatario Qualificato nominato dal PSP. L'invio di CDI da soggetti diversi non sarà preso in considerazione.
