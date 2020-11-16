#!/bin/bash


FILE=$1
echo $FILE

sed -i.bak '4s/.*/  x-logo: \
    backgroundColor: '#FFFFFF' \
    url: "https:\/\/www.cittametropolitana.genova.it\/sites\/default\/files\/siti-tematici\/Logo%20PagoPA.jpg" \
  description: \
    $ref: description.md/' \
${FILE}
