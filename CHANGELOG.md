# SANP3.9.1 (Dicembre 2024)
Nessuna modifica alle API ma solo allineamento del repository alla nuova versione delle SANP:
1. Aggiornamento del modello dati descritto in ​'Modello dati'
2. Aggiornamento del 'Quality improvement'

# SANP3.9.0 (Novembre 2024)
1. Pubblicazione specifiche API Opzioni Di Pagamento `psp_payment_options.json`
2. Pubblicazione specifiche API Stampa Avvisi `print_notices.json`
3. Correzione flag standIn in `pspNotifyPaymentV2`
   - `nodeForPsp.xsd`
     - added "standIn" in "ctPaymentV2"
     - removed "standin" in "pspNotifyPaymentV2"
   - `paForNode.xsd`
     - added "standIn" in "ctReceipt" & "ctReceiptV2"
     - removed "standIn" in "paSendRTReq" & "paSendRTV2Request"
4. `transferCategory` opzionale su `actvatePaymentNoticeV2`
   - `nodeForPsp.xsd`
     - let `transferCategory` not mandatory
5. Cambio formato chiave di idempotenza su `actvatePaymentNoticeV1`, `actvatePaymentNoticeV2`  e su `sendPaymnetOutcome`
   - `nodeForPsp.xsd`
6. `companyName` opzionale sulla primitiva `paGetPaymentV2`
   - `paForNode.xsd`
7. Aggiunta la sezione `metadata` all'interno della sezione `transferList` sulle primitive `paGetPayment`
   - `paForNode.xsd`
   - `nodeForPsp.xsd`
   

# SANP3.8.0 (Luglio 2024)
1. Gestione massiva delle posizioni debitorie
2. Fix openapi getOrganizationReceipt services, fields `email` and `channelDescription`

# SANP3.7.0 (Marzo 2024)
1. Aggiunta nuovo swagger per le API di BackOffice pagoPA "External" - IBAN & stazioni EC
2. Modificata descrizione del campo amount e timeout per l'API recupero URL della Redirect
3. Aggiunto nuovo swagger `gpd_massive.json` per il caricamento massivo delle posizioni debitorie - corrette le estensioni dei file da `yaml` a `json`
4. Aggiunto nuovo status nelle open api di FDR per l'introduzione del pagamento gestito in Stand In.
5. Aggiunti 4 nuovi campi opzionali nella paCreatePosition
6. Eliminato swagger API Backoffice pagoPA "External" poichè conteneva errori ed aggiunti i due nuovi swagger per PSP (GetIbans) ed EC (GetStations)
7. Correzione API Backoffice pagoPA "External" swagger per PSP (GetIbans) ed EC (GetStations). Aggiunta della nuova API per EC (GetIbansByBroker)
8. Aggiornato campo amount sull'API paCreatePosition
9. Fix swagger API Backoffice pagoPA "External"
10. Add new payment type inside `catalogoDatiInformativiPSP.xsd`
