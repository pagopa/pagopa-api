
# Introduction

This is the documentation of the pagoPA API for Payment Service Provider. This API enables a PSP  to pay a pagoPA Payment Notice according to _CAD (Codice Amministrazione Digitale)_

# Reference API PA side is available [here](https://pagopa.github.io/pagopa-api/indexPA.html)_

**Please notice: this API is subject to small changes since it is in final test release**

## Identification and Authentication

Use of this API is restricted to PSP, or 3rd parties ( named as brokers ) which have signed a contract with PagoPA S.p.A. as stated _[here](https://www.pagopa.gov.it/it/prestatori-servizi-di-pagamento/)_

Both PSPs and Brokers are identified with an identifier ( idPSP, idBroker )  assigned by PagoPA S.p.A.

Formally, any API request is coming from a broker on behalf of a PSP which is responsable of the payment.

- idPSP : it represent the PSP responsable for the payment
- idBroker : the sender
- idChannel : the psp service
- password : channel password

## Getting started guide

> _under construction_
