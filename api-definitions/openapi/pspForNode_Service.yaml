swagger: '2.0'
info:
  title: pspForNode_Service
  x-logo: 
    backgroundColor: #FFFFFF 
    url: "https://www.pagopa.gov.it/assets/images/pagopa-logo.png" 
  description: 
      $ref: descriptionPSP.md
  x-ibm-name: pspfornodeservice
  version: PagoPa API
schemes:
  - https
basePath: /pspForNode_Service
produces:
  - application/xml
consumes:
  - application/xml
x-ibm-configuration:
  type: wsdl
  phase: realized
  enforced: true
  testable: true
  gateway: datapower-gateway
  cors:
    enabled: true
  wsdl-definition:
    wsdl: pspForNode.wsdl
    service: pspForNode_Service
    port: pspForNode_Port
    soap-version: '1.1'
  assembly:
    execute:
      - proxy:
          title: proxy
          target-url: 'http://pagopa-api.pagopa.gov.it/service/psp/pspForNode'
  x-ibm-apiconnect-wsdl:
    package-version: 1.8.31
    options: {}
    messages:
      info: []
      warning: []
      error: []
paths:
  /pspNotifyPayment:
    post:
      summary: Operation pspNotifyPayment
      description: >-
        Notify the outcome of a payment transaction started on any PagoPA client
        and executed on a payment gateway integrated with Payment Manager.


        if outcome is OK, the PSP will receive a transfer found on a technical
        account. Therefore the PSP shall : 


        - close the payment by using the *sendPaymentOutcome* message using the
        *paymentToken* on the request.

        - trasfer founds to the account according to the *transferList* element.


        if outcome is KO, the PSP can use this information to balance payment
        gateway transaction and PSP transfers
      operationId: pspNotifyPayment
      x-ibm-soap:
        soap-action: pspNotifyPayment
        soap-operation: >-
          {http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd}pspNotifyPaymentReq
      parameters:
        - in: body
          name: body
          required: true
          schema:
            $ref: '#/definitions/pspNotifyPaymentInput'
          description: >-
            ```
                <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:pspfn="http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                  <soapenv:Body>
                      <pspfn:pspNotifyPaymentReq>
                        <idPSP>88888888888</idPSP>
                        <idBrokerPSP>88888888888</idBrokerPSP>
                        <idChannel>88888888888_01</idChannel>
                        <paymentDescription>test</paymentDescription>
                        <fiscalCodePA>77777777777</fiscalCodePA>
                        <companyName>company EC</companyName>
                        <officeName>office EC</officeName>                        
                        <paymentToken>ac6536ab9967401fb6cfa98bef88ccf0</paymentToken>
                        <creditorReferenceId>11111111112222222</creditorReferenceId>
                        <debtAmount>30.00</debtAmount>
                        <transferList>
                            <transfer>
                              <idTransfer>1</idTransfer>
                              <transferAmount>20.00</transferAmount>
                              <fiscalCodePA>77777777777</fiscalCodePA>
                              <IBAN>IT0000000000000000000000000</IBAN>
                              <remittanceInformation>info remittance</remittanceInformation>
                            </transfer>
                            <transfer>
                              <idTransfer>2</idTransfer>
                              <transferAmount>10.00</transferAmount>
                              <fiscalCodePA>77777777778</fiscalCodePA>
                              <IBAN>IT0000000000000000000000001</IBAN>
                              <remittanceInformation>info remittance</remittanceInformation>
                            </transfer>
                        </transferList>
                        <creditCardPayment>
                            <rrn>11223344</rrn>
                            <outcomePaymentGateway>00</outcomePaymentGateway>
                            <totalAmount>31.00</totalAmount>
                            <fee>1.00</fee>
                            <timestampOperation>2021-07-09T17:06:03</timestampOperation>
                            <authorizationCode>123456</authorizationCode>
                        </creditCardPayment>
                      </pspfn:pspNotifyPaymentReq>
                  </soapenv:Body>
                </soapenv:Envelope>
            ```            
      responses:
        '200':
          description: 'verificaBollettinoRes'
          schema:
            $ref: '#/definitions/verificaBollettinoOutput'
          examples:
            application/xml: >-
              <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:psp="http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd">
                <soapenv:Header/>
                <soapenv:Body>
                    <psp:pspNotifyPaymentRes>
                      <outcome>OK</outcome>
                    </psp:pspNotifyPaymentRes>
                </soapenv:Body>
              </soapenv:Envelope>
definitions:
  Security:
    xml:
      namespace: >-
        http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd
      prefix: wsse
    description: Header for WS-Security
    type: object
    properties:
      UsernameToken:
        xml:
          namespace: >-
            http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd
          prefix: wsse
        type: object
        properties:
          Username:
            xml:
              namespace: >-
                http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd
              prefix: wsse
            type: string
          Password:
            xml:
              namespace: >-
                http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd
              prefix: wsse
            type: string
          Nonce:
            xml:
              namespace: >-
                http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd
              prefix: wsse
            type: string
            properties:
              EncodingType:
                xml:
                  namespace: ''
                  attribute: true
                type: string
          Created:
            xml:
              namespace: >-
                http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd
              prefix: wsu
            type: string
      Timestamp:
        xml:
          namespace: >-
            http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd
          prefix: wsu
        type: object
        properties:
          Created:
            xml:
              namespace: >-
                http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd
              prefix: wsu
            type: string
          Expires:
            xml:
              namespace: >-
                http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd
              prefix: wsu
            type: string
          Id:
            xml:
              namespace: >-
                http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd
              prefix: wsu
              attribute: true
            type: string
  pspNotifyPaymentInput:
    description: Input message for wsdl operation pspNotifyPaymentReq
    type: object
    properties:
      Envelope:
        xml:
          namespace: 'http://schemas.xmlsoap.org/soap/envelope/'
          prefix: soapenv
        type: object
        properties:
          Header:
            $ref: '#/definitions/pspNotifyPaymentHeader'
          Body:
            xml:
              namespace: 'http://schemas.xmlsoap.org/soap/envelope/'
              prefix: soapenv
            type: object
            properties:
              pspNotifyPaymentReq:
                $ref: '#/definitions/pspNotifyPaymentReq_element_pspfn'
            required:
              - pspNotifyPaymentReq
        required:
          - Body
    required:
      - Envelope
    x-ibm-schema:
      wsdl-port: '{http://pagopa-api.pagopa.gov.it/psp/pspForNode.wsdl}pspForNode_Port'
      wsdl-operation: pspNotifyPaymentReq
      wsdl-message-direction-or-name: pspNotifyPaymentReqRequest
    example: >-

      <soapenv:Envelope
      xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
       <soapenv:Header>
        <!-- The Security element should be removed if WS-Security is not enabled on the SOAP target-url -->
        <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
         <wsse:UsernameToken>
          <wsse:Username>string</wsse:Username>
          <wsse:Password>string</wsse:Password>
          <wsse:Nonce EncodingType="string">string</wsse:Nonce>
          <wsu:Created>string</wsu:Created>
         </wsse:UsernameToken>
         <wsu:Timestamp wsu:Id="string">
          <wsu:Created>string</wsu:Created>
          <wsu:Expires>string</wsu:Expires>
         </wsu:Timestamp>
        </wsse:Security>
       </soapenv:Header>
       <soapenv:Body>
        <pspfn:pspNotifyPaymentReq xmlns:pspfn="http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd"><!-- mandatory -->
         <idPSP><!-- mandatory -->string</idPSP>
         <idBrokerPSP><!-- mandatory -->string</idBrokerPSP>
         <idChannel><!-- mandatory -->string</idChannel>
         <paymentToken><!-- mandatory -->string</paymentToken>
         <paymentDescription><!-- mandatory -->string</paymentDescription>
         <fiscalCodePA><!-- mandatory -->string</fiscalCodePA>
         <companyName><!-- mandatory -->string</companyName>
         <officeName>string</officeName>
         <creditorReferenceId><!-- mandatory -->string</creditorReferenceId>
         <debtAmount><!-- mandatory -->999999996.99</debtAmount>
         <transferList><!-- mandatory -->
          <transfer><!-- mandatory --><!-- between 1 and 5 repetitions of this element -->
           <idTransfer><!-- mandatory -->3</idTransfer>
           <transferAmount><!-- mandatory -->999999996.99</transferAmount>
           <fiscalCodePA><!-- mandatory -->string</fiscalCodePA>
           <IBAN><!-- mandatory -->string</IBAN>
           <remittanceInformation><!-- mandatory -->string</remittanceInformation>
          </transfer>
         </transferList>
         <creditCardPayment><!-- mandatory -->
          <rrn><!-- mandatory -->string</rrn>
          <outcomePaymentGateway><!-- mandatory -->string</outcomePaymentGateway>
          <totalAmount><!-- mandatory -->999999996.99</totalAmount>
          <fee><!-- mandatory -->999999996.99</fee>
          <timestampOperation><!-- mandatory -->2016-04-18T14:07:37</timestampOperation>
          <authorizationCode><!-- mandatory -->string</authorizationCode>
          <paymentGateway>string</paymentGateway>
         </creditCardPayment>
        </pspfn:pspNotifyPaymentReq>
       </soapenv:Body>
      </soapenv:Envelope>
  pspNotifyPaymentHeader:
    description: Input headers for wsdl operation pspNotifyPaymentReq
    type: object
    properties:
      Security:
        $ref: '#/definitions/Security'
  pspNotifyPaymentOutput:
    description: Output message for wsdl operation pspNotifyPaymentReq
    type: object
    properties:
      Envelope:
        xml:
          namespace: 'http://schemas.xmlsoap.org/soap/envelope/'
          prefix: soapenv
        type: object
        properties:
          Body:
            xml:
              namespace: 'http://schemas.xmlsoap.org/soap/envelope/'
              prefix: soapenv
            type: object
            properties:
              pspNotifyPaymentRes:
                $ref: '#/definitions/pspNotifyPaymentRes_element_pspfn'
        required:
          - Body
    required:
      - Envelope
    x-ibm-schema:
      wsdl-port: '{http://pagopa-api.pagopa.gov.it/psp/pspForNode.wsdl}pspForNode_Port'
      wsdl-operation: pspNotifyPaymentReq
      wsdl-message-direction-or-name: pspNotifyPaymentReqResponse
    example: >-

      <soapenv:Envelope
      xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
       <soapenv:Body>
        <pspfn:pspNotifyPaymentRes xmlns:pspfn="http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd">
         <outcome><!-- mandatory -->string</outcome>
         <fault>
          <faultCode><!-- mandatory -->string</faultCode>
          <faultString><!-- mandatory -->string</faultString>
          <id><!-- mandatory -->string</id>
          <description>string</description>
          <serial>3</serial>
          <originalFaultCode>string</originalFaultCode>
          <originalFaultString>string</originalFaultString>
          <originalDescription>string</originalDescription>
         </fault>
        </pspfn:pspNotifyPaymentRes>
       </soapenv:Body>
      </soapenv:Envelope>
  pspNotifyPaymentReq_element_pspfn:
    xml:
      namespace: 'http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd'
      prefix: pspfn
      name: pspNotifyPaymentReq
    type: object
    properties:
      idPSP:
        $ref: '#/definitions/stIdPSP_type_pspfn'
      idBrokerPSP:
        $ref: '#/definitions/stIdBroker_type_pspfn'
      idChannel:
        $ref: '#/definitions/stIdChannel_type_pspfn'
      paymentToken:
        $ref: '#/definitions/stPaymentToken_type_pspfn'
      paymentDescription:
        $ref: '#/definitions/stText140_type_pspfn'
      fiscalCodePA:
        $ref: '#/definitions/stFiscalCodePA_type_pspfn'
      companyName:
        $ref: '#/definitions/stText140_type_pspfn'
      officeName:
        $ref: '#/definitions/stText140_type_pspfn'
      creditorReferenceId:
        $ref: '#/definitions/stText35_type_pspfn'
      debtAmount:
        $ref: '#/definitions/stAmount_type_pspfn'
        description: EC services amout ( without fee )
      transferList:
        $ref: '#/definitions/ctTransferListPSP_type_pspfn'
      creditCardPayment:
        $ref: '#/definitions/ctCreditCardPayment_type_pspfn'
        description: |-
          It describes an on-line payment with cards ( credit / debit ) . 
                        Plese see project integration documentation for further details
    required:
      - idPSP
      - idBrokerPSP
      - idChannel
      - paymentToken
      - paymentDescription
      - fiscalCodePA
      - companyName
      - creditorReferenceId
      - debtAmount
      - transferList
      - creditCardPayment
    example: >-

      <pspfn:pspNotifyPaymentReq
      xmlns:pspfn="http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd">
       <idPSP><!-- mandatory -->string</idPSP>
       <idBrokerPSP><!-- mandatory -->string</idBrokerPSP>
       <idChannel><!-- mandatory -->string</idChannel>
       <paymentToken><!-- mandatory -->string</paymentToken>
       <paymentDescription><!-- mandatory -->string</paymentDescription>
       <fiscalCodePA><!-- mandatory -->string</fiscalCodePA>
       <companyName><!-- mandatory -->string</companyName>
       <officeName>string</officeName>
       <creditorReferenceId><!-- mandatory -->string</creditorReferenceId>
       <debtAmount><!-- mandatory -->999999996.99</debtAmount>
       <transferList><!-- mandatory -->
        <transfer><!-- mandatory --><!-- between 1 and 5 repetitions of this element -->
         <idTransfer><!-- mandatory -->3</idTransfer>
         <transferAmount><!-- mandatory -->999999996.99</transferAmount>
         <fiscalCodePA><!-- mandatory -->string</fiscalCodePA>
         <IBAN><!-- mandatory -->string</IBAN>
         <remittanceInformation><!-- mandatory -->string</remittanceInformation>
        </transfer>
       </transferList>
       <creditCardPayment><!-- mandatory -->
        <rrn><!-- mandatory -->string</rrn>
        <outcomePaymentGateway><!-- mandatory -->string</outcomePaymentGateway>
        <totalAmount><!-- mandatory -->999999996.99</totalAmount>
        <fee><!-- mandatory -->999999996.99</fee>
        <timestampOperation><!-- mandatory -->2016-04-18T14:07:37</timestampOperation>
        <authorizationCode><!-- mandatory -->string</authorizationCode>
        <paymentGateway>string</paymentGateway>
       </creditCardPayment>
      </pspfn:pspNotifyPaymentReq>
  pspNotifyPaymentRes_element_pspfn:
    xml:
      namespace: 'http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd'
      prefix: pspfn
      name: pspNotifyPaymentRes
    allOf:
      - $ref: '#/definitions/ctResponse_type_pspfn'
      - type: object
        properties: {}
    example: >-

      <pspfn:pspNotifyPaymentRes
      xmlns:pspfn="http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd">
       <outcome><!-- mandatory -->string</outcome>
       <fault>
        <faultCode><!-- mandatory -->string</faultCode>
        <faultString><!-- mandatory -->string</faultString>
        <id><!-- mandatory -->string</id>
        <description>string</description>
        <serial>3</serial>
        <originalFaultCode>string</originalFaultCode>
        <originalFaultString>string</originalFaultString>
        <originalDescription>string</originalDescription>
       </fault>
      </pspfn:pspNotifyPaymentRes>
  stIdPSP_type_pspfn:
    xml:
      namespace: ''
    description: >-
      PSP Identifier, it has been assigned from pagoPA.


      Code used in the primitive web service and in its objects exchanged with
      the NodoSPC.


      The code is generally represented by the **BIC** code (_Bank Identifier
      Code_) of the PSP.


      In the absence of the BIC code, or to handle particular situations,
      another code can be used, as long as it uniquely identifies the PSP.
    type: string
    minLength: 1
    maxLength: 35
    x-xsi-type: stIdPSP
    x-xsi-type-xml:
      namespace: 'http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd'
      prefix: pspfn
    x-xsi-type-uniquename: stIdPSP_type_pspfn
  stIdBroker_type_pspfn:
    xml:
      namespace: ''
    description: >-
      Broker Identifier, it has been assigned from pagoPA.


      Identification of the intermediary/broker of the PSP that provides the
      specific access (channel) to the PSP for the service delivery.


      _Note_: The intermediary/broker can coincide with the PSP itself
    type: string
    minLength: 1
    maxLength: 35
    x-xsi-type: stIdBroker
    x-xsi-type-xml:
      namespace: 'http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd'
      prefix: pspfn
    x-xsi-type-uniquename: stIdBroker_type_pspfn
  stIdChannel_type_pspfn:
    xml:
      namespace: ''
    description: >-
      Channel Identifier, it identifies a payment service category and through
      which the transaction is carried out.


      A Channel identifier belongs to only one PSP intermediary/broker and
      consequently must be unique with respect to the PSP.
    type: string
    minLength: 1
    maxLength: 35
    x-xsi-type: stIdChannel
    x-xsi-type-xml:
      namespace: 'http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd'
      prefix: pspfn
    x-xsi-type-uniquename: stIdChannel_type_pspfn
  stPaymentToken_type_pspfn:
    xml:
      namespace: ''
    description: >-
      It is generated by the system during the payment activation phase, it is
      the correlation identifier to match activation and payment outcome. 


      - **PA OLD**: the PA receives it into `CCP` (_CodiceContestoPagamento_)
      which uniquely identifies a single payment activity started from PSP.

      - **PA NEW**: the PA does not know it, it will receive it as a unique
      identifier of the receipt.
    type: string
    minLength: 1
    maxLength: 35
    x-xsi-type: stPaymentToken
    x-xsi-type-xml:
      namespace: 'http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd'
      prefix: pspfn
    x-xsi-type-uniquename: stPaymentToken_type_pspfn
  stText140_type_pspfn:
    xml:
      namespace: ''
    type: string
    minLength: 1
    maxLength: 140
    x-xsi-type: stText140
    x-xsi-type-xml:
      namespace: 'http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd'
      prefix: pspfn
    x-xsi-type-uniquename: stText140_type_pspfn
  stFiscalCodePA_type_pspfn:
    xml:
      namespace: ''
    type: string
    pattern: '[0-9]{11}'
    minLength: 11
    maxLength: 11
    x-xsi-type: stFiscalCodePA
    x-xsi-type-xml:
      namespace: 'http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd'
      prefix: pspfn
    x-xsi-type-uniquename: stFiscalCodePA_type_pspfn
  stText35_type_pspfn:
    xml:
      namespace: ''
    type: string
    minLength: 1
    maxLength: 35
    x-xsi-type: stText35
    x-xsi-type-xml:
      namespace: 'http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd'
      prefix: pspfn
    x-xsi-type-uniquename: stText35_type_pspfn
  stAmount_type_pspfn:
    xml:
      namespace: ''
    type: number
    maximum: 999999999.99
    pattern: '\d+\.\d{2}'
    x-xsi-type: stAmount
    x-xsi-type-xml:
      namespace: 'http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd'
      prefix: pspfn
    x-xsi-type-uniquename: stAmount_type_pspfn
  ctTransferListPSP_type_pspfn:
    xml:
      namespace: ''
      prefix: ''
    type: object
    properties:
      transfer:
        type: array
        minItems: 1
        maxItems: 5
        items:
          $ref: '#/definitions/ctTransferPSP_type_pspfn'
    required:
      - transfer
    x-xsi-type: ctTransferListPSP
    x-xsi-type-xml:
      namespace: 'http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd'
      prefix: pspfn
    x-xsi-type-uniquename: ctTransferListPSP_type_pspfn
  ctCreditCardPayment_type_pspfn:
    xml:
      namespace: ''
      prefix: ''
    type: object
    properties:
      rrn:
        xml:
          namespace: ''
        type: string
      outcomePaymentGateway:
        xml:
          namespace: ''
        description: outcome from the payment gateway
        type: string
      totalAmount:
        $ref: '#/definitions/stAmount_type_pspfn'
        description: transaction amount  = fee + EC service amount
      fee:
        $ref: '#/definitions/stAmount_type_pspfn'
      timestampOperation:
        $ref: '#/definitions/stISODateTime_type_pspfn'
      authorizationCode:
        $ref: '#/definitions/stText6_type_pspfn'
      paymentGateway:
        $ref: '#/definitions/stText35_type_pspfn'
        description: Describe the payment gateway used ( es. VPOS )
    required:
      - rrn
      - outcomePaymentGateway
      - totalAmount
      - fee
      - timestampOperation
      - authorizationCode
    x-xsi-type: ctCreditCardPayment
    x-xsi-type-xml:
      namespace: 'http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd'
      prefix: pspfn
    x-xsi-type-uniquename: ctCreditCardPayment_type_pspfn
  stOutcome_type_pspfn:
    xml:
      namespace: ''
    type: string
    enum:
      - OK
      - KO
    x-xsi-type: stOutcome
    x-xsi-type-xml:
      namespace: 'http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd'
      prefix: pspfn
    x-xsi-type-uniquename: stOutcome_type_pspfn
  ctFaultBean_type_pspfn:
    xml:
      namespace: ''
      prefix: ''
    type: object
    properties:
      faultCode:
        xml:
          namespace: ''
        type: string
      faultString:
        xml:
          namespace: ''
        type: string
      id:
        xml:
          namespace: ''
        type: string
      description:
        xml:
          namespace: ''
        type: string
      serial:
        xml:
          namespace: ''
        type: integer
        format: int32
      originalFaultCode:
        xml:
          namespace: ''
        type: string
      originalFaultString:
        xml:
          namespace: ''
        type: string
      originalDescription:
        xml:
          namespace: ''
        type: string
    required:
      - faultCode
      - faultString
      - id
    x-xsi-type: ctFaultBean
    x-xsi-type-xml:
      namespace: 'http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd'
      prefix: pspfn
    x-xsi-type-uniquename: ctFaultBean_type_pspfn
  ctTransferPSP_type_pspfn:
    xml:
      namespace: ''
      prefix: ''
    type: object
    properties:
      idTransfer:
        $ref: '#/definitions/stIdTransfer_type_pspfn'
      transferAmount:
        $ref: '#/definitions/stAmount_type_pspfn'
      fiscalCodePA:
        $ref: '#/definitions/stFiscalCodePA_type_pspfn'
      IBAN:
        $ref: '#/definitions/stIBAN_type_pspfn'
      remittanceInformation:
        $ref: '#/definitions/stText140_type_pspfn'
    required:
      - idTransfer
      - transferAmount
      - fiscalCodePA
      - IBAN
      - remittanceInformation
    x-xsi-type: ctTransferPSP
    x-xsi-type-xml:
      namespace: 'http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd'
      prefix: pspfn
    x-xsi-type-uniquename: ctTransferPSP_type_pspfn
  stISODateTime_type_pspfn:
    xml:
      namespace: ''
    type: string
    format: date-time
    x-xsi-type: stISODateTime
    x-xsi-type-xml:
      namespace: 'http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd'
      prefix: pspfn
    x-xsi-type-uniquename: stISODateTime_type_pspfn
  stText6_type_pspfn:
    xml:
      namespace: ''
    type: string
    minLength: 1
    maxLength: 6
    x-xsi-type: stText6
    x-xsi-type-xml:
      namespace: 'http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd'
      prefix: pspfn
    x-xsi-type-uniquename: stText6_type_pspfn
  stIdTransfer_type_pspfn:
    xml:
      namespace: ''
    type: integer
    format: int32
    enum:
      - 1
      - 2
      - 3
      - 4
      - 5
    x-xsi-type: stIdTransfer
    x-xsi-type-xml:
      namespace: 'http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd'
      prefix: pspfn
    x-xsi-type-uniquename: stIdTransfer_type_pspfn
  stIBAN_type_pspfn:
    xml:
      namespace: ''
    type: string
    pattern: '[a-zA-Z]{2,2}[0-9]{2,2}[a-zA-Z0-9]{1,30}'
    x-xsi-type: stIBAN
    x-xsi-type-xml:
      namespace: 'http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd'
      prefix: pspfn
    x-xsi-type-uniquename: stIBAN_type_pspfn
  ctResponse_type_pspfn:
    xml:
      namespace: ''
      prefix: ''
    type: object
    properties:
      outcome:
        $ref: '#/definitions/stOutcome_type_pspfn'
      fault:
        $ref: '#/definitions/ctFaultBean_type_pspfn'
    required:
      - outcome
    x-ibm-discriminator: true
    x-xsi-type: ctResponse
    x-xsi-type-xml:
      namespace: 'http://pagopa-api.pagopa.gov.it/psp/pspForNode.xsd'
      prefix: pspfn
    x-xsi-type-uniquename: ctResponse_type_pspfn