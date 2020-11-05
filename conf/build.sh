#!/bin/zsh

 xsltproc -o ./out/form_CatalogoDatiInformativi.html ./xsd2html2xml/xsd2html2xml.xsl CatalogoDatiInformativi.xsd

xsltproc -o ./out/CatalogoDatiInformativi.html ./xs3p/xs3p.xsl CatalogoDatiInformativi.xsd   
