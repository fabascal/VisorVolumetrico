# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present NovaRet
"""

from website import db
from website.settings import blueprint
from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user


from website.authentication.models import Usuario, UserSchema, Grupo, GroupSchema
from website.settings.models import Empresa, EmpresaSchema, Version, EstacionSchema, Zona, Estacion

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
    if int(request.json['grupo']) ==0: 
        response = {'message': 'Grupo no puede ser nulo.'}
        return jsonify(response), 400
    args = {
        "username" : request.json['username'],
        "email" : request.json['email'],
        "id_grupo": int(request.json['grupo']),
        "activo": request.json['activo'],
        "escrito_por": current_user.id
    }
    Usuario.query.filter_by(id=request.json['id']).update(args)
    db.session.commit()
    response = {'message': f'Usuario {args["username"]} editado con exito.'}
    return jsonify(response)


@blueprint.route('/api_users/insert', methods=['POST'])
@login_required
def api_users_insert():
    print (request.json['username'])
    user = Usuario
    #crear funcion para generar password aleatoreo y realizar envio de correo para cambiar contraseña.
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
    usuario = Usuario.query.filter_by(id=current_user.id).first()
    data = {"usuario":usuario}
    return render_template('settings/groups.html', segment='stationSettings_tanks', data=data)

@blueprint.route('/productos')
@login_required
def products():
    usuario = Usuario.query.filter_by(id=current_user.id).first()
    data = {"usuario":usuario}
    return render_template('settings/groups.html', segment='stationSettings_products', data=data)

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

@blueprint.route('/agregar_estacion', methods=['POST','GET'])
@login_required
def add_station():
    zonas = Zona.query.order_by(Zona.id.asc()).all()
    empresa = Empresa.query.order_by(Empresa.id.asc()).all()
    if request.method == 'POST':
        activo = False
        if request.form.get('activo')=='on':
            activo=True 
        estacion = Estacion(
            nombre=request.form.get('nombre').upper(),
            numeroPermisoCRE=request.form.get('numeroPermisoCRE'),
            id_empresa=request.form.get('empresa'),
            id_zona=request.form.get('zona'),
            activo=activo,
            ruta=request.form.get('ruta'),
            creado_por=current_user.id
        )
        print(estacion.id_empresa)
        db.session.add(estacion)
        db.session.commit()
        return redirect(url_for('settings_blueprint.stations'))
    return render_template('settings/add-stations.html', segment='stationSettings', zonas=zonas, empresas=empresa)

@blueprint.route('/editar_estacion/<station_id>', methods=['POST','GET'])
@login_required
def edit_station(station_id):
    zonas = Zona.query.order_by(Zona.id.asc()).all()
    empresa = Empresa.query.order_by(Empresa.id.asc()).all()
    estacion = Estacion.query.filter_by(id=station_id).first()
    if request.method == 'POST':
        activo = False
        if request.form.get('activo') =='on':
            activo=True
        args={
            "nombre":request.form.get('nombre').upper(),
            "numeroPermisoCRE":request.form.get('numeroPermisoCRE').upper(),
            "id_empresa":request.form.get('empresa'),
            "id_zona":request.form.get('zona'),
            "activo":activo,
            "ruta":request.form.get('ruta'),
            "escrito_por":current_user.id
        }
        Estacion.query.filter_by(id=station_id).update(args)
        db.session.commit()
        return redirect(url_for('settings_blueprint.stations'))
    return render_template('settings/edit-stations.html', segment='stationSettings', zonas=zonas, empresas =empresa, estacion=estacion)