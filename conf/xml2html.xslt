<?xml version="1.0" encoding="UTF-8"?> 
<xsl:stylesheet version="1.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  

<xsl:template match="/"> 
 <html> 
 <body> 
  <h1 align="center">PSP Account Viewer</h1>
  <p align="center"><xsl:value-of select="listaInformativePSP/informativaPSP/ragioneSociale"/> </p>
  <h2 align="center"> Identificativo PSP </h2>
  <p align="center"><xsl:value-of select="listaInformativePSP/informativaPSP/identificativoPSP"/></p>
 
  <p align="center">
  <img align="center" width="200" height="200" > 
    <xsl:attribute name="src">
      <xsl:value-of select="concat('data:image/png;base64,',listaInformativePSP/informativaPSP/informativaMaster/logoPSP)"/>
    </xsl:attribute>
  </img>
  </p>

   <table border="3" align="center" > 
   <tr> 
    <th>Intermediario ( CF )</th> 
    <th>Canale</th> 
    <th>Fascia</th> 
    <th>Costo</th> 
   </tr> 
    <xsl:for-each select="listaInformativePSP/informativaPSP/listaInformativaDetail/informativaDetail/costiServizio/listaFasceCostoServizio/fasciaCostoServizio"> 
   <tr> 
    <td><xsl:value-of select="../../../identificativoIntermediario"/></td> 
    <td><xsl:value-of select="../../../identificativoCanale"/></td> 
    <td><xsl:value-of select="importoMassimoFascia"/></td> 
    <td><xsl:value-of select="valoreCommissione"/></td> 
   </tr> 
    </xsl:for-each> 
    </table> 
</body> 
</html> 
</xsl:template> 
</xsl:stylesheet>