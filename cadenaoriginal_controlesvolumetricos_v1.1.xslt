<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions" xmlns:controlesvolumetricos="http://www.sat.gob.mx/esquemas/controlesvolumetricos">
  <xsl:output method="text" version="1.0" encoding="UTF-8" indent="no" />
  <!-- Con el siguiente método se establece que la salida deberá ser en texto -->
  <xsl:output method="text" version="1.0" encoding="UTF-8" indent="no" />
  <!-- En esta sección se define la inclusión de las plantillas de utilerías para colapsar espacios -->
  <!-- <xsl:include href="http://www.sat.gob.mx/esquemas/utilerias.xslt"/> -->
  <xsl:include href="C:\Program Files (x86)\ATIO\ENVOL\ENVOL\Cadenaoriginal.xml" />
  <!-- Aquí iniciamos el procesamiento de la cadena original con su | inicial y el terminador || -->
  <xsl:template match="/">|<xsl:apply-templates select="/controlesvolumetricos:ControlesVolumetricos" />||</xsl:template>
  <xsl:template match="controlesvolumetricos:ControlesVolumetricos">
    <!--Iniciamos el tratamiento de los atributos de ControlesVolumetricos -->
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@version" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@rfc" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@rfcProveedorSw" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@claveClientePEMEX" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@claveEstacionServicio" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@noCertificado" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@certificado" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@fechaYHoraCorte" />
    </xsl:call-template>
    <!--Iniciamos el tratamiento de los elementos de ControlesVolumetricos -->
    <xsl:for-each select="./controlesvolumetricos:EXI">
      <xsl:apply-templates select="." />
    </xsl:for-each>
    <xsl:if test="./controlesvolumetricos:REC">
      <xsl:apply-templates select="./controlesvolumetricos:REC" />
    </xsl:if>
    <xsl:if test="./controlesvolumetricos:VTA">
      <xsl:apply-templates select="./controlesvolumetricos:VTA" />
    </xsl:if>
  </xsl:template>
  <xsl:template match="controlesvolumetricos:EXI">
    <!--Iniciamos el tratamiento de los atributos de EXI -->
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@numeroTanque" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@claveProductoPEMEX" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@volumenUtil" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@volumenFondaje" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@volumenAgua" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@volumenDisponible" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@volumenExtraccion" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@volumenRecepcion" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@temperatura" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@fechaYHoraEstaMedicion" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@fechaYHoraMedicionAnterior" />
    </xsl:call-template>
  </xsl:template>
  <xsl:template match="controlesvolumetricos:REC">
    <!--Iniciamos el tratamiento de los atributos de REC -->
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@totalRecepciones" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@totalDocumentos" />
    </xsl:call-template>
    <!--Iniciamos el tratamiento del los elementos de REC -->
    <xsl:for-each select="./controlesvolumetricos:RECCabecera">
      <xsl:apply-templates select="." />
    </xsl:for-each>
    <xsl:for-each select="./controlesvolumetricos:RECDetalle">
      <xsl:apply-templates select="." />
    </xsl:for-each>
    <xsl:for-each select="./controlesvolumetricos:RECDocumentos">
      <xsl:apply-templates select="." />
    </xsl:for-each>
  </xsl:template>
  <xsl:template match="controlesvolumetricos:RECCabecera">
    <!--Iniciamos el tratamiento de los atributos de RECCabecera -->
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@folioUnicoRecepcion" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@claveProductoPEMEX" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@folioUnicoRelacion" />
    </xsl:call-template>
  </xsl:template>
  <xsl:template match="controlesvolumetricos:RECDetalle">
    <!--Iniciamos el tratamiento de los atributos de RECDetalle -->
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@folioUnicoRecepcion" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@numeroDeTanque" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@volumenInicialTanque" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@volumenFinalTanque" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@volumenRecepcion" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@temperatura" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@fechaYHoraRecepcion" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@folioUnicoRelacion" />
    </xsl:call-template>
  </xsl:template>
  <xsl:template match="controlesvolumetricos:RECDocumentos">
    <!--Iniciamos el tratamiento de los atributos de RECDocumentos -->
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@folioUnicoRecepcion" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@terminalAlmacenamientoYDistribucion" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@tipoDocumento" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@fechaDocumento" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@folioDocumentoRecepcion" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@volumenDocumentadoPEMEX" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@claveVehiculo" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@folioUnicoRelacion" />
    </xsl:call-template>
  </xsl:template>
  <xsl:template match="controlesvolumetricos:VTA">
    <!--Iniciamos el tratamiento del los elementos de VTA -->
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@numTotalRegistrosDetalle" />
    </xsl:call-template>
    <xsl:for-each select="./controlesvolumetricos:VTACabecera">
      <xsl:apply-templates select="." />
    </xsl:for-each>
    <xsl:for-each select="./controlesvolumetricos:VTADetalle">
      <xsl:apply-templates select="." />
    </xsl:for-each>
  </xsl:template>
  <xsl:template match="controlesvolumetricos:VTACabecera">
    <!--Iniciamos el tratamiento de los atributos de VTACabecera -->
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@numeroTotalRegistrosDetalle" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@numeroDispensario" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@identificadorManguera" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@claveProductoPEMEX" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@sumatoriaVolumenDespachado" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@sumatoriaVentas" />
    </xsl:call-template>
  </xsl:template>
  <xsl:template match="controlesvolumetricos:VTADetalle">
    <!--Iniciamos el tratamiento de los atributos de VTADetalle -->
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@tipoDeRegistro" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@numeroUnicoTransaccionVenta" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@numeroDispensario" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@identificadorManguera" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@claveProductoPEMEX" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@volumenDespachado" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@precioUnitarioProducto" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@importeTotalTransaccion" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@fechaYHoraTransaccionVenta" />
    </xsl:call-template>
  </xsl:template>
</xsl:stylesheet>