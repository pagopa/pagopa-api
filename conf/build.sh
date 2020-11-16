#!/bin/zsh

echo "Build creation form for CDI:CatalogoDatiInformativi ..."
xsltproc -o ./out/form_CatalogoDatiInformativi.html ./xsd2html2xml/xsd2html2xml.xsl CatalogoDatiInformativi.xsd

echo "Build creation docuementation for CDI:CatalogoDatiInformativi ..."
xsltproc -o ./out/CatalogoDatiInformativi.html ./xs3p/xs3p.xsl CatalogoDatiInformativi.xsd

echo "Done!"


open "./out/CatalogoDatiInformativi.html"
open "./out/form_CatalogoDatiInformativi.html"