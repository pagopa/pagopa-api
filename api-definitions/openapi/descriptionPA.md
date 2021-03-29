
# Introduction

This is the documentation of the pagoPA API for Public Administration. This API enables a PA  to request a payment on pagoPA Payment Notice according to _CAD (Codice Amministrazione Digitale)_

_Reference API PSP side is available [here](https://pagopa.github.io/pagopa-api/index.html)_

**Please notice: this API is subject to small changes since it is in final test release**

## Identification and Authentication

Use of this API is restricted to PA, or 3rd parties ( named as brokers ) which have signed a contract with [PagoPA S.p.A.](https://www.pagopa.gov.it/it/pagopa-spa/) as stated _[here](https://www.pagopa.gov.it/it/pubbliche-amministrazioni/come-aderire/)_

Both PAs and Brokers are identified with an identifier (`idPA`, `idBrokerPA`)  assigned by PagoPA S.p.A.

Formally, any API request is coming from a broker on behalf of a PA which is responsable of the payment.

- `idPA` : it represents the PA responsable for a request payment
- `idBrokerPA` : the sender
- `idStation` : the pa service

## Getting started guide

> _under construction_
