
# Introduction

This is the documentation of the pagoPA API for Provider Payment Services. This API enables a PSP  to pay a pagoPA Payment Notice according to _CAD (Codice Amministrazione Digitale)_

_Reference API PA side is available [here](https://raw.githubusercontent.com/pagopa/pagopa-api/develop/docs/indexPA.html)_

## Warning

**This is an experimental API that is (most probably) going to change as we evolve the pagoPa platform.**

## Identification and Authentication

Use of this API is restricted to PSP, or 3rd parties ( named as brokers ) which have signed a contract with PagoPA S.p.A. as stated _[here](https://www.pagopa.gov.it/it/prestatori-servizi-di-pagamento/)_

Both PSPs and Brokers are identified with an identifier ( idPSP, idBroker )  assigned by PagoPA S.p.A.

Formally, any API request is coming from a broker on behalf of a PSP which is responsable pf the payment.

- idPSP : it represent the PSP responsable for the payment
- idBroker : the sender
- idChannel : the psp service
- password : channel password

## Getting started guide

> _under construction_
