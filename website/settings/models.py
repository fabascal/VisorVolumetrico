# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - NovaRet
"""
from flask_login import UserMixin
from website import db , login_manager, ma
from website.authentication.utils import hash_pass
from sqlalchemy.sql import func
from sqlalchemy.orm import deferred
from sqlalchemy import event

estaciones_productos = db.Table('estaciones_productos',
    db.Column('estacion_id', db.Integer, db.ForeignKey('estaciones.id'), primary_key=True),
    db.Column('producto_id', db.Integer, db.ForeignKey('productos.id'), primary_key=True)
)

class Producto(db.Model):
    __tablename__='productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=True, nullable=False)
    nombre_corto = db.Column(db.String(30), unique=True, nullable=False, default="a")
    claveProducto = db.Column(db.String(2), unique=False, nullable=False)
    claveSubProducto = db.Column(db.String(1), unique=True, nullable=False)
    composicionOctanajeDeGasolina = db.Column(db.String(2))
    gasolinaConEtanol = db.Column(db.String(2))
    claveProductoPEMEX = db.Column(db.String(30), unique=True, nullable=False)
    creado_en = db.Column(db.DateTime(timezone=False),default=func.now())
    creado_por = db.Column(db.Integer)
    escrito_en = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    escrito_por = db.Column(db.Integer)
    
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
    claveClientePEMEX = db.Column(db.String(30), unique=True, nullable=False)
    claveEstacionServicio = db.Column(db.String(30), unique=True, nullable=False)
    key_file_path = db.Column(db.String(255))
    cer_file_path = db.Column(db.String(255))
    pem_file_path = db.Column(db.String(255))
    noCertificado = db.Column(db.String(255))
    certificado_value = db.Column(db.String())
    productos = db.relationship('Producto', secondary=estaciones_productos, backref=db.backref('estaciones', lazy=True))
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
    version = db.relationship('Version', backref='version', passive_deletes=True)
    estaciones = db.relationship('Estacion', backref='empresa', passive_deletes=True)
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
    
class Dispensario(db.Model):
    __tablename__ = 'dispensario'
    id = db.Column(db.Integer, primary_key=True)
    numeroDispensario = db.Column(db.String(2), unique=True, nullable=False)
    id_estacion = db.Column(db.Integer, db.ForeignKey('estaciones.id'), nullable=True, index=True)
    estacion = db.relationship('Estacion', backref='dispensario')
    creado_en = db.Column(db.DateTime(timezone=False),default=func.now())
    creado_por = db.Column(db.Integer)
    escrito_en = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    escrito_por = db.Column(db.Integer)
    
class Manguera(db.Model):
    __tablename__ = 'manguera'
    id = db.Column(db.Integer, primary_key=True)
    identificadorManguera = db.Column(db.String(1), unique=False, nullable=False)
    id_Dispensario = db.Column(db.Integer, db.ForeignKey('dispensario.id'), nullable=True, index=True)
    Dispensario = db.relationship('Dispensario', backref='mangueras')
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=True, index=True)
    producto = db.relationship('Producto', backref='manguera')
    creado_en = db.Column(db.DateTime(timezone=False),default=func.now())
    creado_por = db.Column(db.Integer)
    escrito_en = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    escrito_por = db.Column(db.Integer)
    
class Tanques (db.Model):
    __tablename__ = 'tanques'
    id = db.Column(db.Integer, primary_key=True)
    id_estacion = db.Column(db.Integer, db.ForeignKey('estaciones.id'), nullable=True, index=True)
    estacion = db.relationship('Estacion', backref='tanques')
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=True, index=True)
    producto = db.relationship('Producto', backref='tanques')
    no_tanque = db.Column(db.Integer)
    volumenUtil = db.Column(db.Integer)
    volumenFondaje = db.Column(db.Integer)
    volumenAgua = db.Column(db.Integer)
    volumenDisponible = db.Column(db.Integer)
    volumenExtraccion = db.Column(db.Integer)
    volumenRecepcion = db.Column(db.Integer)
    temperatura = db.Column(db.Float)
    activo = db.Column(db.Boolean, default=True)
    fecha_reporte = db.Column(db.DateTime(timezone=False),default=func.now())
    creado_en = db.Column(db.DateTime(timezone=False),default=func.now())
    creado_por = db.Column(db.Integer)
    escrito_en = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    escrito_por = db.Column(db.Integer)
    
    def serialize(self):
        return {
            'id': self.id,
            'id_estacion': self.id_estacion,
            'id_producto': self.id_producto,
            'no_tanque': self.no_tanque,
            'volumenUtil': self.volumenUtil,
            'volumenFondaje': self.volumenFondaje,
            'volumenAgua': self.volumenAgua,
            'volumenDisponible': self.volumenDisponible,
            'volumenExtraccion': self.volumenExtraccion,
            'volumenRecepcion': self.volumenRecepcion,
            'temperatura': self.temperatura,
            'activo': self.activo,
            'fecha_reporte': self.fecha_reporte.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_reporte else None,
            'creado_en': self.creado_en.strftime('%Y-%m-%d %H:%M:%S') if self.creado_en else None,
            'creado_por': self.creado_por,
            'escrito_en': self.escrito_en.strftime('%Y-%m-%d %H:%M:%S') if self.escrito_en else None,
            'escrito_por': self.escrito_por
        }
    