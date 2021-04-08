#!/bin/zsh

echo "Build creation form for CDI:CatalogoDatiInformativiPerPSP ..."
xsltproc -o ./out/form_CatalogoDatiInformativiPerPSP.html ./xsd2html2xml/xsd2html2xml.xsl CatalogoDatiInformativiPerPSP.xsd

echo "Build creation docuementation for CDI:CatalogoDatiInformativiPerPSP ..."
xsltproc -o ./out/CatalogoDatiInformativiPerPSP.html ./xs3p/xs3p.xsl CatalogoDatiInformativiPerPSP.xsd

echo "Done!"


open "./out/CatalogoDatiInformativiPerPSP.html"
open "./out/form_CatalogoDatiInformativiPerPSP.html"