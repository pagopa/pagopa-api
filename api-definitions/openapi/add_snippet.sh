#!/bin/bash


FILE=$1
echo $FILE

case $FILE in 

psp*)
sed -i.bak '4s/.*/  x-logo: \
    backgroundColor: '#FFFFFF' \
    url: "https:\/\/www.pagopa.gov.it\/assets\/images\/pagopa-logo.png" \
  description: \
      $ref: descriptionPSP.md/' \
${FILE}
;;

node*)

sed -i.bak '4s/.*/  x-logo: \
    backgroundColor: '#FFFFFF' \
    url: "https:\/\/www.pagopa.gov.it\/assets\/images\/pagopa-logo.png" \
  description: \
      $ref: description.md/' \
${FILE}

;;

pa*)
sed -i.bak '4s/.*/  x-logo: \
    backgroundColor: '#FFFFFF' \
    url: "https:\/\/www.pagopa.gov.it\/assets\/images\/pagopa-logo.png" \
  description: \
      $ref: descriptionPA.md/' \
${FILE}
;;


esac

