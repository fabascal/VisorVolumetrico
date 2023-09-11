# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present NovaRet
"""


from email.policy import default
from math import prod
import os
from ast import arg
from sre_constants import SUCCESS

from sqlalchemy import and_, func, cast, Date, extract
from website import db, scheduler, utils
import website
from website.home import blueprint
from flask import Response,render_template,render_template_string, request, jsonify, redirect, url_for, current_app, session, send_file, send_from_directory, make_response,flash
from flask_login import login_required, current_user
import datetime
from datetime import date, datetime
from decimal import Decimal
from website.authentication.models import Usuario
from website.settings.models import Producto, Estacion, Empresa, Tanques, Version, estaciones_productos
from website.home.models import Reporte_Linea_Compra as Compra, Reporte_Linea_Venta as Venta, Reporte, Reporte_Linea_Venta
from website.home.forms import GeneratorXmlForm, GenXmlTanquesCampos, GenXmlRecepcionesCampos, GenXmlVentas

import pysftp
from xml.dom import minidom
import xml.etree.ElementTree as ET
import pandas as pd

import pdfkit

from website.home.create_xml import create_xml_11, create_xml_12, create_xml_13


COLOR_DANGER = 'rgb( 241, 148, 138 )'
COLOR_WARNING = 'rgb( 249, 231, 159 )'
COLOR_SUCCESS = 'rgb( 174, 214, 241 )'
COLOR_TEXT = 'rgb( 255, 255, 255 )'
FORMAT_DATE = "%Y-%m-%d"

@blueprint.route('/obtener_tanques', methods=['POST'])
@login_required
def obtener_tanques():
    form = GeneratorXmlForm(request.form)
    estacion_id = request.form.get('estacion_id')
    tanques = Tanques.query.filter_by(id_estacion=estacion_id).order_by(Tanques.no_tanque).all()
    #Obtener productos
    producto_ids = db.session.query(estaciones_productos.c.producto_id).filter(estaciones_productos.c.estacion_id == estacion_id).all()
    # Convertir la lista de tuplas a una lista de IDs
    producto_ids = [item[0] for item in producto_ids]
    # 2. Consulta la tabla productos
    productos_obj = db.session.query(Producto).filter(Producto.id.in_(producto_ids)).all()
    form.tanques.entries.clear()
    for tanque in tanques:
        #Tanques
        tanque_form = GenXmlTanquesCampos()
        tanque_form.no_tanque = tanque.no_tanque
        tanque_form.producto = tanque.producto.nombre
        tanque_form.volumenDisponible = tanque.volumenDisponible
        tanque_form.volumenExtraccion = tanque.volumenExtraccion
        tanque_form.volumenRecepcion = tanque.volumenRecepcion 
        tanque_form.claveProducto = tanque.producto.claveProducto
        tanque_form.claveProductoPEMEX = tanque.producto.claveProductoPEMEX
        tanque_form.claveSubProducto = tanque.producto.claveSubProducto
        tanque_form.composicionOctanajeDeGasolina = tanque.producto.composicionOctanajeDeGasolina
        tanque_form.gasolinaConEtanol = tanque.producto.gasolinaConEtanol
        tanque_form.volumenUtil = tanque.volumenUtil
        tanque_form.volumenFondaje = tanque.volumenFondaje
        tanque_form.volumenAgua = 0 #tanque.volumenAgua
        tanque_form.temperatura = 21 #tanque.temperatura
        form.tanques.append_entry(tanque_form)
        #Recepcion
        recepcion_form = GenXmlRecepcionesCampos()
        recepcion_form.recepcion = False
        recepcion_form.no_tanque_recepcion = tanque.no_tanque
        recepcion_form.producto = tanque.producto.nombre
        recepcion_form.claveProducto = tanque.producto.claveProducto
        recepcion_form.claveSubProducto = tanque.producto.claveSubProducto
        recepcion_form.composicionOctanajeDeGasolina = tanque.producto.composicionOctanajeDeGasolina
        recepcion_form.gasolinaConEtanol = tanque.producto.gasolinaConEtanol
        recepcion_form.folioUnicoRecepcionCabecera = ""
        recepcion_form.folioUnicoRecepcion = ""
        recepcion_form.volumenInicialTanque = 0
        recepcion_form.volumenFinalTanque = 0
        recepcion_form.volumenRecepcion = 0
        recepcion_form.temperatura = 21
        recepcion_form.fechaYHoraRecepcion = datetime.now()
        recepcion_form.folioUnicoRelacion = ""
        form.recepciones.append_entry(recepcion_form)
    for producto in productos_obj:
        ventas_form = GenXmlVentas()
        ventas_form.id_producto = producto.id
        ventas_form.producto = producto.nombre
        ventas_form.claveProductoPEMEX = producto.claveProductoPEMEX
        ventas_form.litros = 0.00
        ventas_form.precio = 0.00
        form.ventas.append_entry(ventas_form)
    #rendered_template = render_template('home/genera-xml.html', segment='procesamiento_generaxml', tanques=tanques)
    tanques_html = render_template_string('''
                        <!-- Inicia la card -->                   
                              {% for nested in form.tanques %}
                              <div class="col-12 col-sm-6 col-md-4 d-flex align-items-stretch flex-column">
                                <div class="card bg-light d-flex flex-fill">
                                  <div class="card-header text-muted border-bottom-0 text-center">
                                    TANQUE - {{ nested.no_tanque.data }}
                                  </div>
                                  <div style="display: none;"> {{nested.no_tanque }}</div>
                                  <div class="card-body pt-0">
                                    <div class="row">
                                      <div class="col-12">
                                        <h2 class="lead">
                                          <b class="small">{{ nested.producto.data}}</b>
                                        </h2>
                                        <hr>
                                        <ul class="ml-0 mb-0 fa-ul text-muted">
                                          <li class="small mb-2 "> 
                                            <b>{{ nested.volumenDisponible.label(style="display:inline") }}: </b> 
                                            {{ nested.volumenDisponible (class="form-control") }} 
                                          </li>
                                          <li class="small mb-2 "> 
                                            <b>{{ nested.volumenExtraccion.label(style="display:inline") }}: </b> 
                                            {{ nested.volumenExtraccion (class="form-control")}} 
                                          </li>
                                          <li class="small mb-2 "> 
                                            <b>{{ nested.volumenRecepcion.label(style="display:inline") }}: </b> 
                                            {{ nested.volumenRecepcion (class="form-control")}} 
                                          </li>
                                          <li class="small mb-2 " style="display: none;"> 
                                            <b>{{ nested.claveProducto.label(style="display:inline") }}: </b> 
                                            {{ nested.claveProducto }} 
                                          </li>
                                          <li class="small mb-2 " style="display: none;"> 
                                            <b>{{ nested.claveSubProducto.label(style="display:inline") }}: </b> 
                                            {{ nested.claveSubProducto }} 
                                          </li>
                                          <li class="small mb-2 " style="display: none;"> 
                                            <b>{{ nested.claveProductoPEMEX.label(style="display:inline") }}: </b> 
                                            {{ nested.claveProductoPEMEX }} 
                                          </li>
                                          <li class="small mb-2 " style="display: none;"> 
                                            <b>{{ nested.composicionOctanajeDeGasolina.label(style="display:inline") }}: </b> 
                                            {{ nested.composicionOctanajeDeGasolina }} 
                                          </li>
                                          <li class="small mb-2 " style="display: none;"> 
                                            <b>{{ nested.gasolinaConEtanol.label(style="display:inline") }}: </b> 
                                            {{ nested.gasolinaConEtanol }} 
                                          </li>
                                          <li class="small mb-2 " style="display: none;"> 
                                            <b>{{ nested.volumenUtil.label(style="display:inline") }}: </b> 
                                            {{ nested.volumenUtil }} 
                                          </li>
                                          <li class="small mb-2 " style="display: none;"> 
                                            <b>{{ nested.volumenFondaje.label(style="display:inline") }}: </b> 
                                            {{ nested.volumenFondaje }} 
                                          </li>
                                          <li class="small mb-2 " style="display: none;"> 
                                            <b>{{ nested.volumenAgua.label(style="display:inline") }}: </b> 
                                            {{ nested.volumenAgua }} 
                                          </li>
                                          <li class="small mb-2 " style="display: none;"> 
                                            <b>{{ nested.temperatura.label(style="display:inline") }}: </b> 
                                            {{ nested.temperatura }} 
                                          </li>
                                        </ul>
                                      </div>
                                    </div>
                                  </div>
                                  <div class="card-footer">
                                    <div class="text-right">
                                    </div>
                                  </div>
                                </div>
                              </div>
                              {% endfor %}
                        <!-- Fin de la card -->
                                          ''', form=form)
    recepcion_html = render_template_string("""
                            <!-- Inicia la card -->                   
                              {% for nested_recepciones in form.recepciones %}
                              <div class="col-12 col-sm-6 col-md-4 d-flex align-items-stretch flex-column">
                                <div class="card bg-light d-flex flex-fill">
                                  <div class="card-header text-muted border-bottom-0 text-center">
                                    TANQUE - {{ nested_recepciones.no_tanque_recepcion.data }}
                                  </div>
                                  <div class="card-body pt-0">
                                    <div class="row">
                                      <div class="col-12">
                                        <h2 class="lead">
                                          <b class="small">{{ nested_recepciones.producto.data}}</b>
                                        </h2>
                                        <hr>
                                        <ul class="ml-0 mb-0 fa-ul text-muted">
                                          <li class="custom-control custom-checkbox small mb-2">
                                            {{ nested_recepciones.recepcion(class_="custom-control-input",type="checkbox", onclick="toggleElements(this)") }}
                                            {{ nested_recepciones.recepcion.label (class="custom-control-label")}}
                                          </li>
                                          <li class="small mb-2 "> 
                                            <b>{{ nested_recepciones.folioUnicoRecepcionCabecera.label(style="display:inline") }}: </b> 
                                            {{ nested_recepciones.folioUnicoRecepcionCabecera (class="form-control", onchange="folioUnicoRecepcion(this)") }} 
                                          </li>
                                          <li class="small mb-2 " style="display: none;"> 
                                            <b>{{ nested_recepciones.folioUnicoRecepcion.label(style="display:inline") }}: </b> 
                                            {{ nested_recepciones.folioUnicoRecepcion (class="form-control")}} 
                                          </li>
                                          <li class="small mb-2" style="display: none;"> 
                                            <b>{{ nested_recepciones.folioUnicoRelacion.label(style="display:inline") }}: </b> 
                                            {{ nested_recepciones.folioUnicoRelacion (class="form-control")}} 
                                          </li>
                                          <li class="small mb-2 "> 
                                            <b>{{ nested_recepciones.volumenInicialTanque.label(style="display:inline") }}: </b> 
                                            {{ nested_recepciones.volumenInicialTanque (class="form-control", onchange="volumenFinal(this)")}} 
                                          </li>
                                          <li class="small mb-2 "> 
                                            <b>{{ nested_recepciones.volumenRecepcion.label(style="display:inline") }}: </b> 
                                            {{ nested_recepciones.volumenRecepcion (class="form-control", onchange="volumenFinal(this)")}} 
                                          </li>
                                          <li class="small mb-2 "> 
                                            <b>{{ nested_recepciones.volumenFinalTanque.label(style="display:inline") }}: </b> 
                                            {{ nested_recepciones.volumenFinalTanque (class="form-control")}} 
                                          </li>
                                        </ul>
                                      </div>
                                    </div>
                                  </div>
                                  <div class="card-footer">
                                    <div class="text-right">
                                    </div>
                                  </div>
                                </div>
                              </div>
                              {% endfor %}
                                            """,form=form)
    ventas_html = render_template_string("""
                <!-- Inicia la card -->                   
                              {% for nested_venta in form.ventas %}
                              <div class="col-12 col-sm-6 col-md-4 d-flex align-items-stretch flex-column">
                                <div class="card bg-light d-flex flex-fill">
                                  <div class="card-header text-muted border-bottom-0 text-center">
                                    VENTA
                                  </div>
                                  <div class="card-body pt-0">
                                    <div class="row">
                                      <div class="col-12">
                                        <h2 class="lead">
                                          <b class="small">{{ nested_venta.producto.data}}</b>
                                        </h2>
                                        <hr>
                                        <ul class="ml-0 mb-0 fa-ul text-muted">
                                          <li class="small mb-2" style="display: none;"> 
                                            <b>{{ nested_venta.id_producto.label(style="display:inline") }}: </b> 
                                            {{ nested_venta.id_producto (class="form-control")}} 
                                          </li>
                                          <li class="small mb-2" style="display: none;"> 
                                            <b>{{ nested_venta.producto.label(style="display:inline") }}: </b> 
                                            {{ nested_venta.producto (class="form-control")}} 
                                          </li>
                                          <li class="small mb-2" style="display: none;"> 
                                            <b>{{ nested_venta.claveProductoPEMEX.label(style="display:inline") }}: </b> 
                                            {{ nested_venta.claveProductoPEMEX (class="form-control")}} 
                                          </li>
                                          <li class="small mb-2"> 
                                            <b>{{ nested_venta.litros.label(style="display:inline") }}: </b> 
                                            {{ nested_venta.litros (class="form-control", onchange="folioUnicoRecepcion(this)") }} 
                                          </li>
                                          <li class="small mb-2"> 
                                            <b>{{ nested_venta.precio.label(style="display:inline") }}: </b> 
                                            {{ nested_venta.precio (class="form-control")}} 
                                          </li>
                                        </ul>
                                      </div>
                                    </div>
                                  </div>
                                  <div class="card-footer">
                                    <div class="text-right">
                                    </div>
                                  </div>
                                </div>
                              </div>
                              {% endfor %}
    """, form=form)
    return jsonify(rendered_tanques = tanques_html, rendered_recepciones = recepcion_html, rendered_ventas = ventas_html)

@blueprint.route('/generar', methods=['POST', 'GET'])
@login_required
def genera_xml():
    form = GeneratorXmlForm(request.form)
    form.id_estacion.choices = [(e.id, e.nombre) for e in Estacion.query.order_by('nombre').all()]
    # Obtén solo los registros de la tabla Version que tengan el campo "activo" con valor True
    versions = Version.query.filter(Version.activo.is_(True)).order_by(Version.id).all()
    # Crea la lista de opciones para el campo "id_version" del formulario
    form.id_version.choices = [(v.id, v.nombre) for v in versions]
    estacion_uno = Estacion.query.order_by('nombre').first()
    tanques = Tanques.query.filter_by(id_estacion=estacion_uno.id).order_by(Tanques.no_tanque).all()
    #Obtener productos
    producto_ids = db.session.query(estaciones_productos.c.producto_id).filter(estaciones_productos.c.estacion_id == estacion_uno.id).all()
    # Convertir la lista de tuplas a una lista de IDs
    producto_ids = [item[0] for item in producto_ids]
    # 2. Consulta la tabla productos
    productos_obj = db.session.query(Producto).filter(Producto.id.in_(producto_ids)).all()
    # Llenar los tanques en el formulario
    form.tanques.entries.clear()
    form.ventas.entries.clear()
    for tanque in tanques:
        #Tanques
        tanque_form = GenXmlTanquesCampos()
        tanque_form.no_tanque = tanque.no_tanque
        tanque_form.producto = tanque.producto.nombre
        tanque_form.volumenDisponible = tanque.volumenDisponible
        tanque_form.volumenExtraccion = tanque.volumenExtraccion
        tanque_form.volumenRecepcion = tanque.volumenRecepcion 
        tanque_form.claveProducto = tanque.producto.claveProducto
        tanque_form.claveProductoPEMEX = tanque.producto.claveProductoPEMEX
        tanque_form.claveSubProducto = tanque.producto.claveSubProducto
        tanque_form.composicionOctanajeDeGasolina = tanque.producto.composicionOctanajeDeGasolina
        tanque_form.gasolinaConEtanol = tanque.producto.gasolinaConEtanol
        tanque_form.volumenUtil = tanque.volumenUtil
        tanque_form.volumenFondaje = tanque.volumenFondaje
        tanque_form.volumenAgua = 0 #tanque.volumenAgua
        tanque_form.temperatura = 21 #tanque.temperatura
        form.tanques.append_entry(tanque_form)
        #Recepcion
        recepcion_form = GenXmlRecepcionesCampos()
        recepcion_form.recepcion = False
        recepcion_form.no_tanque_recepcion = tanque.no_tanque
        recepcion_form.producto = tanque.producto.nombre
        recepcion_form.claveProducto = tanque.producto.claveProducto
        recepcion_form.claveSubProducto = tanque.producto.claveSubProducto
        recepcion_form.composicionOctanajeDeGasolina = tanque.producto.composicionOctanajeDeGasolina
        recepcion_form.gasolinaConEtanol = tanque.producto.gasolinaConEtanol
        recepcion_form.folioUnicoRecepcionCabecera = ""
        recepcion_form.folioUnicoRecepcion = ""
        recepcion_form.volumenInicialTanque = 0
        recepcion_form.volumenFinalTanque = 0
        recepcion_form.volumenRecepcion = 0
        recepcion_form.temperatura = 21
        recepcion_form.fechaYHoraRecepcion = datetime.now()
        recepcion_form.folioUnicoRelacion = ""
        form.recepciones.append_entry(recepcion_form)
    for producto in productos_obj:
        ventas_form = GenXmlVentas()
        ventas_form.id_producto = producto.id
        ventas_form.producto = producto.nombre
        ventas_form.claveProductoPEMEX = producto.claveProductoPEMEX
        ventas_form.litros = 0.00
        ventas_form.precio = 0.00
        form.ventas.append_entry(ventas_form)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            data={}
            data['tanques'] = {}
            data['recepciones'] = {}
            data['ventas'] = {}
            filtered_recepciones = {}  # Diccionario para almacenar solo la recepción filtrada
            for key, value in request.form.items():
                if key.startswith('tanques-'):
                    index = key.split('-')[1]  # Obtener el índice del tanque
                    field_name = key.split('-')[2]  # Obtener el nombre del campo del tanque
                    if index not in data['tanques']:
                        data['tanques'][index] = {}
                    data['tanques'][index][field_name] = value
                elif key.startswith('recepciones-'):
                    index = key.split('-')[1]  # Obtener el índice de la recepcion
                    field_name = key.split('-')[2]  # Obtener el nombre del campo de la recepcion

                    # Si el campo 'recepcion' tiene un valor 'y', entonces agregamos esta recepción al diccionario filtered_recepciones
                    if field_name == 'recepcion' and value == 'y':
                        if index not in filtered_recepciones:
                            filtered_recepciones[index] = {}
                        filtered_recepciones[index][field_name] = value
                    elif index in filtered_recepciones:  # Si ya se ha agregado esta recepción (porque tiene un valor 'y'), guardamos los otros campos también
                        filtered_recepciones[index][field_name] = value
                                
                elif key.startswith('ventas-'):
                    index = key.split('-')[1]  # Obtener el índice de las ventas
                    field_name = key.split('-')[2]  # Obtener el nombre del campo de las ventas
                    if index not in data['ventas']:
                        data['ventas'][index] = {}
                    data['ventas'][index][field_name] = value
                else:
                    data[key] = value

            data['recepciones'] = filtered_recepciones
            estacion = Estacion.query.filter_by(id=form.id_estacion.data[0]).first()
            fecha = form.fecha.data
            if data['id_version'] == "1":   
                archivo_xml = create_xml_11(estacion, data)
            elif data['id_version'] == "2":
                archivo_xml = create_xml_12(estacion, data)
            elif data['id_version'] == "3"  :
                archivo_xml = create_xml_13(estacion, data)
            else:    
                archivo_xml = create_xml_13(estacion, data)
            # Directorio y nombre del archivo
            path_file = 'website/filestore/xml/'+estacion.nombre+'/'
            path_file_2 = 'filestore/xml/'+estacion.nombre+'/'
            if not os.path.exists(path_file):
                os.makedirs(path_file)
            name_file = estacion.numeroPermisoCRE.replace('/', '_') +"|"+ str(fecha) +".xml"
            # Guardar el contenido en el archivo
            file_path = os.path.join(path_file, name_file)
            with open(file_path, 'wb') as file:
                file.write(archivo_xml)
            return send_from_directory(path_file_2, name_file, as_attachment=True)
        except ValueError as e:
            print(e)
            flash('Error al agregar objeto: ' + str(e), 'error')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error en el campo {getattr(form, field).label.text}: {error}")
    
    return render_template('home/genera-xml.html', segment='procesamiento_generaxml', form=form)


@blueprint.route('/index')
@login_required
def index():
    usuario = Usuario.query.filter_by(id=current_user.id).first()
    estaciones = db.session.query(Estacion).count()
    dia_uno = date(date.today().year,date.today().month,1)
    reportes = Reporte.query.filter(Reporte.fecha >= dia_uno).all()
    
    reportes_data = db.session.query(Reporte.fecha,db.func.sum(Reporte_Linea_Venta.sumatoriaVolumenDespachado)).join(Reporte_Linea_Venta, Reporte.id == Reporte_Linea_Venta.id_reporte).group_by(Reporte.fecha).all()
    
    #db.session.query(func.sum(Reporte.venta).label('Venta'),
    #                        extract('year', Reporte.fecha),
    #                        extract('month', Reporte.fecha)).\
    #                group_by(extract('year', Reporte.fecha),
    #                extract('month', Reporte.fecha)).\
    #                all()
    data = {"usuario":usuario}
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
    return render_template('home/reportes.html', segment='reportes_reportes_dia', reportes=reportes)

@blueprint.route('/reporte/<id_reporte>', methods=['POST','GET'])
@login_required
def reporte_detail(id_reporte):
    print(id_reporte)
    reporte = Reporte.query.filter_by(id=id_reporte).first()
    return render_template('home/reporte-detail.html', segment='procesamiento_reportes_detalle', reporte=reporte)

@blueprint.route('/calendario', methods=['POST','GET'])
@login_required
def calendario():
    return render_template('home/calendar.html', segment='procesamiento_calendario' )

@blueprint.route('/procesado_ruta', methods=['POST'])
@login_required
def calendar_detail_route():
    try:
        if request.method == 'POST':
            response = request.get_json()
            return jsonify({'redirect': url_for("home_blueprint.calendar_detail", date=response['date'])})
    except ReferenceError as e:
        return f"It is a {e} Provide proper referaece of file path"
    
@blueprint.route('/procesado/<date>', methods=['POST','GET'])
@login_required
def calendar_detail(date):
    reportes = Reporte.query.filter(Reporte.fecha == date).all()
    estaciones = db.session.query(Estacion).count()
    return render_template('home/calendar-detail.html', segment='procesamiento_calendario_detallado',date=date,reportes=reportes,estaciones=estaciones)

@blueprint.route('/deleteReport/<id_report>', methods=['GET'])
@login_required
def delete_report(id_report):
    if request.method == 'GET':
        Compra.query.filter_by(id_reporte=id_report).delete()
        Venta.query.filter_by(id_reporte=id_report).delete()
        Reporte.query.filter_by(id=id_report).delete()
        db.session.commit()
        message = {'greeting':'Reporte borrado'}
        return jsonify(message)
    
@blueprint.route('/redo_read_sftp', methods=['POST'])
@login_required
def redo_read_sftp():
    if request.method == 'POST':
        response = request.get_json()
        date = datetime.strptime(response['fecha'],FORMAT_DATE).date()
        reportes = Reporte.query.filter_by(fecha=date,estado='Terminado').all()
        empresas = Empresa.query.all()
        est_procesadas = []
        for reporte in reportes:
            est_procesadas.append(reporte.estacion.id)
        for empresa in empresas:
            estaciones = Estacion.query.filter(Estacion.id.notin_(est_procesadas),Estacion.id_empresa==empresa.id).all()
            if estaciones:
                read_file_sftp(empresa, estaciones,date)
        return jsonify({'redirect': url_for("home_blueprint.calendar_detail", date=date)})
    
@blueprint.route('/updateReport', methods=['POST'])
@login_required
def update_report():
    if request.method == 'POST':
        response = request.get_json()
        report = Reporte.query.filter_by(id=response['id_report']).first()
        update_data_from_sftp(report)
        return jsonify({'redirect': url_for("home_blueprint.calendar_detail", date=report.fecha)})

def get_background_color(terminadas, estaciones):
    percentage = 100 * float(terminadas) / float(estaciones)
    if  percentage < 90 :
        return COLOR_DANGER
    elif percentage >= 91 and percentage <= 99:
        return COLOR_WARNING
    else:
        return COLOR_SUCCESS

@blueprint.route('/get_calendar_data/<start>', methods=['POST','GET'])  
@blueprint.route('/get_calendar_data', defaults={'start':date.today()})
@login_required      
def get_calendar_data(start):
    if (isinstance(start, str)):
        start = datetime.strptime(start,FORMAT_DATE)
    dates = []
    event = []
    rep_term=0
    if start:
        reportes = Reporte.query.filter(extract('year', Reporte.fecha)==start.year).filter(extract('month', Reporte.fecha)==start.month).order_by(Reporte.fecha).all()
        estaciones = db.session.query(Estacion).count()
        for reporte in reportes:
            if reporte.fecha not in dates:
                dates.append(reporte.fecha)
                if reporte.estado == 'Terminado':
                    rep_term = 1
                event.append(
                    {
                        'rep_term' : rep_term,
                        'title' : f'{rep_term}/{estaciones} estaciones.',
                        'start' : str(datetime.strptime(str(reporte.fecha),FORMAT_DATE)),
                        'color' : get_background_color(rep_term,estaciones),
                        'end' : '',
                        'allDay': 'true',
                        'display': 'background'
                    }
                )
            #actualizar el listado cuando ya se registro la fecha
            else:
                for lno, line in enumerate(event):                
                    if str(datetime.strptime(str(reporte.fecha),FORMAT_DATE)) == str(line['start']):
                        if reporte.estado == 'Terminado':
                            rep_term = line['rep_term']+ 1
                        color = get_background_color(rep_term, estaciones)
                        event[lno] = {
                                    'rep_term' : rep_term,
                                    'title' : f'{rep_term}/{estaciones} estaciones.',
                                    'start' : str(datetime.strptime(str(reporte.fecha),FORMAT_DATE)),
                                    'color' : color,
                                    'end' : '',
                                    'allDay': 'true',
                                    'display': 'background'
                                    }
    return jsonify(event)
    
@blueprint.route('/reporte/tanques/<stations>/<start_date>/<end_date>', methods=['POST','GET'])
@login_required
def report_detail_tqs(start_date, end_date, stations):
    reports = Reporte.query.filter(start_date <= Reporte.fecha , Reporte.fecha <= end_date, Reporte.id_estacion.in_(tuple(stations))).all()
    fecha = datetime.today()
    css = os.path.join(current_app.root_path,'static/assets/custom/css/reporte-main.css')
    html = render_template('home/reports/detailed_report_tqs.html', reports=reports, fecha=fecha, start_date=start_date, end_date=end_date)
    pdf = pdfkit.from_string(html,css=css)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/x-pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=Reporte-tqs.pdf'
    return response

@blueprint.route('/reporte/dispensarios/<stations>/<start_date>/<end_date>', methods=['POST','GET'])
@login_required
def report_detail_disp(start_date, end_date, stations):
    reports = Reporte.query.filter(start_date <= Reporte.fecha , Reporte.fecha <= end_date, Reporte.id_estacion.in_(tuple(stations))).all()
    fecha = datetime.today()
    css = os.path.join(current_app.root_path,'static/assets/custom/css/reporte-main.css')
    html = render_template('home/reports/detailed_report_disp.html', reports=reports, fecha=fecha, start_date=start_date, end_date=end_date)
    pdf = pdfkit.from_string(html,False,css=css)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/x-pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=Reporte-disp.pdf'
    return response

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

def update_data_from_sftp(reporte):
    empresa = Empresa.query.filter_by(id=reporte.estacion.id_empresa).first()
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(host=empresa.ftp_host,port=int(empresa.ftp_port), username=empresa.ftp_username, password=empresa.ftp_password, cnopts=cnopts) as server:
        print (f'Conexion con SFTP establecida correctamente para {empresa.nombre}...')
        server.chdir(reporte.estacion.ruta)
        name = reporte.estacion.numeroPermisoCRE.replace("/","_") + str(reporte.fecha.year) + str("{:02d}".format(reporte.fecha.month)) + str("{:02d}".format(reporte.fecha.day))
        args={
            "estado":"Actualizando",
            "escrito_por" : current_user.id
        }
        Reporte.query.filter_by(id=reporte.id).update(args)
        for file in server.listdir_attr():
            if name in file.filename and ".zip" not in file.filename:
                with server.open(file.filename) as xml:
                    doc = minidom.parse(xml)
                    for d in doc.getElementsByTagName("controlesvolumetricos:ControlesVolumetricos"):
                        version = d.getAttribute("version")
                        rfc = d.getAttribute("rfc")
                        rfcProveedorSw = d.getAttribute("rfcProveedorSw")
                        numeroPermisoCRE = d.getAttribute("numeroPermisoCRE")
                    #Realizamos validación del archivo para corroborar que corresponda con la información de la estación.
                    if empresa.version.nombre == version and empresa.rfc == rfc and empresa.rfcProveedorSW == rfcProveedorSw and reporte.estacion.numeroPermisoCRE == numeroPermisoCRE:
                        print("es correcto")
                        num_manguera,num_dispensario = 0,0
                        #realizamos proceso de tanques (Compras)
                        for tqs in doc.getElementsByTagName("controlesvolumetricos:EXI"):
                            producto = Producto.query.filter_by(
                                claveProducto=tqs.getAttribute("claveProducto"),
                                claveSubProducto=tqs.getAttribute("claveSubProducto")
                                ).first()
                            args_tqs = { 
                                "id_producto" : producto.id,
                                "volumenUtil" : tqs.getAttribute("volumenUtil"),
                                "volumenFondaje" : tqs.getAttribute("volumenFondaje"),
                                "volumenAgua" : tqs.getAttribute("volumenAgua"),
                                "volumenDisponible" : tqs.getAttribute("volumenDisponible"),
                                "volumenExtraccion" : tqs.getAttribute("volumenExtraccion"),
                                "volumenRecepcion" : tqs.getAttribute("volumenRecepcion"),
                                "temperatura" : tqs.getAttribute("temperatura"),
                                "escrito_por" : current_user.id
                            }
                            Compra.query.filter_by(id_reporte=reporte.id, numeroTanque= tqs.getAttribute("numeroTanque")).update(args_tqs)
                            db.session.commit()
                            print("Tanque Actualizado")
                        for cabecera in doc.getElementsByTagName("controlesvolumetricos:VTACabecera"):
                            producto = Producto.query.filter_by(
                                claveProducto=cabecera.getAttribute("claveProducto"),
                                claveSubProducto=cabecera.getAttribute("claveSubProducto")
                                ).first()
                            vta_args = {
                                "id_producto" : producto.id,
                                "numeroTotalRegistrosDetalle" : cabecera.getAttribute("numeroTotalRegistrosDetalle"),
                                "sumatoriaVolumenDespachado" : cabecera.getAttribute("sumatoriaVolumenDespachado"),
                                "sumatoriaVentas" : cabecera.getAttribute("sumatoriaVentas"),
                                "escrito_por" : current_user.id
                            }
                            Venta.query.filter_by(id_reporte=reporte.id,numeroDispensario=cabecera.getAttribute("numeroDispensario"),identificadorManguera=cabecera.getAttribute("identificadorManguera")).update(vta_args)
                            db.session.commit()
                            print("Cabecera Actualizada")
                        for tqs in doc.getElementsByTagName("controlesvolumetricos:TQS"):
                            args_tqs = { 
                                "capacidadTotalTanque" : tqs.getAttribute("capacidadTotalTanque"),
                                "capacidadOperativaTanque" : tqs.getAttribute("capacidadOperativaTanque"),
                                "capacidadUtilTanque" : tqs.getAttribute("capacidadUtilTanque"),
                                "capacidadFondajeTanque" : tqs.getAttribute("capacidadFondajeTanque"),
                                "volumenMinimoOperacion" : tqs.getAttribute("volumenMinimoOperacion"),
                                "estadoTanque" : tqs.getAttribute("estadoTanque")
                            }
                            Compra.query.filter_by(id_reporte=reporte.id, numeroTanque= tqs.getAttribute("numeroTanque")).update(args_tqs)
                            db.session.commit()
                        for dispensario in doc.getElementsByTagName("controlesvolumetricos:DIS"):
                            if num_dispensario < int(dispensario.getAttribute("numeroDispensario")):
                                num_dispensario = int(dispensario.getAttribute("numeroDispensario"))
                            num_manguera += 1
                        args={
                            "mangueras":num_manguera,
                            "dispensarios":num_dispensario,
                            "estado":"Terminado",
                            "escrito_por" : current_user.id
                        }
                        Reporte.query.filter_by(id=reporte.id).update(args)
                        db.session.commit()

#Funcion para procesar archivos, es necesario enviar empresas de una estacion
@login_required
def read_file_sftp(empresa, estaciones, fecha):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(host=empresa.ftp_host,port=int(empresa.ftp_port), username=empresa.ftp_username, password=empresa.ftp_password, cnopts=cnopts) as server:
        for estacion in estaciones:
            server.chdir(estacion.ruta)
            name = estacion.numeroPermisoCRE.replace("/","_") + str(fecha.year) + str("{:02d}".format(fecha.month)) + str("{:02d}".format(fecha.day))
            for file in server.listdir_attr():
                if name in file.filename and ".zip" not in file.filename:
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
                                Compra.query.filter_by(id_reporte=reporte.id, numeroTanque= tqs.getAttribute("numeroTanque")).update(args_tqs)
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
                    titulo = {}
                    for d in doc.getElementsByTagName("controlesvolumetricos:ControlesVolumetricos"):
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

@scheduler.task("cron", id="do_listar", hour="2")
def run_listar():
    print("Incia SFTP")
    sftp_connection_new()

def sftp_connection_new():
    with scheduler.app.app_context():
        fecha = date(2022, 6, 18)
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
                                        Compra.query.filter_by(id_reporte=reporte.id, numeroTanque= tqs.getAttribute("numeroTanque")).update(args_tqs)
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
            