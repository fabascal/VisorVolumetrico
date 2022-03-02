# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - NovaRet
"""
from flask_login import UserMixin
from website import db , login_manager, ma
from website.authentication.utils import hash_pass
from sqlalchemy.sql import func
from sqlalchemy import event


class Producto(db.Model):
    __tablename__='productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=True, nullable=False)
    claveProducto = db.Column(db.String(2), unique=False, nullable=False)
    claveSubProducto = db.Column(db.String(1), unique=True, nullable=False)
    creado_en = db.Column(db.DateTime(timezone=False),default=func.now())
    creado_por = db.Column(db.Integer)
    escrito_en = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    escrito_por = db.Column(db.Integer)
    
@event.listens_for(Producto.__table__,'after_create')
def create_products(*args, **kwargs):
    magna = Producto(nombre='GASOLINA CONTENIDO MINIMO 87 OCTANO',claveProducto='07',claveSubProducto='1',creado_por=1)
    premium = Producto(nombre='GASOLINA CONTENIDO MINIMO 92 OCTANO',claveProducto='07',claveSubProducto='2',creado_por=1)
    diesel = Producto(nombre='DIESEL AUTOMOTRIZ',claveProducto='03',claveSubProducto='3',creado_por=1)
    db.session.add(magna)
    db.session.add(premium)
    db.session.add(diesel)
    db.session.commit()
    
class Version(db.Model):
    __tablename__ = 'versiones'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=True, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime(timezone=False),default=func.now())
    creado_por = db.Column(db.Integer)
    escrito_en = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    escrito_por = db.Column(db.Integer)

class Zona(db.Model):
    __tablename__='zonas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=True, nullable=False)
    creado_en = db.Column(db.DateTime(timezone=False),default=func.now())
    creado_por = db.Column(db.Integer)
    escrito_en = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    escrito_por = db.Column(db.Integer)

class Estacion(db.Model):
    __tablename__='estaciones'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=True, nullable=False)
    id_zona = db.Column(db.Integer, db.ForeignKey('zonas.id'), nullable=True, index=True)
    zona = db.relationship('Zona', backref='zona', passive_deletes=True)
    numeroPermisoCRE = db.Column(db.String(30), unique=True, nullable=False)
    id_empresa = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=True, index=True)
    activo = db.Column(db.Boolean, default=True)
    ruta = db.Column(db.String(100),nullable=False)
    creado_en = db.Column(db.DateTime(timezone=False),default=func.now())
    creado_por = db.Column(db.Integer)
    escrito_en = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    escrito_por = db.Column(db.Integer)

class EstacionSchema(ma.ModelSchema):
    class Meta:
        model = Estacion
        sqla_session = db.session
        
class Empresa(db.Model):
    __tablename__ = 'empresas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=True, nullable=False)
    rfc = db.Column(db.String(30), unique=True, nullable=False)
    rfcProveedorSW = db.Column(db.String(30), nullable=False)
    id_version = db.Column(db.Integer, db.ForeignKey('versiones.id'), nullable=True, index=True)
    version = db.relationship('Version', backref='empresa', passive_deletes=True)
    estaciones = db.relationship('Estacion',backref='empresas', passive_deletes=True)
    ftp_on = db.Column(db.Boolean, default=False)
    ftp_host = db.Column(db.String(30), unique=False, nullable=False)
    ftp_port = db.Column(db.String(30), unique=False, nullable=False)
    ftp_username = db.Column(db.String(30), unique=False, nullable=False)
    ftp_password = db.Column(db.String(30), unique=False, nullable=False)
    creado_en = db.Column(db.DateTime(timezone=False),default=func.now())
    creado_por = db.Column(db.Integer)
    escrito_en = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    escrito_por = db.Column(db.Integer)
    
class EmpresaSchema(ma.ModelSchema):
    class Meta:
        model = Empresa
        sqla_session = db.session
        
@event.listens_for(Version.__table__,'after_create')
def create_version(*args, **kwargs):
    version = Version(nombre="1.2", creado_por=1)
    db.session.add(version)
    db.session.commit() 