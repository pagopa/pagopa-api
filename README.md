<img width="150px"  src="https://www.pagopa.gov.it/assets/images/pagopa-logo.png" title="pagoPa" alt="pagoPa"></a>
# pagopa-specifichepagamenti-schemi


> definizione di tutte le interfacce (esposte e richieste) per la connessione con il sistema pagoPA.
> Tutti gli schemi XSD e WSDL seguono release diverse dalle SANP

Il repository è suddiviso nelle seguenti sezioni:

* **ec**: contiene la definizione delle interfacce esposte da un ente creditore.
* **psp**: contiene la definizione delle interfacce esposte da un Psp.
* **nodo**: contiene la definizione delle interfacce esposte dal sistema.
* **pda**: contiene i tipi di dati scambiati dai soggetti aderenti con il Portale delle Adesioni.
* **general**: contiene gli schemi di definizione dei documenti XML scambiati all'interno del sistema.


## How to generate documentation 

clone the repo typing:
```
git clone https://github.com/pagopa/pagopa-api pagopa-api && cd $_
```

and then run 🚀 the following script ( ex: _nodeForPsp_ )
```
./build_doc.sh -b -r nodeForPsp
```
> NOTE : allowed services _{nodeForPa, nodeForPsp , paForNode, pspForNode}_

if all rights 👍 you will see somethign like that:
```
Using Redoc community edition.
Login with openapi-cli login or use an enterprise license key to preview with the premium docs.


  🔎  Preview server running at http://127.0.0.1:8080

Bundling...


  👀  Watching openapi/nodeForPsp_Service.yaml and all related resources for changes

Created a bundle for openapi/nodeForPsp_Service.yaml successfully
```

then click [here](http://127.0.0.1:8080) to show documentation.

