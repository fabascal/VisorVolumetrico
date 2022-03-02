# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present NovaRet
"""

from asyncore import write
from csv import writer
import os
from ast import arg
from calendar import month
from sqlalchemy.sql.expression import extract
from sqlalchemy.sql.functions import session_user
from sqlalchemy import and_, func, cast, Date, extract
from website import db, scheduler, utils
import website
from website.home import blueprint
from flask import render_template, request, jsonify, redirect, url_for, current_app, session, send_file, send_from_directory
from flask_login import login_required, current_user
from .models import Reporte, Reporte_Linea_Compra
import datetime
from datetime import date, datetime
from decimal import Decimal


from website.authentication.models import Usuario
from website.settings.models import Producto, Estacion, Empresa
from website.home.models import Reporte_Linea_Compra as Compra, Reporte_Linea_Venta as Venta, Reporte

import pysftp
from xml.dom import minidom
import xml.etree.ElementTree as ET
import pandas as pd
from io import BytesIO


@blueprint.route('/index')
@login_required
def index():
    usuario = Usuario.query.filter_by(id=current_user.id).first()
    estaciones = db.session.query(Estacion).count()
    #dia_uno = datetime.datetime(date.today().year,date.today().month,1)
    dia_uno = datetime(2021,10,1)
    print (dia_uno)
    reportes = Reporte.query.filter(extract('month',Reporte.fecha) >= dia_uno.month).all()
    compra = venta_lts = venta_pesos = 0
    for reporte in reportes:
        for c in reporte.compra:
            compra += c.volumenRecepcion
        for v in reporte.venta:
            venta_lts += v.sumatoriaVolumenDespachado
            venta_pesos += v.sumatoriaVentas
    data = {"usuario":usuario,"estaciones":estaciones,"compra":"{:,.4f}".format(compra),"venta_lts":"{:,.4f}".format(venta_lts),"venta_pesos":"${:,.2f}".format(venta_pesos)}
    return render_template('home/index.html', segment='index', data=data)

@blueprint.route('/reportes/<fecha_api>', methods=['POST','GET'])
@blueprint.route('/reportes', defaults={'fecha_api':date.today()})
@login_required
def reportes(fecha_api):
    if request.method == 'POST':
        reportes = Reporte.query.filter_by(fecha = str(fecha_api)).all()
        response = {'message': f'Reportes filtrados con exito.'}
        return jsonify(response)
    reportes=Reporte.query.filter_by(fecha = str(fecha_api)).all()
    return render_template('home/reportes.html', segment='reportes_dia', reportes=reportes)

@blueprint.route('/reporte/<id_reporte>', methods=['POST','GET'])
@login_required
def reporte_detail(id_reporte):
    print(id_reporte)
    reporte = Reporte.query.filter_by(id=id_reporte).first()
    return render_template('home/reporte-detail.html', segment='reportes_detalle', reporte=reporte)


@blueprint.route('reporte/excel/<id_reporte>', methods=['GET'])
@login_required
def download(id_reporte):
    reporte = Reporte.query.filter_by(id=id_reporte).first()
    #Si no hay archivo lo creamos y guardamos
    if not reporte.excel:
        get_file_sftp(reporte)
    #Buscamos el archivo para descargarlo
    name_file = reporte.estacion.nombre +"|"+ str(reporte.fecha) +".xlsx"
    return send_from_directory(os.path.join('.','filestore/'+reporte.estacion.nombre),name_file)
    
def get_file_sftp(reporte):
    print(f'la estacion es {reporte.estacion.id_empresa}')
    empresa = Empresa.query.filter_by(id=reporte.estacion.id_empresa).first()
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(host=empresa.ftp_host,port=int(empresa.ftp_port), username=empresa.ftp_username, password=empresa.ftp_password, cnopts=cnopts) as server:
        print (f'Conexion con SFTP establecida correctamente para {empresa.nombre}...')
        server.chdir(reporte.estacion.ruta)
        name = reporte.estacion.numeroPermisoCRE.replace("/","_") + str(reporte.fecha.year) + str("{:02d}".format(reporte.fecha.month)) + str("{:02d}".format(reporte.fecha.day))
        for file in server.listdir_attr():
            if name in file.filename and ".zip" not in file.filename:
                with server.open(file.filename) as xml:
                    doc = minidom.parse(xml)
                    ControlesVolumetricos = []
                    for d in doc.getElementsByTagName("controlesvolumetricos:ControlesVolumetricos"):
                        titulo = {}
                        for attribute, value in d.attributes.items():
                            titulo.update({attribute:value})
                    for d in doc.getElementsByTagName("controlesvolumetricos:EXI"):
                        exi = {}
                        for attribute, value in d.attributes.items():
                            exi.update({attribute:value})
                        ControlesVolumetricos.append(utils.merge_two_dicts(titulo,exi))
                    for d in doc.getElementsByTagName("controlesvolumetricos:REC"):
                        rec = {}
                        for attribute, value in d.attributes.items():
                            rec.update({attribute:value})
                        ControlesVolumetricos.append(utils.merge_two_dicts(titulo,rec))
                    for d in doc.getElementsByTagName("controlesvolumetricos:VTA"):
                        vta = {}
                        for attribute, value in d.attributes.items():
                            vta.update({attribute:value})
                        ControlesVolumetricos.append(utils.merge_two_dicts(titulo,vta))
                    for d in  doc.getElementsByTagName("controlesvolumetricos:VTACabecera"):
                        cabecera = {}
                        for attribute, value in d.attributes.items():
                            cabecera.update({attribute:value})
                        ControlesVolumetricos.append(utils.merge_two_dicts(titulo,cabecera))
                    for d in doc.getElementsByTagName("controlesvolumetricos:VTADetalle"):
                        detalle = {}
                        for attribute,value in d.attributes.items():
                            detalle.update({attribute: value})
                        ControlesVolumetricos.append(utils.merge_two_dicts(titulo,detalle))
                    for d in doc.getElementsByTagName("controlesvolumetricos:TQS"):
                        tqs = {}
                        for attribute, value in d.attributes.items():
                            tqs.update({attribute:value})
                        ControlesVolumetricos.append(utils.merge_two_dicts(titulo, tqs))
                    for d in doc.getElementsByTagName("controlesvolumetricos:DIS"):
                        dis = {}
                        for attribute, value in d.attributes.items():
                            dis.update({attribute:value})
                        ControlesVolumetricos.append(utils.merge_two_dicts(titulo,dis))
                    df = pd.DataFrame(ControlesVolumetricos)
                    df.drop_duplicates(keep='first', inplace=True)
                    df.reset_index(drop=True, inplace=True)
                    #output = BytesIO()
                    path_file = 'website/filestore/'+reporte.estacion.nombre+'/'
                    if not os.path.exists(path_file):
                        os.makedirs(path_file)
                    name_file = reporte.estacion.nombre +"|"+ str(reporte.fecha) +".xlsx"
                    writer = pd.ExcelWriter(path_file+name_file, engine='xlsxwriter')
                    df.to_excel(writer, sheet_name="Hoja 1")
                    writer.save()
                    args={
                        "excel":path_file+name_file,
                        "escrito_por" : current_user.id
                    }
                    Reporte.query.filter_by(id=reporte.id).update(args)
                    db.session.commit()
                    


#Ejemplo que se ejecuta a la 1:30 am
@scheduler.task("cron", id="do_listar", day="*", hour="1", minute="30")
def job1():
    print('Job 1 executed')

@scheduler.task("cron", id="do_listar", hour="9")
def run_listar():
    print("Incia SFTP")
    sftp_connection_new()

def sftp_connection_new():
    with scheduler.app.app_context():
        fecha = date(2021, 10, 15)
        print(fecha)
        for empresa in Empresa.query.filter_by(ftp_on = True).all():
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            with pysftp.Connection(host=empresa.ftp_host,port=int(empresa.ftp_port), username=empresa.ftp_username, password=empresa.ftp_password, cnopts=cnopts) as server:
                print (f'Conexion con SFTP establecida correctamente para {empresa.nombre}...')
                for estacion in Estacion.query.filter_by(activo=True, id_empresa=empresa.id).all():
                    reporte_validar = Reporte.query.filter_by(id_estacion=estacion.id,fecha=str(fecha)).first()
                    if reporte_validar:
                        print("ya se proceso")
                        continue
                    flag_file = False
                    server.chdir(estacion.ruta)
                    name = estacion.numeroPermisoCRE.replace("/","_") + str(fecha.year) + str("{:02d}".format(fecha.month)) + str("{:02d}".format(fecha.day))
                    for file in server.listdir_attr():
                        if name in file.filename and ".zip" not in file.filename:
                            flag_file = True
                            reporte = Reporte(
                                id_estacion = estacion.id,
                                fecha = fecha,
                                estado = 'Creado',
                                creado_por = 1
                            )
                            db.session.add(reporte)
                            db.session.commit()
                            with server.open(file.filename) as xml:
                                doc = minidom.parse(xml)
                                for d in doc.getElementsByTagName("controlesvolumetricos:ControlesVolumetricos"):
                                    version = d.getAttribute("version")
                                    rfc = d.getAttribute("rfc")
                                    rfcProveedorSw = d.getAttribute("rfcProveedorSw")
                                    numeroPermisoCRE = d.getAttribute("numeroPermisoCRE")
                                #Realizamos validación del archivo para corroborar que corresponda con la información de la estación.
                                if empresa.version.nombre == version and empresa.rfc == rfc and empresa.rfcProveedorSW == rfcProveedorSw and estacion.numeroPermisoCRE == numeroPermisoCRE:
                                    print("es correcto")
                                    num_manguera,num_dispensario = 0,0
                                    #realizamos proceso de tanques (Compras)
                                    for tanque in doc.getElementsByTagName("controlesvolumetricos:EXI"):
                                        producto = Producto.query.filter_by(
                                            claveProducto=tanque.getAttribute("claveProducto"),
                                            claveSubProducto=tanque.getAttribute("claveSubProducto")
                                            ).first()
                                        compra = Compra(
                                            id_reporte = reporte.id,
                                            id_producto = producto.id,
                                            numeroTanque = tanque.getAttribute("numeroTanque"),
                                            volumenUtil = tanque.getAttribute("volumenUtil"),
                                            volumenFondaje = tanque.getAttribute("volumenFondaje"),
                                            volumenAgua = tanque.getAttribute("volumenAgua"),
                                            volumenDisponible = tanque.getAttribute("volumenDisponible"),
                                            volumenExtraccion = tanque.getAttribute("volumenExtraccion"),
                                            volumenRecepcion = tanque.getAttribute("volumenRecepcion"),
                                            temperatura = tanque.getAttribute("temperatura"),
                                            creado_por = 1
                                        )
                                        print("Tanque registrado")
                                        #Comentamos para no agregar mas datos
                                        db.session.add(compra)
                                        db.session.commit()
                                    for cabecera in doc.getElementsByTagName("controlesvolumetricos:VTACabecera"):
                                        producto = Producto.query.filter_by(
                                            claveProducto=cabecera.getAttribute("claveProducto"),
                                            claveSubProducto=cabecera.getAttribute("claveSubProducto")
                                            ).first()
                                        venta = Venta(
                                            id_reporte = reporte.id,
                                            id_producto = producto.id,
                                            numeroTotalRegistrosDetalle = cabecera.getAttribute("numeroTotalRegistrosDetalle"),
                                            numeroDispensario = cabecera.getAttribute("numeroDispensario"),
                                            identificadorManguera = cabecera.getAttribute("identificadorManguera"),
                                            sumatoriaVolumenDespachado = cabecera.getAttribute("sumatoriaVolumenDespachado"),
                                            sumatoriaVentas = cabecera.getAttribute("sumatoriaVentas"),
                                            creado_por = 1
                                        )
                                        #Comentamos para no agregar mas datos
                                        db.session.add(venta)
                                        db.session.commit()
                                        print("Cabecera registrada")
                                    for tqs in doc.getElementsByTagName("controlesvolumetricos:TQS"):
                                        args_tqs = { 
                                            "capacidadTotalTanque" : tqs.getAttribute("capacidadTotalTanque"),
                                            "capacidadOperativaTanque" : tqs.getAttribute("capacidadOperativaTanque"),
                                            "capacidadUtilTanque" : tqs.getAttribute("capacidadUtilTanque"),
                                            "capacidadFondajeTanque" : tqs.getAttribute("capacidadFondajeTanque"),
                                            "volumenMinimoOperacion" : tqs.getAttribute("volumenMinimoOperacion"),
                                            "estadoTanque" : tqs.getAttribute("estadoTanque")
                                        }
                                        Reporte_Linea_Compra.query.filter_by(id_reporte=reporte.id, numeroTanque= tqs.getAttribute("numeroTanque")).update(args_tqs)
                                        db.session.commit()

                                    for dispensario in doc.getElementsByTagName("controlesvolumetricos:DIS"):
                                        if num_dispensario < int(dispensario.getAttribute("numeroDispensario")):
                                            num_dispensario = int(dispensario.getAttribute("numeroDispensario"))
                                        num_manguera += 1
                                    args={
                                        "mangueras":num_manguera,
                                        "dispensarios":num_dispensario,
                                        "estado":"Terminado",
                                        "escrito_por" : 1
                                    }
                                    Reporte.query.filter_by(id=reporte.id).update(args)
                                    db.session.commit()
                                else:
                                    print("No Coincide archivo.")
                    if flag_file == False:
                        print("no hay archivo")
                        args = Reporte(
                            id_estacion = estacion.id,
                            fecha = fecha,
                            estado = 'Sin archivo',
                            creado_por = 1
                        )
                        db.session.add(args)
                        db.session.commit()
            

    
