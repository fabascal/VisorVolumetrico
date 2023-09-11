# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present NovaRet
"""
from werkzeug.utils import secure_filename
import os
from website import db
from website.settings import blueprint
from flask import render_template, request, jsonify, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
import json
from website.authentication.utils import hash_pass
from website.authentication.models import Usuario, UserSchema, Grupo, GroupSchema
from website.settings.models import Empresa, EmpresaSchema, Version, EstacionSchema, Zona, Estacion, Tanques, Producto, Dispensario, Manguera, estaciones_productos
from website.settings.forms import TanquesForm, ProductosForm, DispensariosForm, MangueraForm, EstacionForm, EstacionTanquesForm
from website.home.utils.gen_pem import GenPem
from website.home.utils.cer_data import CerData
from xml.dom import minidom

@blueprint.route('/usuarios', methods=['GET','PUT'])
@login_required
def users():    
    return render_template('settings/users.html', segment='usersSettings_users')

@blueprint.route('/api_users', methods=['GET'])
@login_required
def api_users():
    usuarios = Usuario.query.filter_by(activo = True).order_by(Usuario.id.asc()).all()
    user_schema = UserSchema(many=True)
    return jsonify(user_schema.dump(usuarios).data)

@blueprint.route('/api_users/update',methods=['PUT'])
@login_required
def api_users_update():
    if int(request.json['grupo']) == 0: 
        response = {'message': 'Grupo no puede ser nulo.'}
        return jsonify(response), 400
    
    # Encripta la contraseña antes de pasarla a la base de datos
    password = hash_pass(request.json['password'])

    args = {
        "username": request.json['username'],
        "email": request.json['email'],
        "id_grupo": int(request.json['grupo']),
        "activo": request.json['activo'],
        "escrito_por": current_user.id,
        "password": password  # Utiliza el valor encriptado de la contraseña
    }
    
    Usuario.query.filter_by(id=request.json['id']).update(args)
    db.session.commit()
    
    response = {'message': f'Usuario {args["username"]} editado con éxito.'}
    return jsonify(response)


@blueprint.route('/api_users/insert', methods=['POST'])
@login_required
def api_users_insert():
    data = request.json
    username = data['username']
    email = data['email']
    grupo_id = data['grupo']
    activo = data['activo']
    password = data['password']  # Asegúrate de que este campo exista en los datos enviados
    creado_por = current_user.id

    # Crea una nueva instancia del modelo Usuario con los datos recibidos
    new_user = Usuario(username=username, email=email, id_grupo=grupo_id, activo=activo, password=str(password),creado_por=creado_por)

    # Agrega el nuevo usuario a la base de datos y guarda los cambios
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('settings_blueprint.users'))

@blueprint.route('/grupos')
@login_required
def groups():
    return render_template('settings/groups.html', segment='usersSettings_groups')

@blueprint.route('/api_groups',methods=['GET'])
@login_required
def api_groups():
    grupos = Grupo.query.order_by(Grupo.id.asc()).all()
    group_schema = GroupSchema(many=True)
    return jsonify(group_schema.dump(grupos).data)

@blueprint.route('/api_groups/update', methods=['PUT'])
@login_required
def api_groups_update():
    args = {
        "nombre":request.json['nombre'],
        "descripcion":request.json['descripcion'],
        "escrito_por":current_user.id
    }
    Grupo.query.filter_by(id=request.json['id']).update(args)
    db.session.commit()
    response = {'message': f'Grupo {args["nombre"]} editado con exito.'}
    return jsonify(response)

@blueprint.route('/api_groups/insert', methods=['POST'])
@login_required
def api_groups_insert():
    group = Grupo(
        nombre=request.json['nombre'],
        descripcion=request.json['descripcion'],
        escrito_por=current_user.id
    )
    db.session.add(group)
    db.session.commit()
    response = {'message': f'Grupo {group.nombre} creado con exito.'}
    return jsonify(response)
    
@blueprint.route('/empresa')
@login_required
def company():
    empresas = Empresa.query.order_by(Empresa.id.asc()).all()
    return render_template('settings/company.html', segment='companySettings_company', empresas=empresas)

@blueprint.route('/agrega_empresa', methods=['POST','GET'])
@login_required
def add_company():
    versiones = Version.query.order_by(Version.id.asc()).all()
    if request.method == 'POST':
        activo = False
        if request.form.get('activo') =='on':
            activo=True
        company = Empresa(
            nombre=request.form.get('nombre').upper(),
            rfc=request.form.get('rfc').upper(),
            rfcProveedorSW=request.form.get('rfcProveedorSW').upper(),
            version=Version.query.filter_by(nombre=request.form.get('version')).first(),
            ftp_on=activo,
            ftp_host=request.form.get('ftp_host'),
            ftp_port=request.form.get('ftp_port'),
            ftp_username=request.form.get('ftp_username'),
            ftp_password=request.form.get('ftp_password'),
            creado_por=current_user.id
        )
        db.session.add(company)
        db.session.commit()
        return redirect(url_for('settings_blueprint.company'))
    return render_template('settings/add-company.html', segment='companySettings', versiones=versiones)

@blueprint.route('/editar_empresa/<company_id>', methods=['POST','GET'])
@login_required
def edit_company(company_id):
    company=Empresa.query.filter_by(id=company_id).first()
    versiones = Version.query.order_by(Version.id.asc()).all()
    if request.method == 'POST':
        activo = False
        if request.form.get('activo') =='on':
            activo=True
        args={
            "nombre":request.form.get('nombre').upper(),
            "rfc":request.form.get('rfc').upper(),
            "rfcProveedorSW":request.form.get('rfcProveedorSW').upper(),
            "id_version":Version.query.filter_by(nombre=request.form.get('version')).first().id,
            "ftp_on":activo,
            "ftp_host":request.form.get('ftp_host'),
            "ftp_port":request.form.get('ftp_port'),
            "ftp_username":request.form.get('ftp_username'),
            "ftp_password":request.form.get('ftp_password'),
            "escrito_por":current_user.id
        }
        Empresa.query.filter_by(id=company_id).update(args)
        db.session.commit()
        return redirect(url_for('settings_blueprint.company'))
    return render_template('settings/edit-company.html',segment='companySettings', company=company, versiones=versiones)


@blueprint.route('/tanques')
@login_required
def tanks():
    tanques = Tanques.query.all()
    return render_template('settings/tanks.html', segment='stationSettings_tanks', tanques=tanques)

@blueprint.route('/agrega_tanque', methods=['POST','GET'])
@login_required
def add_tanks():
    tanques = Tanques()
    form = TanquesForm(obj=tanques)
    form.id_estacion.choices = [(e.id, e.nombre) for e in Estacion.query.order_by('nombre').all()]
    form.id_producto.choices = [(p.id, p.nombre) for p in Producto.query.order_by('nombre').all()]
    if request.method == 'POST' and form.validate_on_submit():
        try:
            tanques.id_estacion = form.id_estacion.data[0]
            tanques.id_producto = form.id_producto.data[0]
            tanques.no_tanque = form.no_tanque.data
            tanques.volumenUtil = form.volumenUtil.data
            tanques.volumenFondaje = form.volumenFondaje.data
            tanques.volumenAgua = form.volumenAgua.data
            tanques.volumenDisponible = form.volumenDisponible.data
            tanques.volumenExtraccion = form.volumenExtraccion.data
            tanques.volumenRecepcion = form.volumenRecepcion.data
            tanques.temperatura = form.temperatura.data
            tanques.activo = form.activo.data
            tanques.creado_por = current_user.id
            db.session.add(tanques)
            db.session.commit()
            flash("Tipo creado correctamente.",'success')
        except Exception as e:
            print(e)
            flash('Error al agregar objeto: ' + str(e), 'error')
            db.session.rollback()
        return redirect(url_for('settings_blueprint.tanks')) 
    else:
        print(form.errors)
    return render_template('settings/add-tanks.html', segment='stationSettings_tanks', form=form)
    
@blueprint.route('/editar_tanque/<int:id_tanque>', methods=['POST','GET'])
@login_required
def edit_tank(id_tanque):
    return redirect(url_for('settings_blueprint.tanks'))    

@blueprint.route('/productos')
@login_required
def products():
    productos = Producto.query.all()
    return render_template('settings/products.html', segment='stationSettings_products', productos=productos)

@blueprint.route('/agregar_producto')
@login_required
def add_product():
    productos = Producto.query.all()
    form = ProductosForm(obj=productos)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            form.populate_obj(productos)
            db.session.commit()
            flash("Producto actualizado correctamente.",'success')
            return redirect(url_for('settings_blueprint.products'))
        except Exception as e:
            flash('Error al agregar objeto: ' + str(e), 'error')
            db.session.rollback()
    return render_template('settings/add-product.html', segment='stationSettings_products', form=form)

@blueprint.route('editar_producto/<id_producto>', methods=['POST', 'GET'])
@login_required
def edit_product(id_producto):
    producto = Producto.query.filter_by(id=id_producto).first()
    form = ProductosForm(obj=producto)
    print(form.validate_on_submit())
    if request.method == 'POST' and form.validate_on_submit():
        try:
            form.populate_obj(producto)
            db.session.commit()
            flash("Producto actualizado correctamente.",'success')
            return redirect(url_for('settings_blueprint.products'))
        except Exception as e:
            flash('Error al editar objeto: ' + str(e), 'error')
            db.session.rollback()
    return render_template('settings/edit-product.html', segment='stationSettings_products', form=form)

@blueprint.route('dispensarios')
@login_required
def dispensarios():
    dispensarios = Dispensario.query.order_by(Dispensario.id.asc()).all()
    #form = DispensariosForm(obj=dispensarios)
    return render_template('settings/dispensarios.html', segment='stationSettings_dispensarios', dispensarios=dispensarios)

@blueprint.route('agregar_dispensario', methods=['POST','GET'])
@login_required
def add_dispensario():
    dispensario = Dispensario.query.all()
    form = DispensariosForm(obj=dispensario)
    form.id_estacion.choices = [(e.id, e.nombre) for e in Estacion.query.order_by('nombre').all()] 

    # Obtener las opciones para el campo id_producto
    opciones_id_producto = [(p.id, p.nombre) for p in Producto.query.order_by('nombre').all()]
    # Convertir las opciones a formato JSON
    opciones_id_producto_json = json.dumps(opciones_id_producto)

    # Establecer las opciones para el campo id_producto en cada instancia de MangueraForm
    for manguera in form.mangueras:
        manguera.id_producto.choices = opciones_id_producto

    if request.method == 'POST' and form.validate_on_submit():
        try:
            print(form.data)
            dispendarioObj = Dispensario(
                numeroDispensario = request.form.get('numeroDispensario'),
                id_estacion = request.form.get('id_estacion'),
                creado_por = current_user.id
            )
            db.session.add(dispendarioObj)
            db.session.commit()
            for manguera in form.mangueras.data:
                print(manguera)
                mangueraObj = Manguera(
                    identificadorManguera = manguera.get('identificadorManguera'),
                    id_Dispensario = dispendarioObj.id,
                    id_producto = manguera.get('id_producto'),
                    creado_por = current_user.id
                )
                print(mangueraObj.identificadorManguera)
                print(mangueraObj.id_Dispensario)
                print(mangueraObj.id_producto)
                db.session.add(mangueraObj)
                db.session.commit()
            flash("Producto actualizado correctamente.",'success')
            return redirect(url_for('settings_blueprint.dispensarios'))
        except Exception as e:
            print(e)
            flash('Error al editar objeto: ' + str(e), 'error')
            db.session.rollback()
    return render_template('settings/add-dispensarios.html', segment='stationSettings_dispensarios-crear', form=form, opciones_id_producto=opciones_id_producto_json)


@blueprint.route('editar_dispensario/<id_dispensario>', methods=['POST','GET'])
@login_required
def edit_dispensario(id_dispensario):
    dispensario = Dispensario.query.filter_by(id=id_dispensario).first()
    form = DispensariosForm(obj=dispensario)
    form.id_estacion.choices = [(e.id, e.nombre) for e in Estacion.query.order_by('nombre').all()] 

    # Obtener las opciones para el campo id_producto
    opciones_id_producto = [(p.id, p.nombre) for p in Producto.query.order_by('nombre').all()]
    # Convertir las opciones a formato JSON
    opciones_id_producto_json = json.dumps(opciones_id_producto)

    # Establecer las opciones para el campo id_producto en cada instancia de MangueraForm
    for manguera in form.mangueras:
        manguera.id_producto.choices = opciones_id_producto
        
    if request.method == 'POST' and form.validate_on_submit():
        # Transferir los datos del formulario al objeto dispensario
        form.populate_obj(dispensario)
        
        # Transferir datos de cada manguera individualmente
        for i, manguera_form in enumerate(form.mangueras.entries):
            manguera_obj = dispensario.mangueras[i]  # Accedemos directamente a la manguera en la lista de mangueras

            # Recrea el formulario MangueraForm con los datos específicos de esta manguera
            manguera_form_updated = MangueraForm(**manguera_form.data)

            # Llena el objeto manguera con los datos del formulario actualizado
            manguera_form_updated.populate_obj(manguera_obj)

            # Agregar el id_dispensario a la manguera
            manguera_obj.id_Dispensario = dispensario.id

        # Guardar los cambios en la base de datos
        db.session.commit()
        flash('Dispensario editado exitosamente', 'success')
        return redirect(url_for('settings_blueprint.dispensarios'))
    return render_template('settings/edit-dispensarios.html', segment='stationSettings_dispensarios-editar', form=form, opciones_id_producto=opciones_id_producto_json, dispensario=dispensario)

@blueprint.route('/zonas')
@login_required
def zones():
    zonas = Zona.query.order_by(Zona.id.asc()).all()
    return render_template('settings/zones.html', segment='stationSettings_zones', zonas=zonas)

@blueprint.route('/agregar_zona', methods=['POST','GET'])
@login_required
def add_zone():
    if request.method == 'POST':
        zona = Zona(
            nombre=request.form.get('nombre').upper(),
            creado_por=current_user.id
        )
        db.session.add(zona)
        db.session.commit()
        return redirect(url_for('settings_blueprint.zones'))
    return render_template('settings/add-zone.html',segment='stationSettings')

@blueprint.route('/editar_zona/<zone_id>', methods=['POST','GET'])
@login_required
def edit_zone(zone_id):
    zone = Zona.query.filter_by(id=zone_id).first()
    if request.method == 'POST':
        args={
            "nombre":request.form.get('nombre').upper(),
            "escrito_por":current_user.id
        }
        Zona.query.filter_by(id=zone_id).update(args)
        db.session.commit()
        return redirect(url_for('settings_blueprint.zones'))
    return render_template('settings/edit-zone.html',segment='stationSettings',zone=zone)


@blueprint.route('/estaciones')
@login_required
def stations():
    estaciones = Estacion.query.order_by(Estacion.id.asc()).all()
    return render_template('settings/stations.html', segment='stationSettings_stations', estaciones=estaciones)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@blueprint.route('/upload_xml<int:station_id>', methods=['POST'])
@login_required
def upload_file(station_id):
    print("*"*20)
    print("ID de la estación:", station_id)
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        # Aquí puedes añadir lógica adicional para procesar el XML si es necesario
        content = file.read()  # Leer el contenido del archivo
        doc = minidom.parseString(content)
        estacion = Estacion.query.filter_by(id=station_id).first()
        nodos = doc.getElementsByTagName("controlesvolumetricos:ControlesVolumetricos")
        if nodos:
            primer_nodo = nodos[0]
            numeroPermisoCRE_nodo = primer_nodo.getAttribute("numeroPermisoCRE")
            if estacion.numeroPermisoCRE != numeroPermisoCRE_nodo:
                flash("El número de permiso CRE no coincide.", "error")  # Mensaje de error usando la categoría "error"
                return redirect(url_for('settings_blueprint.stations'))
        for tanque in doc.getElementsByTagName("controlesvolumetricos:EXI"):
            producto = Producto.query.filter_by(
                                            claveProducto=tanque.getAttribute("claveProducto"),
                                            claveSubProducto=tanque.getAttribute("claveSubProducto")
                                            ).first()
            tanque_data = Tanques()
            tanque_data.id_estacion = station_id
            tanque_data.id_producto = producto.id
            tanque_data.no_tanque = tanque.getAttribute("numeroTanque")
            tanque_data.volumenUtil = tanque.getAttribute("volumenUtil")
            tanque_data.volumenFondaje = tanque.getAttribute("volumenFondaje")
            tanque_data.volumenAgua = tanque.getAttribute("volumenAgua")
            tanque_data.volumenDisponible = tanque.getAttribute("volumenDisponible")
            tanque_data.volumenExtraccion = tanque.getAttribute("volumenExtraccion")
            tanque_data.volumenRecepcion = tanque.getAttribute("volumenRecepcion")
            tanque_data.temperatura = tanque.getAttribute("temperatura")
            tanque_data.activo = True
            tanque_data.creado_por = current_user.id
            db.session.add(tanque_data)
            db.session.commit()
    
        # Diccionario para mantener un seguimiento de los dispensarios ya creados.
        dispensarios_creados = {}
        for dispensario in doc.getElementsByTagName("controlesvolumetricos:DIS"):
            numeroDispensario = dispensario.getAttribute("numeroDispensario")
            identificadorManguera = dispensario.getAttribute("identificadorManguera")
            claveProducto = dispensario.getAttribute("claveProducto")
            claveSubProducto = dispensario.getAttribute("claveSubProducto")
            composicionOctanajeDeGasolina = dispensario.getAttribute("composicionOctanajeDeGasolina")
            gasolinaConEtanol = dispensario.getAttribute("gasolinaConEtanol")
            producto = Producto.query.filter_by(
                                            claveProducto=dispensario.getAttribute("claveProducto"),
                                            claveSubProducto=dispensario.getAttribute("claveSubProducto")
                                            ).first()
            # Verificar si el dispensario ya se ha creado o no.
            if numeroDispensario not in dispensarios_creados:
                dispensario = Dispensario(
                    numeroDispensario=numeroDispensario, 
                    id_estacion=station_id,
                    creado_por = current_user.id
                    )
                db.session.add(dispensario)
                db.session.commit()
                dispensarios_creados[numeroDispensario] = dispensario
            else:
                dispensario = dispensarios_creados[numeroDispensario]
            
            # Crear manguera asociada a este dispensario.
            manguera = Manguera(
                identificadorManguera=identificadorManguera, 
                id_Dispensario=dispensario.id, 
                id_producto=int(producto.id),
                creado_por = current_user.id
                )
            db.session.add(manguera)
            db.session.commit()
        return redirect(url_for('settings_blueprint.stations'))  # Redirecciona a donde quieras después de subir el archivo
    
@blueprint.route('/agregar_estacion', methods=['POST','GET'])
@login_required
def add_station():
    estacion = Estacion()
    form = EstacionForm(obj=estacion)
    form.id_zona.choices = [(e.id, e.nombre) for e in Zona.query.order_by('nombre').all()]
    form.id_empresa.choices = [(e.id, e.nombre) for e in Empresa.query.order_by('nombre').all()]
    form.id_producto.choices = [(e.id, e.nombre) for e in Producto.query.order_by('nombre').all()]
    if request.method == 'POST' and form.validate_on_submit():
        estacion.creado_por = current_user.id
        #agregar codigo para guardar objeto
        station_directory = os.path.join(current_app.config['UPLOAD_FOLDER'], form.nombre.data.upper())
        
        if not os.path.exists(station_directory):
            os.makedirs(station_directory)

        # Guardar el archivo key y obtener su ruta relativa
        if 'key_file' in request.files and allowed_file(request.files['key_file'].filename):
            key_file = request.files['key_file']
            key_filename = secure_filename(key_file.filename)
            key_file_path = os.path.join(station_directory, key_filename)
            key_file.save(key_file_path)
            estacion.key_file_path = os.path.join(form.nombre.data.upper(), key_filename)

        # Guardar el archivo cer y obtener su ruta relativa
        if 'cer_file' in request.files and allowed_file(request.files['cer_file'].filename):
            cer_file = request.files['cer_file']
            cer_filename = secure_filename(cer_file.filename)
            cer_file_path = os.path.join(station_directory, cer_filename)
            cer_file.save(cer_file_path)
            estacion.cer_file_path = os.path.join(form.nombre.data.upper(), cer_filename)
            estacion.noCertificado = os.path.splitext(cer_filename)[0]
            estacion.certificado_value = CerData(cer_file_path)

        # Generar el archivo PEM y obtener su ruta relativa
        if estacion.key_file_path:
            GenPem(estacion.key_file_path, form.nombre.data.upper())
            pem_filename = secure_filename(form.nombre.data.upper() + '.pem')
            estacion.pem_file_path = os.path.join(form.nombre.data.upper(), pem_filename)
        
        
        estacion.nombre = form.nombre.data.upper()
        estacion.id_zona = form.id_zona.data[0]
        estacion.numeroPermisoCRE = form.numeroPermisoCRE.data
        estacion.id_empresa = form.id_empresa.data[0]
        estacion.activo = form.activo.data
        estacion.ruta = form.ruta.data
        estacion.claveClientePEMEX = form.claveClientePEMEX.data
        estacion.claveEstacionServicio = form.claveEstacionServicio.data
        
        print(estacion.cer_file_path)
        
        db.session.add(estacion)
        db.session.commit()
        # Insertar relaciones en la tabla intermedia
        productos_ids = request.form.getlist('id_producto')

        for producto_id in productos_ids:
            print(producto_id)
            insert_statement = estaciones_productos.insert().values(estacion_id=estacion.id, producto_id=producto_id)
            print(insert_statement)
            db.session.execute(insert_statement)
        db.session.commit()
        return redirect(url_for('settings_blueprint.stations'))

    return render_template('settings/add-stations.html', segment='stationSettings',form=form)

@blueprint.route('/editar_estacion/<station_id>', methods=['POST', 'GET'])
@login_required
def edit_station(station_id):
    estacion = Estacion.query.filter_by(id=station_id).first()
    form = EstacionForm(obj=estacion)
    form.id_zona.choices = [(e.id, e.nombre) for e in Zona.query.order_by('nombre').all()]
    form.id_empresa.choices = [(e.id, e.nombre) for e in Empresa.query.order_by('nombre').all()]
    form.id_producto.choices = [(e.id, e.nombre) for e in Producto.query.order_by('nombre').all()]
    
    productos_estacion = db.session.query(estaciones_productos.c.producto_id).filter_by(estacion_id=station_id).all()
    print(productos_estacion)
    productos_estacion_ids = [item[0] for item in productos_estacion]
    print(productos_estacion_ids)
    form.id_producto.data = productos_estacion_ids

    form.tanques.entries.clear()
    tanques = Tanques.query.filter_by(id_estacion=station_id).all()
    for tanque in tanques:
        tanque_form = EstacionTanquesForm()
        tanque_form.no_tanque = tanque.no_tanque
        tanque_form.producto = tanque.producto.nombre
        tanque_form.volumenUtil = tanque.volumenUtil
        tanque_form.volumenDisponible = tanque.volumenDisponible
        form.tanques.append_entry(tanque_form)
    
    cer_file_name = None
    if estacion.cer_file_path:
        cer_file_name = secure_filename('cer_file.pem')

    if request.method == 'POST' and form.validate_on_submit():
        estacion.escrito_por = current_user.id 

        # Define el directorio para esta estación, y crea el directorio si no existe
        station_directory = os.path.join(current_app.config['UPLOAD_FOLDER'], estacion.nombre)
        if not os.path.exists(station_directory):
            os.makedirs(station_directory)

        # Guardar el archivo key y obtener su ruta relativa
        if 'key_file' in request.files and allowed_file(request.files['key_file'].filename):
            key_file = request.files['key_file']
            key_filename = secure_filename(key_file.filename)
            key_file_path = os.path.join(station_directory, key_filename)
            key_file.save(key_file_path)
            estacion.key_file_path = os.path.join(estacion.nombre, key_filename)

        # Guardar el archivo cer y obtener su ruta relativa
        if 'cer_file' in request.files and allowed_file(request.files['cer_file'].filename):
            cer_file = request.files['cer_file']
            cer_filename = secure_filename(cer_file.filename)
            cer_file_path = os.path.join(station_directory, cer_filename)
            cer_file.save(cer_file_path)
            estacion.cer_file_path = os.path.join(estacion.nombre, cer_filename)
            estacion.noCertificado = os.path.splitext(cer_filename)[0]
            estacion.certificado_value = CerData(cer_file_path)

        # Generar el archivo PEM y obtener su ruta relativa
        if estacion.key_file_path:
            GenPem(estacion.key_file_path, estacion.nombre)
            pem_filename = secure_filename(estacion.nombre + '.pem')
            estacion.pem_file_path = os.path.join(estacion.nombre, pem_filename)

        estacion.nombre = form.nombre.data
        estacion.id_zona = form.id_zona.data[0]
        estacion.numeroPermisoCRE = form.numeroPermisoCRE.data
        estacion.id_empresa = form.id_empresa.data[0]
        estacion.activo = form.activo.data
        estacion.ruta = form.ruta.data
        estacion.claveClientePEMEX = form.claveClientePEMEX.data
        estacion.claveEstacionServicio = form.claveEstacionServicio.data
        
        # Eliminar las asociaciones existentes
        delete_statement = estaciones_productos.delete().where(estaciones_productos.c.estacion_id == estacion.id)
        db.session.execute(delete_statement)

        # Agregar las nuevas asociaciones
        productos_ids = request.form.getlist('id_producto')
        for producto_id in productos_ids:
            print(producto_id)
            insert_statement = estaciones_productos.insert().values(estacion_id=estacion.id, producto_id=producto_id)
            print(insert_statement)
            db.session.execute(insert_statement)


        db.session.commit()
        return redirect(url_for('settings_blueprint.stations'))
    
    return render_template('settings/edit-stations.html', segment='stationSettings_stationsEdit', form=form, cer_file_name=cer_file_name)

