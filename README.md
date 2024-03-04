> **NOTA**
Quanto riportato nel presente branch del repository è valido dal momento della pubblicazione della corrispondente versione delle SANP.

<img width="150px"  src="https://www.pagopa.gov.it/assets/images/pagopa-logo.png" title="pagoPa" alt="pagoPa">

# pagopa-specifichepagamenti-schemi 
> definizione di tutte le interfacce (esposte e richieste) per la connessione con il sistema pagoPA.
> Tutti gli schemi XSD, WSDL e swagger seguono release diverse dalle SANP

Il repository è suddiviso nelle seguenti sezioni:

* **wsdl**: contiene la definizione delle interfacce _SOAP_ valide per la connessione al _Nodo dei Pagamenti pagoPA_ 
mediante la nuova modalità diretta esposta su Internet (_Nuova Connettività_)
* **gad**: contiene la definizione delle interfacce _SOAP_ valide per la connessione al _Nodo dei Pagamenti pagoPA_ mediante
il _GAD_ (**Deprecato**)
* **xsd-common**: contiene gli schemi di definizione dei documenti _XML_ comuni scambiati all'interno del sistema _pagoPA_
* **catalogo-servizi**: contiene gli schemi di definizione _XML_ dei singoli servizi a catalogo (_Catalogo Servizi_) 
* **openapi**: contiene gli swagger delle interfacce _REST_.
