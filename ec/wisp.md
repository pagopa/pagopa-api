# Interfaccia WISP

Nel presente paragrafo saranno date indicazioni circa i parametri da utilizzare nella gestione della re-direzione del browser dell'utente nell'ambito del modello di pagamento presso il sito web dell'EC.

## Re-direzione dal Portale EC verso il Web-FESP

La sintassi dello URL che il Portale dell'Ente Creditore deve utilizzare per re-indirizzare il browser dell’utilizzatore finale verso il WISP è la seguente,

`<wispURL>[&lang="xy”][&logo="1239338234242_01"]`

dove :

*wispURL*:  la stringa fornita all'Ente Creditore dal NodoSPC nella response della primitiva nodoInviaCarrelloRPT. La stringa è così composta:
            `<urlWeb-FESP>?idSession=<idSession>"`
            dove :
                *urlWeb-FESP*:  è lo URL della componente Web-FESP del Nodo dei Pagamenti-SPC
                *idSessione*:   è generato dal NodoSPC e identifica in modo univoco l’operazione di pagamento

*lang*:     specifica il linguaggio scelto dall'utilizzatore finale sul Portale dell'Ente Creditore, secondo la codifica standard ISO 693-1. Se non presente, la lingua mostrata sarà l'italiano. Le lingue supportate sono Italiano ( it , it-IT ) , Inglese (en-US), Francese (fr-FR) , Tedesco (de-DE), Sloveno (sl-SI)

esempio per poter configurare la lingua inglese 

`<wispURL>&lang="en”`

*logo*: codice identificativo del logo dell'EC configurato ( tipo file : png o jpg , formato 220x220 pixel)

## Re-direzione dal Web-FESP verso il Portale EC

Lo URL restituito dal Web-FESP al browser dell’utilizzatore finale per il re-indirizzamento verso il Portale dell'Ente Creditore è la seguente:

`<urlPortalePA>?&idSession=<idSession>& esito=<esito>[&<URLesitoPSP>]`

dove:

*urlPortalePA*: è lo URL del Portale dell'Ente Creditore così come configurato all'interno della stazione dalla quale è stato richiesto il pagamento. Ad esempio: http://www.giustizia.it/pagamenti

*idSession*:    generato dal NodoSPC e identifica univocamente l’operazione di pagamento.

*esito*:        corrisponde alla traduzione dell’esito della transazione on-line fornito dal Portale PSP nella re-direzione di ritorno al Web-FESP, dopo che l’utilizzatore finale ha interagito con il Portale PSP. Può essere utilizzato opzionalmente dal Portale dell'Ente Creditore per scegliere automaticamente una pagina da presentare all’utilizzatore finale in base all’esito della transazione. In ogni caso l’esito certo del pagamento è dato dalla RT. I valori di esito ammessi sono:
    - OK: il pagamento presso il Portale PSP è stato eseguito con successo; quest’ultimo fornirà a breve una RT positiva
    -ERROR: il pagamento presso il Portale PSP non è stato eseguito con successo; quest’ultimo ha segnalato al Web-FESP l’esito negativo.
    -DIFFERITO: l’esito del pagamento eseguito dall’utilizzatore finale presso il Portale PSP sarà noto solo al ricevimento della RT.

*URlEsitoPSP*:  è tutta la query string dei parametri passati dal Portale PSP al Web-FESP senza traduzione in idSession ed esito, il suo contenuto dipende dall'integrazione effettuata. Esempio per uno specifico PSP:
`"idBruciatura=abc1d4e7f3a8&idCarrello=123456789&codiceRitorno=KO_02"`
