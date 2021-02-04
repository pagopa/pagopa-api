#!/bin/bash


FILE=$1
echo $FILE

sed -i.bak '4s/.*/  x-logo: \
    backgroundColor: '#FFFFFF' \
    url: "https:\/\/www.pagopa.gov.it\/assets\/images\/pagopa-logo.png" \
  description: \
$ref: description.md/' \
${FILE}
