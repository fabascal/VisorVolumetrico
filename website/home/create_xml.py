# -*- encoding: utf-8 -*-
#- minidom_Build_XML.py
#- Copyright (c) 2018 HerongYang.com. All Rights Reserved.
#
import xml.dom.minidom
from website.home.get_number import get_number, generate_sales_data
from website.settings.models import Empresa, Tanques, Version
from collections import OrderedDict
from website.home.utils.sign import signDoc
from website.home.utils.date_exi import FechaHora, FechaHora_minus_one_day

title = 'controlesvolumetricos'
root_segment = 'ControlesVolumetricos'
version_label = 'version'
rfc = 'rfc'
rfcProveedorSw = 'rfcProveedorSw'
numeroPermisoCRE = 'numeroPermisoCRE'
sello = 'sello'
sello_value = 'hlWwTDcBMGpxP1r30kQiPEe3DlIQZhWpit1bkPqXJFE2MMcTsLxpRD2dBGEOdvPZIT6MiiuTCc8Yl59leygz1EDj1bwRfdGkOcS2b/7UTm1Q30xr2pd48HcS1lE9A/lM/kGib0Pngi/obOspzPX6kurBnVKneornMv4LKoGmSpw='
noCertificado = 'noCertificado'
certificado = 'certificado'
fechaYHoraCorte = 'fechaYHoraCorte'
fechaYHoraCorte_value = '2021-12-20T23:59:59'
xmlns = 'xmlns'
xmlns_value = 'http://www.sat.gob.mx/esquemas/controlesvolumetricos'
xsi = 'xsi'
xsi_value = 'http://www.w3.org/2001/XMLSchema-instance'
schemaLocation  = 'schemaLocation'
schemaLocation_value = 'http://www.sat.gob.mx/esquemas/controlesvolumetricos http://www.sat.gob.mx/fichas_tematicas/controles_volumetricos/Documents/controlesvolumetricos_v1_2.xsd'
exi  = 'EXI'
exi_numeroTanque = 'numeroTanque'
claveProducto = 'claveProducto'
claveSubProducto = 'claveSubProducto'
composicionOctanajeDeGasolina = 'composicionOctanajeDeGasolina'
gasolinaConEtanol = 'gasolinaConEtanol'
volumenUtil = 'volumenUtil'
volumenFondaje = 'volumenFondaje'
volumenAgua = 'volumenAgua'
volumenDisponible = 'volumenDisponible'
volumenExtraccion = 'volumenExtraccion'
volumenRecepcion = 'volumenRecepcion'
temperatura = 'temperatura'
fechaYHoraEstaMedicion_label = 'fechaYHoraEstaMedicion'
fechaYHoraMedicionAnterior_label = 'fechaYHoraMedicionAnterior'
rec = 'REC'
RECCabecera_label = 'RECCabecera'
RECDetalle_label = 'RECDetalle'
totalRecepciones_label = 'totalRecepciones'
totalDocumentos_label = 'totalDocumentos'
claveClientePEMEX_label = 'claveClientePEMEX'
claveEstacionServicio_label = 'claveEstacionServicio'
claveProductoPEMEX_label = 'claveProductoPEMEX'
folioUnicoRecepcion_label = 'folioUnicoRecepcion'
folioUnicoRelacion_label = 'folioUnicoRelacion'
volumenInicialTanque_label = 'volumenInicialTanque'
volumenFinalTanque_label = 'volumenFinalTanque'
volumenRecepcion_label = 'volumenRecepcion'
fechaYHoraRecepcion_label = 'fechaYHoraRecepcion'
vta = 'VTA'
numTotalRegistrosDetalle_label = 'numTotalRegistrosDetalle'
VTACabecera_label = 'VTACabecera'
numeroTotalRegistrosDetalle_label = 'numeroTotalRegistrosDetalle'
numeroDispensario_label = 'numeroDispensario'
identificadorManguera_label = 'identificadorManguera'
sumatoriaVolumenDespachado_label = 'sumatoriaVolumenDespachado'
sumatoriaVentas_label = 'sumatoriaVentas'
VTADetalle_label = 'VTADetalle'

#Version 1.1
def create_xml_11(estacion, data):
    cadena_original = []
    empresa = Empresa.query.get(estacion.id_empresa)
    version = Version.query.get(data['id_version'])
    doc = xml.dom.minidom.Document()
    root = doc.createElement('{0}:{1}'.format(title,root_segment))  # TOP-LEVEL ROOT
    root.setAttribute(version_label,version.nombre)
    cadena_original.append(version.nombre)
    root.setAttribute(rfc,empresa.rfc)
    cadena_original.append(empresa.rfc)
    root.setAttribute(rfcProveedorSw,empresa.rfcProveedorSW)
    cadena_original.append(empresa.rfcProveedorSW)
    root.setAttribute(claveClientePEMEX_label,estacion.claveClientePEMEX)
    cadena_original.append(estacion.claveClientePEMEX)
    root.setAttribute(claveEstacionServicio_label,estacion.claveEstacionServicio)
    cadena_original.append(estacion.claveEstacionServicio)
    root.setAttribute(sello,"")
    root.setAttribute(noCertificado,estacion.noCertificado)
    cadena_original.append(estacion.noCertificado)
    root.setAttribute(certificado,estacion.certificado_value)
    cadena_original.append(estacion.certificado_value)
    root.setAttribute(fechaYHoraCorte,fechaYHoraCorte_value)
    cadena_original.append(fechaYHoraCorte_value)
    root.setAttribute('{0}:{1}'.format(xmlns,title),xmlns_value)
    
    doc.appendChild(root)
    for index, tanque in data['tanques'].items():
        tanqueElem = doc.createElement('{0}:{1}'.format(title,exi))
        tanqueElem.setAttribute(exi_numeroTanque,str(tanque['no_tanque']))
        cadena_original.append(str(tanque['no_tanque']))
        tanqueElem.setAttribute(claveProductoPEMEX_label,str(tanque['claveProductoPEMEX']))
        cadena_original.append(str(tanque['claveProductoPEMEX']))
        tanqueElem.setAttribute(volumenUtil,str(tanque['volumenUtil']))
        cadena_original.append(str(tanque['volumenUtil']))
        tanqueElem.setAttribute(volumenFondaje,str(tanque['volumenFondaje']))
        cadena_original.append(str(tanque['volumenFondaje']))
        tanqueElem.setAttribute(volumenAgua,str(tanque['volumenAgua']))
        cadena_original.append(str(tanque['volumenAgua']))
        tanqueElem.setAttribute(volumenDisponible,str("{:.2f}".format(float(tanque['volumenDisponible']))))#volumenDisponible
        cadena_original.append(str("{:.2f}".format(float(tanque['volumenDisponible']))))
        tanqueElem.setAttribute(volumenExtraccion,str("{:.2f}".format(float(tanque['volumenExtraccion'])))) #volumenExtraccion
        cadena_original.append(str("{:.2f}".format(float(tanque['volumenExtraccion']))))
        tanqueElem.setAttribute(volumenRecepcion,str("{:.2f}".format(float(tanque['volumenRecepcion'])))) #volumenRecepcion
        cadena_original.append(str("{:.2f}".format(float(tanque['volumenRecepcion']))))
        tanqueElem.setAttribute(temperatura,str(tanque['temperatura'])) 
        cadena_original.append(str(tanque['temperatura']))
        tanqueElem.setAttribute(fechaYHoraEstaMedicion_label,str(FechaHora(data['fecha'])))
        cadena_original.append(FechaHora(data['fecha']))
        tanqueElem.setAttribute(fechaYHoraMedicionAnterior_label,str(FechaHora_minus_one_day(data['fecha'])))
        cadena_original.append(FechaHora_minus_one_day(data['fecha']))
        #falta fecha y hora de medicion tanto para xml como para cadena
        #falta fecha y hora de medicion anterior tanto para xml como para cadena
        root.appendChild(tanqueElem)
    #Recepciones
    recepcionElem = doc.createElement('{0}:{1}'.format(title,rec))
    recepcionElem.setAttribute(totalRecepciones_label,str(len(data['recepciones'])))
    cadena_original.append(str(len(data['recepciones'])))
    recepcionElem.setAttribute(totalDocumentos_label,"0")
    cadena_original.append("0")
    #recepciones cabecera
    for index, recepcion in data['recepciones'].items():
        recepcionCabecera = doc.createElement('{0}:{1}'.format(title,RECCabecera_label))
        recepcionCabecera.setAttribute(folioUnicoRecepcion_label,recepcion['folioUnicoRecepcionCabecera'])
        cadena_original.append(recepcion['folioUnicoRecepcionCabecera'])
        recepcionCabecera.setAttribute(claveProductoPEMEX_label,data['tanques'][index]['claveProductoPEMEX'])
        cadena_original.append(data['tanques'][index]['claveProductoPEMEX'])
        recepcionCabecera.setAttribute(folioUnicoRelacion_label,recepcion['folioUnicoRelacion'])
        cadena_original.append(recepcion['folioUnicoRelacion'])
        recepcionElem.appendChild(recepcionCabecera)
    #Recepciones Detalle
    for index, recepcion in data['recepciones'].items():
        recepcionDetalle = doc.createElement('{0}:{1}'.format(title,RECDetalle_label))
        recepcionDetalle.setAttribute(folioUnicoRecepcion_label,recepcion['folioUnicoRecepcion'])
        cadena_original.append(recepcion['folioUnicoRecepcion'])
        recepcionDetalle.setAttribute("numeroDeTanque",data['tanques'][index]['no_tanque'])
        cadena_original.append(data['tanques'][index]['no_tanque'])
        recepcionDetalle.setAttribute(volumenInicialTanque_label,recepcion['volumenInicialTanque'])
        cadena_original.append(recepcion['volumenInicialTanque'])
        recepcionDetalle.setAttribute(volumenFinalTanque_label,recepcion['volumenFinalTanque'])
        cadena_original.append(recepcion['volumenFinalTanque'])
        recepcionDetalle.setAttribute(volumenRecepcion_label,recepcion['volumenRecepcion'])
        cadena_original.append(recepcion['volumenRecepcion'])
        recepcionDetalle.setAttribute(temperatura,data['tanques'][index]['temperatura'])
        cadena_original.append(data['tanques'][index]['temperatura'])
        recepcionDetalle.setAttribute(fechaYHoraRecepcion_label,str(data['fecha']))
        cadena_original.append(str(data['fecha']))
        recepcionDetalle.setAttribute(folioUnicoRelacion_label,recepcion['folioUnicoRelacion'])
        cadena_original.append(recepcion['folioUnicoRelacion'])
        recepcionElem.appendChild(recepcionDetalle)
    root.appendChild(recepcionElem)
    #falta validar los documentos
    #Ventas numTotalRegistrosDetalle
    ventas_data = generate_sales_data(data)
    ventasElem = doc.createElement('{0}:{1}'.format(title,vta))
    ventasElem.setAttribute(numTotalRegistrosDetalle_label,str(len(ventas_data)))
    cadena_original.append(str(len(ventas_data)))
    #ventas cabecera
    for clave_unica, datos in CabeceraVentas(ventas_data).items():
        dispensario, manguera, clave_producto = clave_unica.split('_')
        ventaCabecera = doc.createElement('{0}:{1}'.format(title,VTACabecera_label))
        ventaCabecera.setAttribute(numeroTotalRegistrosDetalle_label,str(datos['numero_registros']))
        cadena_original.append(str(datos['numero_registros']))
        ventaCabecera.setAttribute(numeroDispensario_label,dispensario)
        cadena_original.append(dispensario)
        ventaCabecera.setAttribute(identificadorManguera_label,manguera)
        cadena_original.append(manguera)
        ventaCabecera.setAttribute(claveProductoPEMEX_label,clave_producto)
        cadena_original.append(clave_producto)
        ventaCabecera.setAttribute(sumatoriaVolumenDespachado_label,str(round(datos['sumatoria_volumen'],4)))
        cadena_original.append(str(round(datos['sumatoria_volumen'],4)))
        ventaCabecera.setAttribute(sumatoriaVentas_label,str(round(datos['sumatoria_ventas'],2)))
        cadena_original.append(str(round(datos['sumatoria_ventas'],2)))
        ventasElem.appendChild(ventaCabecera)
    for venta in ventas_data:
        ventaDetalle = doc.createElement('{0}:{1}'.format(title,VTADetalle_label))
        ventaDetalle.setAttribute("tipoDeRegistro","D")
        cadena_original.append("D")
        ventaDetalle.setAttribute("numeroUnicoTransaccionVenta",str(venta['numeroUnicoTransaccionVenta']))
        cadena_original.append(str(venta['numeroUnicoTransaccionVenta']))
        ventaDetalle.setAttribute("numeroDispensario",str(venta['numeroDispensario']))
        cadena_original.append(str(venta['numeroDispensario']))
        ventaDetalle.setAttribute("identificadorManguera",str(venta['identificadorManguera']))
        cadena_original.append(str(venta['identificadorManguera']))
        ventaDetalle.setAttribute("claveProductoPEMEX",str(venta['claveProductoPEMEX']))
        cadena_original.append(str(venta['claveProductoPEMEX']))
        ventaDetalle.setAttribute("volumenDespachado",str(venta['volumenDespachado']))
        cadena_original.append(str(venta['volumenDespachado']))
        ventaDetalle.setAttribute("precioUnitarioProducto",str(venta['precioUnitarioProducto']))
        cadena_original.append(str(venta['precioUnitarioProducto']))
        ventaDetalle.setAttribute("importeTotalTransaccion",str(venta['importeTotalTransaccion']))
        cadena_original.append(str(venta['importeTotalTransaccion']))
        ventaDetalle.setAttribute("fechaYHoraTransaccionVenta",venta['fechaYHoraTransaccionVenta'])
        cadena_original.append(venta['fechaYHoraTransaccionVenta'])
        ventasElem.appendChild(ventaDetalle)
    root.appendChild(ventasElem)
    sello_data = signDoc(cadena_original, estacion.pem_file_path)
    root.setAttribute(sello, sello_data)
    return doc.toprettyxml(encoding="utf-8")

#Version 1.2
def create_xml_12(estacion, data):
    empresa = Empresa.query.get(estacion.id_empresa)
    version = Version.query.get(data['id_version'])
    doc = xml.dom.minidom.Document()
    root = doc.createElement('{0}:{1}'.format(title,root_segment))  # TOP-LEVEL ROOT
    root.setAttribute(version_label,version.nombre)
    root.setAttribute(rfc,empresa.rfc)
    root.setAttribute(rfcProveedorSw,empresa.rfcProveedorSW)
    root.setAttribute(claveClientePEMEX_label,estacion.claveClientePEMEX)
    root.setAttribute(claveEstacionServicio_label,estacion.claveEstacionServicio)
    root.setAttribute(sello,sello_value)
    root.setAttribute(noCertificado,estacion.noCertificado)
    root.setAttribute(certificado,estacion.certificado_value)
    root.setAttribute(fechaYHoraCorte,fechaYHoraCorte_value)
    root.setAttribute('{0}:{1}'.format(xmlns,title),xmlns_value)
    #root.setAttribute('{0}:{1}'.format(xmlns,xsi),xsi_value)
    #root.setAttribute('{0}:{1}'.format(xsi,schemaLocation),schemaLocation_value)
    doc.appendChild(root)
    for index, tanque in data['tanques'].items():
        tanqueElem = doc.createElement('{0}:{1}'.format(title,exi))
        tanqueElem.setAttribute(exi_numeroTanque,str(tanque['no_tanque']))
        tanqueElem.setAttribute(claveProductoPEMEX_label,str(tanque['claveProductoPEMEX']))
        tanqueElem.setAttribute(volumenUtil,str(tanque['volumenUtil']))
        tanqueElem.setAttribute(volumenFondaje,str(tanque['volumenFondaje']))
        tanqueElem.setAttribute(volumenAgua,str(tanque['volumenAgua']))
        tanqueElem.setAttribute(volumenDisponible,str("{:.2f}".format(float(tanque['volumenDisponible']))))#volumenDisponible
        tanqueElem.setAttribute(volumenExtraccion,str("{:.2f}".format(float(tanque['volumenExtraccion'])))) #volumenExtraccion
        tanqueElem.setAttribute(volumenRecepcion,str("{:.2f}".format(float(tanque['volumenRecepcion'])))) #volumenRecepcion
        tanqueElem.setAttribute(temperatura,str(tanque['temperatura'])) 
        root.appendChild(tanqueElem)
    #Recepciones
    recepcionElem = doc.createElement('{0}:{1}'.format(title,rec))
    recepcionElem.setAttribute(totalRecepciones_label,str(len(data['recepciones'])))
    recepcionElem.setAttribute(totalDocumentos_label,"0")
    #recepciones cabecera
    for index, recepcion in data['recepciones'].items():
        recepcionCabecera = doc.createElement('{0}:{1}'.format(title,RECCabecera_label))
        recepcionCabecera.setAttribute(folioUnicoRecepcion_label,recepcion['folioUnicoRecepcionCabecera'])
        recepcionCabecera.setAttribute(claveProductoPEMEX_label,data['tanques'][index]['claveProductoPEMEX'])
        recepcionCabecera.setAttribute(folioUnicoRelacion_label,recepcion['folioUnicoRelacion'])
        recepcionElem.appendChild(recepcionCabecera)
    #Recepciones Detalle
    for index, recepcion in data['recepciones'].items():
        recepcionDetalle = doc.createElement('{0}:{1}'.format(title,RECDetalle_label))
        recepcionDetalle.setAttribute(folioUnicoRecepcion_label,recepcion['folioUnicoRecepcion'])
        recepcionDetalle.setAttribute("numeroDeTanque",data['tanques'][index]['no_tanque'])
        recepcionDetalle.setAttribute(volumenInicialTanque_label,recepcion['volumenInicialTanque'])
        recepcionDetalle.setAttribute(volumenFinalTanque_label,recepcion['volumenFinalTanque'])
        recepcionDetalle.setAttribute(volumenRecepcion_label,recepcion['volumenRecepcion'])
        recepcionDetalle.setAttribute(temperatura,data['tanques'][index]['temperatura'])
        recepcionDetalle.setAttribute(fechaYHoraRecepcion_label,str(data['fecha']))
        recepcionDetalle.setAttribute(folioUnicoRelacion_label,recepcion['folioUnicoRelacion'])
        recepcionElem.appendChild(recepcionDetalle)
    root.appendChild(recepcionElem)
    #Ventas numTotalRegistrosDetalle
    ventas_data = generate_sales_data(data)
    ventasElem = doc.createElement('{0}:{1}'.format(title,vta))
    ventasElem.setAttribute(numTotalRegistrosDetalle_label,str(len(ventas_data)))
    #ventas cabecera
    for clave_unica, datos in CabeceraVentas(ventas_data).items():
        dispensario, manguera, clave_producto = clave_unica.split('_')
        ventaCabecera = doc.createElement('{0}:{1}'.format(title,VTACabecera_label))
        ventaCabecera.setAttribute(numeroTotalRegistrosDetalle_label,str(datos['numero_registros']))
        ventaCabecera.setAttribute(numeroDispensario_label,dispensario)
        ventaCabecera.setAttribute(identificadorManguera_label,manguera)
        ventaCabecera.setAttribute(claveProductoPEMEX_label,clave_producto)
        ventaCabecera.setAttribute(sumatoriaVolumenDespachado_label,str(datos['sumatoria_volumen']))
        ventaCabecera.setAttribute(sumatoriaVentas_label,str(datos['sumatoria_ventas']))
        ventasElem.appendChild(ventaCabecera)
    for venta in ventas_data:
        ventaDetalle = doc.createElement('{0}:{1}'.format(title,VTADetalle_label))
        ventaDetalle.setAttribute("tipoDeRegistro","D")
        ventaDetalle.setAttribute("numeroUnicoTransaccionVenta",str(venta['numeroUnicoTransaccionVenta']))
        ventaDetalle.setAttribute("numeroDispensario",str(venta['numeroDispensario']))
        ventaDetalle.setAttribute("identificadorManguera",str(venta['identificadorManguera']))
        ventaDetalle.setAttribute("claveProductoPEMEX",str(venta['claveProductoPEMEX']))
        ventaDetalle.setAttribute("volumenDespachado",str(venta['volumenDespachado']))
        ventaDetalle.setAttribute("precioUnitarioProducto",str(venta['precioUnitarioProducto']))
        ventaDetalle.setAttribute("importeTotalTransaccion",str(venta['importeTotalTransaccion']))
        ventaDetalle.setAttribute("fechaYHoraTransaccionVenta","2017-01-02T07:00:00")
        ventasElem.appendChild(ventaDetalle)  
    root.appendChild(ventasElem)
    return doc.toprettyxml(encoding="utf-8")

#Version 1.3
def create_xml_13(estacion, data):
    empresa = Empresa.query.get(estacion.id_empresa)
    version = Version.query.get(data['id_version'])
    doc = xml.dom.minidom.Document()
    root = doc.createElement('{0}:{1}'.format(title,root_segment))  # TOP-LEVEL ROOT
    root.setAttribute(version_label,version.nombre)
    root.setAttribute(rfc,empresa.rfc)
    root.setAttribute(rfcProveedorSw,empresa.rfcProveedorSW)
    root.setAttribute(claveClientePEMEX_label,estacion.claveClientePEMEX)
    root.setAttribute(claveEstacionServicio_label,estacion.claveEstacionServicio)
    root.setAttribute(sello,sello_value)
    root.setAttribute(noCertificado,estacion.noCertificado)
    root.setAttribute(certificado,estacion.certificado_value)
    root.setAttribute(fechaYHoraCorte,fechaYHoraCorte_value)
    root.setAttribute('{0}:{1}'.format(xmlns,title),xmlns_value)
    #root.setAttribute('{0}:{1}'.format(xmlns,xsi),xsi_value)
    #root.setAttribute('{0}:{1}'.format(xsi,schemaLocation),schemaLocation_value)
    doc.appendChild(root)
    for index, tanque in data['tanques'].items():
        tanqueElem = doc.createElement('{0}:{1}'.format(title,exi))
        tanqueElem.setAttribute(exi_numeroTanque,str(tanque['no_tanque']))
        tanqueElem.setAttribute(claveProductoPEMEX_label,str(tanque['claveProductoPEMEX']))
        tanqueElem.setAttribute(volumenUtil,str(tanque['volumenUtil']))
        tanqueElem.setAttribute(volumenFondaje,str(tanque['volumenFondaje']))
        tanqueElem.setAttribute(volumenAgua,str(tanque['volumenAgua']))
        tanqueElem.setAttribute(volumenDisponible,str("{:.2f}".format(float(tanque['volumenDisponible']))))#volumenDisponible
        tanqueElem.setAttribute(volumenExtraccion,str("{:.2f}".format(float(tanque['volumenExtraccion'])))) #volumenExtraccion
        tanqueElem.setAttribute(volumenRecepcion,str("{:.2f}".format(float(tanque['volumenRecepcion'])))) #volumenRecepcion
        tanqueElem.setAttribute(temperatura,str(tanque['temperatura'])) 
        root.appendChild(tanqueElem)
    #Recepciones
    recepcionElem = doc.createElement('{0}:{1}'.format(title,rec))
    recepcionElem.setAttribute(totalRecepciones_label,str(len(data['recepciones'])))
    recepcionElem.setAttribute(totalDocumentos_label,"0")
    #recepciones cabecera
    for index, recepcion in data['recepciones'].items():
        recepcionCabecera = doc.createElement('{0}:{1}'.format(title,RECCabecera_label))
        recepcionCabecera.setAttribute(folioUnicoRecepcion_label,recepcion['folioUnicoRecepcionCabecera'])
        recepcionCabecera.setAttribute(claveProductoPEMEX_label,data['tanques'][index]['claveProductoPEMEX'])
        recepcionCabecera.setAttribute(folioUnicoRelacion_label,recepcion['folioUnicoRelacion'])
        recepcionElem.appendChild(recepcionCabecera)
    #Recepciones Detalle
    for index, recepcion in data['recepciones'].items():
        recepcionDetalle = doc.createElement('{0}:{1}'.format(title,RECDetalle_label))
        recepcionDetalle.setAttribute(folioUnicoRecepcion_label,recepcion['folioUnicoRecepcion'])
        recepcionDetalle.setAttribute("numeroDeTanque",data['tanques'][index]['no_tanque'])
        recepcionDetalle.setAttribute(volumenInicialTanque_label,recepcion['volumenInicialTanque'])
        recepcionDetalle.setAttribute(volumenFinalTanque_label,recepcion['volumenFinalTanque'])
        recepcionDetalle.setAttribute(volumenRecepcion_label,recepcion['volumenRecepcion'])
        recepcionDetalle.setAttribute(temperatura,data['tanques'][index]['temperatura'])
        recepcionDetalle.setAttribute(fechaYHoraRecepcion_label,str(data['fecha']))
        recepcionDetalle.setAttribute(folioUnicoRelacion_label,recepcion['folioUnicoRelacion'])
        recepcionElem.appendChild(recepcionDetalle)
    root.appendChild(recepcionElem)
    #Ventas numTotalRegistrosDetalle
    ventas_data = generate_sales_data(data)
    ventasElem = doc.createElement('{0}:{1}'.format(title,vta))
    ventasElem.setAttribute(numTotalRegistrosDetalle_label,str(len(ventas_data)))
    #ventas cabecera
    for clave_unica, datos in CabeceraVentas(ventas_data).items():
        dispensario, manguera, clave_producto = clave_unica.split('_')
        ventaCabecera = doc.createElement('{0}:{1}'.format(title,VTACabecera_label))
        ventaCabecera.setAttribute(numeroTotalRegistrosDetalle_label,str(datos['numero_registros']))
        ventaCabecera.setAttribute(numeroDispensario_label,dispensario)
        ventaCabecera.setAttribute(identificadorManguera_label,manguera)
        ventaCabecera.setAttribute(claveProductoPEMEX_label,clave_producto)
        ventaCabecera.setAttribute(sumatoriaVolumenDespachado_label,str(datos['sumatoria_volumen']))
        ventaCabecera.setAttribute(sumatoriaVentas_label,str(datos['sumatoria_ventas']))
        ventasElem.appendChild(ventaCabecera)
    for venta in ventas_data:
        ventaDetalle = doc.createElement('{0}:{1}'.format(title,VTADetalle_label))
        ventaDetalle.setAttribute("tipoDeRegistro","D")
        ventaDetalle.setAttribute("numeroUnicoTransaccionVenta",str(venta['numeroUnicoTransaccionVenta']))
        ventaDetalle.setAttribute("numeroDispensario",str(venta['numeroDispensario']))
        ventaDetalle.setAttribute("identificadorManguera",str(venta['identificadorManguera']))
        ventaDetalle.setAttribute("claveProductoPEMEX",str(venta['claveProductoPEMEX']))
        ventaDetalle.setAttribute("volumenDespachado",str(venta['volumenDespachado']))
        ventaDetalle.setAttribute("precioUnitarioProducto",str(venta['precioUnitarioProducto']))
        ventaDetalle.setAttribute("importeTotalTransaccion",str(venta['importeTotalTransaccion']))
        ventaDetalle.setAttribute("fechaYHoraTransaccionVenta","2017-01-02T07:00:00")
        ventasElem.appendChild(ventaDetalle)
    root.appendChild(ventasElem)
    return doc.toprettyxml(encoding="utf-8")
    
def sort_key(key):
    dispensario, _, _ = key.split('_')
    return int(dispensario)

def sort_key_manguera(key):
    _, manguera, _ = key.split('_')
    return int(manguera)

def CabeceraVentas(data):
    # Creamos un diccionario para almacenar la información agrupada por manguera
    agrupado_por_manguera = {}
    # Recorremos los registros y los agrupamos por manguera
    for registro in data:
        manguera = registro['identificadorManguera']
        dispensario = registro['numeroDispensario']
        clave_producto = registro['claveProductoPEMEX']
        # Creamos una clave única para cada manguera, dispensario y clave de producto
        clave_unica = f"{dispensario}_{manguera}_{clave_producto}"
        
        if clave_unica not in agrupado_por_manguera:
            agrupado_por_manguera[clave_unica] = {
                'numero_registros': 0,
                'sumatoria_volumen': 0.0,
                'sumatoria_ventas': 0.0
            }
        agrupado_por_manguera[clave_unica]['numero_registros'] += 1
        agrupado_por_manguera[clave_unica]['sumatoria_volumen'] += registro['volumenDespachado']
        agrupado_por_manguera[clave_unica]['sumatoria_ventas'] += registro['importeTotalTransaccion']
    
    # Ordenar el diccionario por dispensario y luego por manguera
    agrupado_por_manguera_ordenado = OrderedDict(sorted(agrupado_por_manguera.items(), key=lambda x: (int(x[0].split('_')[0]), sort_key_manguera(x[0]))))
    return agrupado_por_manguera_ordenado
    
