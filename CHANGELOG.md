# SANP3.7.0 (Marzo 2024)
1. `SANP3.7.0_01` - `08/03/2024` - Aggiunta nuovo swagger per le API di BackOffice pagoPA "External" - IBAN & stazioni EC
2. `SANP3.7.0_02` - `08/03/2024` - Modificata descrizione del campo amount e timeout per l'API recupero URL della Redirect
3. `SANP3.7.0_03` - `08/03/2024` - Aggiunto nuovo swagger `gpd_massive.json` per il caricamento massivo delle posizioni debitorie - corrette le estensioni dei file da `yaml` a `json`
4. `SANP3.7.0_04` - `12/03/2024` - Aggiunto nuovo status nelle open api di FDR per l'introduzione del pagamento gestito in Stand In.
5. `SANP3.7.0_05` - `13/03/2024` - Aggiunti 4 nuovi campi opzionali nella paCreatePosition
6. `SANP3.7.0_06` - `15/03/2024` - Eliminato swagger API Backoffice pagoPA "External" poichè conteneva errori ed aggiunti i due nuovi swagger per PSP (GetIbans) ed EC (GetStations)
7. `SANP3.7.0_07` - `21/03/2024` - Correzione API Backoffice pagoPA "External" swagger per PSP (GetIbans) ed EC (GetStations). Aggiunta della nuova API per EC (GetIbansByBroker)
8. `SANP3.7.0_08` - `25/03/2024` - Aggiornato campo amount sull'API paCreatePosition
9. `SANP3.7.0_09` - `25/03/2024` - fix swagger API Backoffice pagoPA "External"
10. `SANP3.7.0_10` - `08/04/2024` - add new payment type inside `catalogoDatiInformativiPSP.xsd`
