<!-- 
plantuml -tsvg api-definitions/openapi/descriptionPA.md 
-->
# Introduction

This is the documentation of the pagoPA API for Public Administration. This API enables a PA  to request a payment on pagoPA Payment Notice according to _CAD (Codice Amministrazione Digitale)_

The payment process defined below starting from the infrastructures made available by the PSP such as, for example, ATMs, Home banking and mobile payment applications, post offices, etc. The acquisition of the information necessary to communicate with the platform is contained within a `QR-CODE` present in the payment notice which can facilitate data entry. The same information is present in the notice to allow manual entry

### Mock EC environment by [PagoPA](https://www.pagopa.gov.it/) 🧑‍💻
<details>
  <summary>Click to expand!</summary>  

  **How to get access to `pagopa-pa-mock`**

  **WIP** : _Shortly it will be available in this section how to connect to the PagoPa service (a.k.a. `pagopa-pa-mock`) which will allow PSPs to test all the primitives defined on this page in a UAT environment_
  
</details>

<br>

### API NodoSPC payment : **PSP side**
_Reference API PSP side is available [here](https://pagopa.github.io/pagopa-api/index.html)_

### Payment process activated by the PSP

<!-- https://github.com/pagopa/pagopa-analisi/blob/main/PlantUML/Sequence/modelli/nuovoModello3_ENG.puml -->

<!-- 
@startuml uml_diag/seqdiag-wisplightnuovoModello3_newPA
title Payment process activated by the PSP

participant EC
participant pagoPA
participant PSP
actor       User

== verify phase (optional) ==

User [#blue]-> PSP: Payment Notice

alt QR-CODE
    PSP -> pagoPA: verifyPaymentNotice req
    note right : The PSP requests the verification of the notice \n (check amount)
    activate pagoPA
    pagoPA -> EC: paVerifyPaymentNotice req
    note left #aqua : Debt Position\n STATUS = **Open**
    activate EC
    EC -> pagoPA: paVerifyPaymentNotice res
    deactivate EC
    pagoPA -> PSP: verifyPaymentNotice res
    deactivate pagoPA
else BARCODE-128-AIM 
    PSP -> pagoPA: verificaBollettino req
    activate pagoPA
    pagoPA -> EC: paVerifyPaymentNotice req
    note left #aqua : Debt Position\n STATUS = **Open**
    activate EC
    EC -> pagoPA: paVerifyPaymentNotice res
    deactivate EC
    pagoPA -> PSP: verificaBollettino res
    deactivate pagoPA
end

PSP [#blue]-> User: Notice verified and updated

== activate phase ==
User [#blue]-> PSP: Confirm willingness to pay
PSP -> pagoPA: activatePaymentNotice req
note right : The PSP requires payment activation
activate pagoPA
pagoPA -> pagoPA: token generation (<color blue>token</color>)
pagoPA -> EC: paGetPayment req
note left #aqua : Debt Position\n STATUS = **Open**
activate EC
EC -> pagoPA: paGetPayment res
deactivate EC
pagoPA -> PSP: activatePaymentNotice res (<color blue>token</color>)
note right : The PSP has all data \nto allow the payment
deactivate pagoPA

PSP [#blue]-> User: Payment page
note left EC #pink : Newly configured ECs \n**DOES'NT HAVE TO** lock the debt position \nafter activation.

== send receipt phase ==

User [#blue]-> PSP: Pay
note right PSP : If payment OK ->  Outcome +\nIf payment KO -> Outcome -

PSP -> pagoPA: sendPaymentOutcome req (<color blue>token</color>)
activate pagoPA
pagoPA -> PSP: sendPaymentOutcome res
deactivate pagoPA
pagoPA -> pagoPA: receipt generation (idReceipt=<color blue>token</color>)

loop for each EC in transfer list
    pagoPA -> EC: paSendRT req (idReceipt=<color blue>token</color>)
    activate EC
    EC -> pagoPA: paSendRT res
    deactivate EC
end 

note left EC #aqua: Debt Position\n STATUS = **Open -> Closed/Open**\n(based on receipt result)

@enduml
-->
![](seqdiag-wisplightnuovoModello3_newPA.svg)

**Please notice: this API is subject to small changes since it is in final test release**

## Identification and Authentication

Use of this API is restricted to PA, or 3rd parties ( named as brokers ) which have signed a contract with [PagoPA S.p.A.](https://www.pagopa.gov.it/it/pagopa-spa/) as stated _[here](https://www.pagopa.gov.it/it/pubbliche-amministrazioni/come-aderire/)_

Both PAs and Brokers are identified with an identifier (`idPA`, `idBrokerPA`)  assigned by PagoPA S.p.A.

Formally, any API request is coming from a broker on behalf of a PA which is responsable of the payment.
  
| Field   |      Description      |  Example value |
|:----------:|-------------|------|
| **idPA** | Alphanumeric field containing the tax code of the PA that manage the payment request.<br>(_in previous versions called_ `identificativoDominio`)| 80215430580 |
| **idBrokerPA** | Identification of the PA intermediary who provides the specific access (**idStation**) | 88835020584 |
| **idStation**|  Station identifer related to PA in the SPC Payment Node system | 888020584_01 |


## Verify Phase
Below is the detailed diagram of this phase

<!-- https://github.com/pagopa/pagopa-analisi/blob/main/PlantUML/Sequence/businessProcess/verifyPaymentNotice.puml -->
<!-- 
@startuml uml_diag/verifyPaymentNotice_newPA
title Verify Payment Notice 

participant EC
participant pagoPA
participant PSP

PSP -> pagoPA: verifyPaymentNotice req
activate pagoPA
pagoPA -> EC: paVerifyPaymentNotice req
activate EC
EC -> pagoPA: paVerifyPaymentNotice res
deactivate EC
pagoPA -> PSP: verifyPaymentNotice res
deactivate pagoPA

@enduml
-->
![](verifyPaymentNotice_newPA.svg)

## Activation Phase
Below is the detailed diagram of this phase

<!-- https://github.com/pagopa/pagopa-analisi/blob/main/PlantUML/Sequence/businessProcess/activatePaymentNotice.puml -->
<!-- 
@startuml uml_diag/activatePaymentNotice_newPA
title Activate Payment Notice

participant EC
participant pagoPA
participant PSP

PSP -> pagoPA: activatePaymentNotice req
activate pagoPA
pagoPA -> pagoPA: token generation (<color blue>token</color>)
pagoPA -> EC: paGetPayment req
activate EC
EC -> pagoPA: paGetPayment res
deactivate EC
pagoPA -> PSP: activatePaymentNotice res (<color blue>token</color>)
deactivate pagoPA

@enduml
-->
![](activatePaymentNotice_newPA.svg)

## Receipt Phase
Below is the detailed diagram of this phase

<!-- https://github.com/pagopa/pagopa-analisi/blob/main/PlantUML/Sequence/businessProcess/sendPaymentOutcome.puml -->
<!-- 
@startuml uml_diag/outcomeOK
title Send Payment Outcome

participant EC
participant pagoPA
participant PSP

PSP -> pagoPA: sendPaymentOutcome req (<color blue>token</color>)
activate pagoPA
pagoPA -> PSP: sendPaymentOutcome res
deactivate pagoPA
pagoPA -> pagoPA: receipt generation (idReceipt=<color blue>token</color>)

loop for each EC in transfer list
    pagoPA -> EC: paSendRT req (idReceipt=<color blue>token</color>)
    activate EC
    EC -> pagoPA: paSendRT res
    deactivate EC
end 

@enduml
-->
![](outcomeOK.svg)
