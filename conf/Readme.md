# Configurazione di un PSP

La configurazione di un PSP all'interno della piattaforma pagoPA avviene tramite la trasmissione di un file xml il cui schema è riportato all'intenro di CatalogoDatiInformativi.xsd

## Premessa
Per poter essere configurati all'interno della piattaforma è necessario che sia stata abilitata la connessione e l'autenticazione.

### Connessione ed autenticazione
La piattaforma pagoPA è raggiungibile via :

- public-internet all'indirizzo XXXX tramite con connessione HTTPS con mutua autenticazione
- VPN dedicata

# CDI - documentazione
La documentazione del CDI è definita per mezzo dello schema XSD presente all'interno di questa directory e fruibile tramite pagina HTML generata come segue

`xslproc -o ./out/CatalogoDatiInformativi.html ./xs3p/xs3p.xsl CatalogoDatiInformativi.xsd`

# CDI - Compilazione
la compilazione del CDI può essere effettuata tramite una form costruita a partire dallo stesso XSD e creata 
`xslproc -o ./out/form_CatalogoDatiInformativi.html ./xs2html2xml/form_CatalogoDatiInformativi.html` 

Il form è disponibile al seguente indirizzo XXX

## Compilazione del Catalogo Dati 
Il catalogo dati informativi ( CDI ) rappresenta l'insieme delle informazioni necessaria 

