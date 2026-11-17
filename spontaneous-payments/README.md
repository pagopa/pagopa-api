# Pagamenti spontanei presso PSP – proposta "v2" (server-driven form)

## 1. Diagnosi: il problema non è SOAP, è `datiSpecificiServizio`

Oggi (`nodeForPsp.xsd` / `paForNode.xsd`, `DemandPaymentNoticeActor.scala`):

```
demandPaymentNotice { idPSP, idBrokerPSP, idChannel, password, idSoggettoServizio, datiSpecificiServizio: base64Binary }
paDemandPaymentNotice { idPA, idBrokerPA, idStation, idServizio, idSoggettoServizio, datiSpecificiServizioRequest: base64Binary }
```

- `datiSpecificiServizio` è un XML **opaco**, diverso per ogni servizio (`<tassaAuto>`, `<pagamentoPratica>` A001, `<pagamentoCup>`), con XSD dedicato nel catalogo servizi.
- Il PSP deve quindi, **per ogni servizio**: leggere l'XSD, disegnare un form ad‑hoc sui propri touchpoint (ATM, home banking, POS, tabaccherie), produrre l'XML, codificarlo base64. → *“implementazione custom ogni volta”* (motivazione di Intesa/Unicredit).
- Il Nodo non conosce la semantica dei campi: la validazione XSD del servizio è addirittura commentata (`DemandPaymentNoticeActor.checkRequest`), gli errori tornano come `PPT_ERRORE_EMESSO_DA_PAA` generico → UX povera (nessun errore per campo).

Passare a REST da solo **non** risolve: un JSON opaco per servizio sarebbe lo stesso problema. La soluzione è rendere il form **descritto dalla piattaforma** e il PSP un **renderer generico**: si implementa una volta, ogni nuovo servizio diventa sola configurazione.

## 2. Ispirazione: IDPay `/onboarding/{initiativeId}/detail` → `selfDeclarationCriteria`

IDPay restituisce una lista polimorfica di criteri (`_type`: `boolean`, `multi`, `text`, `informative`, `multi_consent`) con `code`, `description`, `value`/opzioni; l'app IO li renderizza genericamente e rimanda le risposte indicizzate per `code`. Nessuna release app per nuova iniziativa.

Stesso pattern per i pagamenti spontanei: **descrittore del form per servizio + risposte `code → value`**.

## 3. SOAP o REST?

Raccomandazione: **REST/JSON per la nuova interfaccia PSP**, SOAP legacy mantenuto e congelato.

| Aspetto | SOAP attuale | REST v2 |
|---|---|---|
| Form dinamico/polimorfico | XSD + base64, scomodo | JSON nativo, discriminator `_type` (OpenAPI `oneOf`) |
| Errori per campo | fault bean unico | RFC 7807 + `violations[{code,message}]` |
| Caching descrittore | no | `ETag`/`Cache-Control` (utile per POS/ATM) |
| Idempotenza | no | header `Idempotency-Key` |
| Allineamento piattaforma | — | `checkPosition`, `closePayment`, GPD, IDPay, ecommerce sono già REST; nodo4 ha già `Primitive.rest` + `RestActorPerRequest` |
| Impatto sul resto del flusso | — | nullo: dopo la demand si prosegue con `activatePaymentNoticeV2` (SOAP o REST) come oggi |

Lato EC: **doppio binario** – REST nuovo per gli EC che aderiscono, adapter verso la SOAP `paDemandPaymentNotice` esistente per gli EC già integrati (ACI, Min. Interno), così non li si obbliga a migrare.

## 4. Nuovo modello API lato PSP (`nodeForPsp` REST)

Base path proposto: `/spontaneous-payments/v1` (esposto via APIM, auth con subscription key + `idPSP/idBrokerPSP/idChannel`, niente `password` in body).

### 4.1 Catalogo
`GET /services?touchpoint=ATM|PSP|POS|IO&category=...`

```json
{ "services": [
  { "serviceId": "00002", "subjectServiceId": "00042", "name": "Bollo auto",
    "category": "TAX", "creditorInstitution": {"fiscalCode": "...", "name": "ACI"},
    "formVersion": "3", "logoUrl": "...", "validFrom": "...", "validTo": null }
]}
```
(sostituisce `nodoChiediCatalogoServiziV2` che restituisce XML base64)

### 4.2 Descrittore del form (equivalente di `/onboarding/{id}/detail`)
`GET /services/{subjectServiceId}/form` → `ETag: "v3"`

```json
{
  "subjectServiceId": "00042",
  "formVersion": "3",
  "title": {"it": "Pagamento bollo auto", "en": "Car tax"},
  "fields": [
    { "_type": "SELECT", "code": "vehicleType", "label": {"it": "Tipo veicolo"},
      "required": true,
      "options": [{"value": "1", "label": {"it": "Autoveicolo"}}, {"value": "2", "label": {"it": "Motoveicolo"}}] },
    { "_type": "TEXT", "code": "plate", "label": {"it": "Targa"}, "required": true,
      "validation": {"pattern": "^[A-Z0-9]{5,8}$", "maxLength": 8, "transform": "UPPERCASE"} }
  ]
}
```

Tipi di campo (`_type`, discriminator, set **chiuso e piccolo** così è renderizzabile anche su ATM/POS):

| `_type` | Uso | Attributi specifici |
|---|---|---|
| `TEXT` | targa, nome | `validation.pattern/minLength/maxLength`, `transform` |
| `FISCAL_CODE` | CF persona/PIVA | `subjectKind: PF\|PG\|ANY` (validazione checksum lato Nodo) |
| `EMAIL` | email | `businessOnly` |
| `AMOUNT` | importo in autoliquidazione (CUP) | `min`, `max` (centesimi) |
| `NUMBER` / `DATE` | anni, scadenze | `min`, `max` |
| `SELECT` / `MULTI` | enumerazioni | `options[]` |
| `BOOLEAN` | flag | — |
| `ONE_OF` | scelta tra alternative (CUP: CF **o** ISTAT **o** catasto) | `alternatives[]` di field |
| `GROUP` | blocco logico (pagatore, intestatario) | `fields[]`, `repeatable`, `maxItems` |
| `INFORMATIVE` | testo da mostrare all'utente (come IDPay) | `text` |
| `CONSENT` | presa visione obbligatoria | `text`, `required` |
| `HIDDEN` | costanti (es. `codicePratica=A001`) | `value` |

Attributi comuni: `code`, `label` (i18n), `hint`, `required`, `defaultValue`, `visibleIf` (`{code, equals}`), `sensitive` (PII → mascheramento log/RE), `prefill` (`PAYER_FISCAL_CODE`… se il PSP conosce già il cliente).

### 4.3 Demand (sostituisce `demandPaymentNotice`)
`POST /services/{subjectServiceId}/demands`  – header `Idempotency-Key`, `If-Match: "v3"` (form version)

```json
{ "formVersion": "3",
  "touchpoint": "ATM",
  "answers": [ {"code": "vehicleType", "value": "1"}, {"code": "plate", "value": "AB123CD"} ] }
```

`201 Created`
```json
{ "demandId": "01J...", 
  "qrCode": {"fiscalCode": "80001234567", "noticeNumber": "302000000000000001"},
  "paymentDescription": "Tassa automobilistica 2026 AB123CD",
  "creditorInstitution": {"fiscalCode": "80001234567", "companyName": "Regione Lazio", "officeName": null},
  "paymentOptions": [{"amount": 15250, "option": "EQ", "dueDate": "2026-12-31", "description": "..."}],
  "receiptRequirements": {"barcode": "GS1_128"}   
}
```
→ il PSP prosegue con `activatePaymentNoticeV2` usando `qrCode` (invariato).

Errori (RFC 7807):
- `400` `INVALID_ANSWERS` + `violations: [{"code":"plate","reason":"PATTERN"}]` (validazione **del Nodo** sul descrittore, prima di chiamare l'EC)
- `412` form version obsoleta → il PSP ricarica il descrittore
- `422` `EC_REJECTED` + `violations`/messaggio EC mostrabile all'utente (es. "targa non trovata")
- `404` servizio sconosciuto, `409` servizio non attivo, `502/504` EC irraggiungibile/timeout

Opzionale: `POST .../demands:validate` (dry-run, solo validazione lato Nodo) per form multi-step.

## 5. Nuovo modello lato EC (`paForNode`)

### 5.1 EC REST (nuovi aderenti)
`POST {station.restEndpoint}/demands`
```json
{ "idPA": "...", "idBrokerPA": "...", "idStation": "...",
  "serviceId": "00002", "subjectServiceId": "00042", "formVersion": "3",
  "answers": [{"code": "vehicleType", "value": "1"}, {"code": "plate", "value": "AB123CD"}] }
```
Risposta = stessa struttura di 4.3 (senza `demandId`) oppure `422` con `violations` per campo.

### 5.2 EC SOAP legacy (adapter nel Nodo)
Per i servizi esistenti si salva in configurazione un **template di mapping** `answers → XML` (es. XSLT su un XML canonico `<answers><a code="plate">…</a></answers>`, o template Mustache) che produce l'attuale `datiSpecificiServizioRequest`. L'EC non cambia nulla; i PSP usano solo il REST.

## 6. Esempi di descrittori sui casi d'uso attuali

**Passaporto (A001)**
```json
{ "fields": [
  {"_type": "HIDDEN", "code": "codicePratica", "value": "A001"},
  {"_type": "GROUP", "code": "pagatore", "label": {"it": "Chi paga"}, "fields": [
    {"_type": "FISCAL_CODE", "code": "codiceFiscalePagatore", "subjectKind": "PF", "required": true, "prefill": "PAYER_FISCAL_CODE", "sensitive": true},
    {"_type": "TEXT", "code": "denominazionePagatore", "required": true, "validation": {"maxLength": 70}}]},
  {"_type": "GROUP", "code": "intestatario", "label": {"it": "Intestatario passaporto"}, "fields": [
    {"_type": "FISCAL_CODE", "code": "codiceFiscaleIntestatario", "subjectKind": "PF", "required": true, "sensitive": true},
    {"_type": "TEXT", "code": "denominazioneIntestatario", "required": true}]},
  {"_type": "INFORMATIVE", "code": "infoRicevuta", "text": {"it": "Conserva la ricevuta con il codice a barre da presentare in Questura."}}
]}
```

**Canone Unico Patrimoniale**
```json
{ "fields": [
  {"_type": "ONE_OF", "code": "ente", "label": {"it": "Ente beneficiario"}, "required": true, "alternatives": [
    {"_type": "FISCAL_CODE", "code": "organizationFiscalCode", "subjectKind": "PG"},
    {"_type": "TEXT", "code": "istatCode", "validation": {"pattern": "^[0-9]{6}$"}},
    {"_type": "TEXT", "code": "cadastralCode", "validation": {"pattern": "^[A-Z][0-9]{3}$"}}]},
  {"_type": "TEXT", "code": "companyName", "required": true},
  {"_type": "FISCAL_CODE", "code": "debtorFiscalCode", "subjectKind": "PG", "required": true},
  {"_type": "TEXT", "code": "debtorFullName", "required": true},
  {"_type": "EMAIL", "code": "debtorEmail", "businessOnly": true},
  {"_type": "AMOUNT", "code": "amount", "required": true, "min": 1},
  {"_type": "CONSENT", "code": "autodichiarazione", "required": true, "text": {"it": "Dichiaro che l'importo è calcolato in autoliquidazione…"}}
]}
```

**Bollo auto**: vedi 4.2.

## Specifiche OpenAPI (bozza)

Branch `draft/spontaneous-payments-rest` su [pagopa/pagopa-api](https://github.com/pagopa/pagopa-api/tree/draft/spontaneous-payments-rest/openapi) (non mergiato).

| API | Vista leggibile |
|---|---|
| PSP → Nodo | [Swagger Editor](https://editor.swagger.io/?url=https://raw.githubusercontent.com/pagopa/pagopa-api/draft/spontaneous-payments-rest/openapi/spontaneous_payments_psp.json) |
| Nodo → EC | [Swagger Editor](https://editor.swagger.io/?url=https://raw.githubusercontent.com/pagopa/pagopa-api/draft/spontaneous-payments-rest/openapi/spontaneous_payments_ec.json) |

## Mock-up interattivo

[Apri il mock-up](https://htmlpreview.github.io/?https://github.com/pagopa/pagopa-api/blob/draft/spontaneous-payments-rest/spontaneous-payments/mockup/index.html) (pagina HTML singola, nessun backend: le chiamate sono simulate nel browser secondo la bozza OpenAPI).

- Lo stesso renderer generico del PSP disegna bollo auto, passaporto e CUP su tre touchpoint: home banking, ATM e POS.
- Il pannello "dietro le quinte" mostra le chiamate PSP → pagoPA (REST) e pagoPA → Ente, che sono REST oppure SOAP legacy con l'XML `datiSpecificiServizio` generato da template.
- Puoi provare la validazione campo per campo (es. un codice fiscale errato) e il rifiuto dell'Ente (targa `ZZ999ZZ`).
- Con "Pubblica un nuovo servizio" aggiungi un descrittore JSON: il servizio compare subito sul touchpoint, senza sviluppi lato PSP.

## 7. Impatti su nodo4 (`main_pg`)

- **Config / DB**: estendere `CDS_SERVIZIO` (o nuova tabella `CDS_SERVIZIO_FORM`) con `FORM_SCHEMA` (JSON), `FORM_VERSION`, `EC_INTERFACE` (`SOAP_LEGACY|REST`), `XML_MAPPING_TEMPLATE`; caricati in `ConfigData` (`cdsServices`) come oggi. Stazione: endpoint REST per la demand (accanto a `servicePof`).
- **Primitive**: aggiungere in `Primitive.rest` p.es. `"spontaneousForm-v1" -> "v1/spontaneous/services/form"`, `"spontaneousDemand-v1" -> "v1/spontaneous/demands"` (path parametrici da valutare: `NodoRoute` usa path statici → serviceId in body/query oppure estendere il matcher).
- **Actor**: nuovo `DemandPaymentNoticeV2Actor` che riusa la logica di `checkRequest` (soggetto‑servizio, versione, validità, stazione `spontaneousPayment`, broker) estratta in un trait comune; aggiunge `FormValidator` (answers vs descrittore) e poi chiama l'EC via REST oppure via adapter → `paDemandPaymentNotice` SOAP. Mappa la risposta EC sul DTO JSON.
- **SOAP v1**: invariata; opzionalmente anche lei può validare `datiSpecificiServizio` (oggi validazione XSD commentata).
- **RE/log**: campi `sensitive` mascherati negli eventi RE.

## 8. Roadmap suggerita

1. Definire OpenAPI (`pagopa-api/openapi`) PSP + EC e il meta‑schema del descrittore (set di `_type` chiuso).
2. Convertire i 3 servizi esistenti in descrittori + template XML (nessun impatto EC).
3. Implementare in nodo4 form/demand REST + adapter legacy; pilota con 1 PSP (es. su bollo auto o CIE/passaporto).
4. EC nuovi solo REST; deprecare `demandPaymentNotice` SOAP dopo adozione.

## 9. Punti aperti

- Descrittore custom (stile IDPay) vs **JSON Schema + UI schema** (JSON Forms): JSON Schema è standard ma troppo espressivo per ATM/POS; proposta: DTO custom verso i PSP, JSON Schema solo interno per la validazione.
- Chi gestisce i descrittori (Backoffice/Selfcare EC vs operatore pagoPA) e workflow di approvazione/versioning.
- Lookup dinamici (es. elenco comuni) → servizio `GET /services/{id}/fields/{code}/options?query=` o solo enumerazioni statiche.
- GDPR/PII (CF intestatario): minimizzazione, retention, mascheramento.
- Esposizione anche su IO/checkout (stesso descrittore → stesso form ovunque, vantaggio extra).
