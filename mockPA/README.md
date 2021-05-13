# pagopa-pa-mock

A mock implementation of PA pagoPA service

- [pagopa-pa-mock](#pagopa-pa-mock)
  - [Glossary](#glossary)
  - [Usage](#usage)
  - [Functionalities](#functionalities)
    - [Tribute description](#tribute-description)
    - [Configurations](#configurations)

## Glossary

| Acronym | Description | 
| -------- | ----------- | 
| EC or PA        | Public Admninistration  | 
| CCPost          | Postal account          | 
| CCBank          | Bank account            |

<br>

## Usage
## Functionalities

The following functionalites are available (EC Side) 
>(_see [here](https://pagopa.github.io/pagopa-api/indexPA.html) to details_)
- *paVerifyPaymentNotice*
- *paGetPayment*
- *paSendRT*

These mock functionalities allows the PSP to invoke all the payment steps 
> (_see [here](https://pagopa.github.io/pagopa-api/) to details_)
- *verifyPaymentNotice* or *verificaBollettino*
- *activatePaymentNotice* 
- *sendPaymentOutcome*

### Tribute description
The tribute is 120 EUR divided in 2 transfer: 

- Transfer 1 : TARI, 100€ due to **EC_TE**
- Transfer 2 : TEFA, 20€ due to **Comune di Milano**

With this mock are modelled both : 
1. multibeneficiary notice (comprehensive of TARI and TEFA) 
2. monobeneficiary notice (only TARI) 

### Configurations

Both EC have at their disposal a bank IBAN and a postal IBAN.
Based on notice number the mock will reply with a certain configuration of the tribute.


| Notice number       | CC EC_TE | CC Comune di Milano| Notes                           |
|---------------------|----------|--------------------|---------------------------------|
|302**00**xxxxxxxxxxx | CCPost   | CCPost             | multibeneficiary (TARI + TEFA) |
|302**01**xxxxxxxxxxx | CCPost   | CCBank             | multibeneficiary (TARI + TEFA) |
|302**02**xxxxxxxxxxx | CCBank   | CCPost             | multibeneficiary (TARI + TEFA) |
|302**03**xxxxxxxxxxx | CCBank   | CCBank             | multibeneficiary (TARI + TEFA) |
|302**04**xxxxxxxxxxx | CCPost   | n.a.               | monobeneficiary (TARI)         |
|302**05**xxxxxxxxxxx | CCBank   | n.a.               | monobeneficiary (TARI)         |


The following edge cases are available (stateless, based on notice number)

| Notice number       | Description                            |
|---------------------|----------------------------------------|
|302**99**xxxxxxxxxxx | Payment expired                        |
|302**YY**xxxxxxxxxxx | Payment unknown                        |

**_NOTE:_**  YY: every code not mentioned before -> from 06 to 98
