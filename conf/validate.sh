#!/bin/zsh

echo "Build creation form for CDI:CatalogoDatiInformativiPSP ..."
xsltproc -o ./out/form_CatalogoDatiInformativiPSP.html ./xsd2html2xml/xsd2html2xml.xsl CatalogoDatiInformativiPSP.xsd

echo "Build creation docuementation for CDI:CatalogoDatiInformativiPSP ..."
xsltproc -o ./out/CatalogoDatiInformativiPSP.html ./xs3p/xs3p.xsl CatalogoDatiInformativiPSP.xsd

echo "Done!"


open "./out/CatalogoDatiInformativiPSP.html"
open "./out/form_CatalogoDatiInformativiPSP.html"