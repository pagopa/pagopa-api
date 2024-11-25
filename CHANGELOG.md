# SANP3.7.0 (Marzo 2024)
1. `08/03/2024` - Aggiunta nuovo swagger per le API di BackOffice pagoPA "External" - IBAN & stazioni EC
2. `08/03/2024` - Modificata descrizione del campo amount e timeout per l'API recupero URL della Redirect
3. `08/03/2024` - Aggiunto nuovo swagger `gpd_massive.json` per il caricamento massivo delle posizioni debitorie - corrette le estensioni dei file da `yaml` a `json`
4. `12/03/2024` - Aggiunto nuovo status nelle open api di FDR per l'introduzione del pagamento gestito in Stand In.
5. `13/03/2024` - Aggiunti 4 nuovi campi opzionali nella paCreatePosition
6. `15/03/2024` - Eliminato swagger API Backoffice pagoPA "External" poichè conteneva errori ed aggiunti i due nuovi swagger per PSP (GetIbans) ed EC (GetStations)
7. `21/03/2024` - Correzione API Backoffice pagoPA "External" swagger per PSP (GetIbans) ed EC (GetStations). Aggiunta della nuova API per EC (GetIbansByBroker)
8. `25/03/2024` - Aggiornato campo amount sull'API paCreatePosition
9. `25/03/2024` - fix swagger API Backoffice pagoPA "External"
10. `08/04/2024` - add new payment type inside `catalogoDatiInformativiPSP.xsd`

# SANP3.8.0 (Luglio 2024)
1. Gestione massiva delle posizioni debitorie

# SANP3.9.0 (Novembre 2024)
1. Fix openapi getOrganizationReceipt services, fields `email` and `channelDescription`
