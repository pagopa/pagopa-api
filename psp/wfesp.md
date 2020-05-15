# Interfaccia WFESP

Nel presente paragrafo saranno date indicazioni circa i parametri da utilizzare nella gestione della re-direzione del browser dell'utente verso il servizio di pagamento (anche detto canale) offerto dal PSP aderente durante un pagamento on-line.

Si tenga presente che il dato parametriPagamentoImmediato (più avanti specificato come obbligatorio) ed eventualmente in combinazione con il dato idCarrello (più avanti specificato come opzionale), deve consentire di identificare univocamente il singolo pagamento o l’insieme di pagamenti (carrello di RPT - pagamento multi-beneficiario) inviati al PSP nella sessione di pagamento in oggetto, in modo globale nell’ambito del Sistema.

## Re-direzione dal Web-FESP verso il Portale PSP

Il Portale del PSP viene richiamato dalla componente Web-FESP del NodoSPC con una URL composto nel modo sotto indicato
<urlPortalePSP>?
<parametriProfiloPagamento>&
<parametriPagamentoImmediato>
[&idCarrello=<identificativoCarrello>]
[&<parametriWisp>]
[&lang=xyz]

dove :
<urlPortalePSP>:    url del servizio del PSP come descritto all'interno della configurazione del canale del PSP.

<parametriProfiloPagamento> e <parametriPagamentoImmediato>: Query string fornite al PSP dal Nodo dei Pagamenti-SPC mediante la Request della primitiva pspInviaCarrelloRPT i cui valori sono specifici per ogni integrazione del PSP ( vedi capitolo successivo )

<idCarrello>: parametro opzionale, presente nel caso sia restituito dal PSP nella Response della primitiva  pspInviaCarrelloRPT invocata in precedenza.

<parametriWISP>: parametri opzionali 

<lang>: è la specifica del linguaggio scelto dall'utilizzatore finale, qualora fornita dal Portale dell'Ente Creditore nella re-direzione verso il Web-FESP (si veda il paragrafo 8.3.1). Il codice abbreviato identifica il linguaggio secondo lo standard ISO 693-3.

## Re-direzione dal Portale PSP verso il Web-FESP

Lo URL restituito dal Portale PSP al browser dell’utilizzatore finale, per reindirizzarlo verso il Web-FESP, ha la composizione sotto indicata:

<urlWeb-FESP>?
<parametriPagamentoImmediato>
 [&idCarrello=<identificativoCarrello>]
&<codiceRitornoPSP>

dove:
*urlWeb-FESP*:  è lo URL della componente Web-FESP del NodoSPC.
parametriPagamentoImmediato:    Query string fornita dal PSP mediante la Response della primitiva pspInviaCarrelloRPT invocata in precedenza.

*idCarrello* : parametro opzionale, presente nel caso sia restituito dal PSP nella Response della primitiva pspInviaCarrelloRPT invocata in precedenza

*codiceRitornoPSP*:  stringa contenente un parametro fornito dal PSP, il cui formato è lista di valori possibili sono concordati a priori dallo specifico PSP con il NodoSPC. Il significato del parametro è l’esito della transazione on-line dell’utilizzatore finale sul Portale del PSP. Tale esito viene mappato dal Web-FESP nell’URL di re-direzione verso il Portale dell'Ente Creditore in uno dei tre possibili esiti previsti:
    -OK:    il pagamento presso il Portale PSP è stato eseguito con successo; quest’ultimo fornirà a breve una RT positiva
    -ERROR: il pagamento presso il Portale PSP non è stato eseguito con successo; quest’ultimo ha segnalato al Web-FESP l’esito negativo
    -DIFFERITO: l’esito del pagamento eseguito dall’utilizzatore finale presso il Portale PSP sarà noto solo al ricevimento della RT.

## Integrazioni Specifiche

Le queryString associate ai parametri *parametriProfiloPagamento* e *parametriPagamentoImmediato* dipendono dall'integrazione verso il PSP , in particolare sussitono le seguenti integrazoni

### PosteItaliane

Per tutti i canali con re-indirizzamento del PSP PosteItaliane:

Forma del parametriProfiloPagamento:
profilo=<idIntermediarioPA>~<idStazioneIntermediarioPA>
Forma del parametriPagamentoImmediato:
idBruciatura=<valore>

Esempio di URL di redirezione WFESP->PSP:
`<urlPortalePSP>?[idDominio=<valore>]&profilo=<idIntermediarioPA>~<idStazioneIntermediarioPA>&idBruciatura=<valore>&idCarrello=<valore>`
[&lang=<langISO693-3
>]
Esempio di URL di redirezione PSP->WFESP:
`<urlWeb-FESP>?[idDominio=<valore>]&idBruciatura=<valore>&idCarrello=<valore>&codiceRitorno=<valoreCodiceRitorno>`
con codiceRitorno che può assumere i seguenti valori (traduzione WFESP per PA):

- OK_01: Transazione completata con successo (OK)
- WN_01: Transazione eseguita con successo con errore in fase generazione file firmato (OK)
- KO_01: Carrello scaduto (ERROR)
- KO_02: Transazione con errore su PSP (ERROR)
- KO_03: Transazione annullata su PSP (ERROR)
- AN_01: Carrello annullato da utente (ERROR)
- ER_01: Verifica presenza idBruciatura e idCarrello fallita (ERROR)

### Intesa

Forma del parametriProfiloPagamento:
non valorizzato
Forma del parametriPagamentoImmediato:
idBruciatura=<valore>

Esempio di URL di redirezione WFESP->PSP:
`<urlPortalePSP>?[idDominio=<valore>]&idBruciatura=<valore>[&idCarrello=<valore>][&lang="it-IT"]`

Esempio di URL di redirezione PSP->WFESP:
`<urlWeb-FESP>?[idDominio=<valore>]&idBruciatura=<valore>&codiceRitorno=<valoreCodiceRitorno>`

con codiceRitorno che può assumere i seguenti valori (traduzione WFESP per PA):

- OK:           Processo concluso con esito positivo (OK)
- ERROR:        Processo concluso con esito negativo (ERROR)
- ABORT:        Transazione annullata dall’utente giunto sulla pagina di pagamento (ERROR)
- DIFFERITO:    Processo concluso con esito dubbio- PAGO IN CONTO (DIFFERITO)

### Nexi

Forma del parametriProfiloPagamento:
non valorizzato
Forma del parametriPagamentoImmediato:
idRichiesta=<valore>

Esempio di URL di redirezione WFESP->PSP:
`<urlPortalePSP>?[idDominio=<valore>]&idRichiesta=<valore>[&idCarrello=<valore>][&parametriCustomPa]`
Esempio di URL di redirezione PSP->WFESP:
`<urlWeb-FESP>?[idDominio=<valore>]&idRichiesta=<valore>&codiceRitorno=<valoreCodiceRitorno>`

con codiceRitorno che può assumere i seguenti valori (traduzione WFESP per PA):

- OK:           Processo concluso con esito positivo (OK)
- ERROR:        Processo concluso con esito negativo (ERROR)
- ABORT:        Transazione annullata dall’utente giunto sulla pagina di pagamento (ERROR)
- DIFFERITO:    Processo concluso con esito dubbio (DIFFERITO)

### BancomatPay

Forma del parametriProfiloPagamento:
non è valorizzato.
Forma del parametriPagamentoImmediato:
idBruciatura=<valore>
Forma del parametroWisp:
cell=<numeroTelefonoCriptato>&psp=<abi>
dove :

- cell: numero di telefono associato alla carta BancomatPay criptato 
- psp:  codice abi del PSP incaricato di eseguire la transazione
  
Esempio di URL di redirezione WFESP->PSP:
`<urlPortalePSP>?[idDominio=<valore>]&cell=<numeroTelefonoCriptato>&psp=<abi>&idBruciatura=<valore>[&lang]`
Esempio di URL di redirezione PSP->WFESP:
`<urlWeb-FESP>?[idDominio=<valore>]&idBruciatura=<valore>&codiceRitorno=<valoreCodiceRitorno>`

con codiceRitorno che può assumere i seguenti valori (traduzione WFESP per PA):

- OK:           Processo concluso con esito positivo (OK)
- ERROR:        Processo concluso con esito negativo (ERROR)
- DIFFERITO:    Processo concluso con esito dubbio (DIFFERITO)

### MyBank-Banca Seller

Per tutte le Banche Seller integrate (ovvero sui canali il cui tipoVersamento corrisponde a MYBK) 

Forma del parametriProfiloPagamento:

- IDVS=<valore> : rappresenta l'identificativo della Banca Buyer a cui rendirizzare l'utente per concludere il pagamento.

Forma del parametriPagamentoImmediato:

- idBruciatura=<valore> : identifica univocamente l'operazione di pagamento.

Esempio di URL di redirezione WFESP PSP:
`<urlPortalePSP>?IDVS=<Validation Service ID>&idBruciatura=<valore>[&idCarrello=<valore>][&lang=<language>]`

Esempio di URL di redirezione PSP WFESP:
`<urlWeb-FESP>?[idDominio=<valore>]&idBruciatura=<valore>&codiceRitorno=<valoreCodiceRitorno>`

con codiceRitorno che può assumere i seguenti valori (traduzione WFESP per PA):

- OK:   Processo concluso con esito positivo (OK)
- KO:   Processo concluso con esito negativo (ERROR)
- DIFFERITO:    Processo concluso con esito differito (DIFFERITO)