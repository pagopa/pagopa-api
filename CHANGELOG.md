# SANP3.10.0 (Novembre 2025)
1. Aggiunta nuove specifiche openapi per:
   - servizio di caricameto massivo delle posizioni debitorie tramite `ACA` ➡️ `gpd-4-aca_massive_v2.json`
   - servizio `@e.bollo 2.0` - Pagamento dovuto ➡️ `e_bollo_20.json`
   - servizio `Opzioni Di Pagamento per PSP` ➡️ `psp_payment_options.json`
   - servizio `Opzioni Di Pagamento per EC` ➡️ `orgs_payment_options.json`
2. Modificati i seguenti servizi:
   - aggiunto campo `standIN` nella response della primitiva `verificaBollettino`
3. Aggiunto servizio di pagamento spontaneo per il Passaporto attivato presso il touchpoint del PSP in favore del Ministero degli Interni ➡️ `catalogo-servizi/A001_Passaporto_1_0_0.xsd`
4. Flussi di Rendicontazione `FdR`
   - Deprecati i vecchi flussi di rendicontazione `SOAP` - due date `30 Giugno 2026`
     - `nodoInviaFlussoRendicontazione`
     - `nodoChiediElencoFlussiRendicontazione`
     - `nodoChiediFlussoRendicontazione`
   - Deprecate le API di GPD `GPD Reporting Analysis` per la gestione dei flussi - due date `31 Dicembre 2026`
     - `getFlowList`
     - `getFlow`
5. Dizionario dei metadata - Aggiunto metadato per le spese di notifica SEND ➡️ [Spese di notifica SEND](https://developer.pagopa.it/pago-pa/guides/metadata/v1.0/spese-di-notifica-send)
6. Refactoring sezione `openapi`
   - Tutti i file sono ora in formato `.json`
     - `checkout.yaml` ➡️ `checkout.json`
     - `fdr_organization.yaml` ➡️ `fdr_organization.json`
     - `fdr_psp.yaml` ➡️ `fdr_psp.json`
     - `paCreatePosition.yaml` ➡️ `paCreatePosition.json`
     - `redirect.yaml` ➡️ `redirect.json`

# SANP3.9.1 (Dicembre 2024)
Nessuna modifica alle API ma solo allineamento del repository alla nuova versione delle SANP:
1. Aggiornamento del modello dati descritto in ​'Modello dati'
2. Aggiornamento del 'Quality improvement'
3. 2025-03-11 - BizEvent Service aggiunto campo `paymentDateTimeFormatted` su `getOrganizationReceipt` in conformità con `paSendRT`

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
