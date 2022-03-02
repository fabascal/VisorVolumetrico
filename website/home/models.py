# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - NovaRet
"""
from flask_login import UserMixin
from website import db , login_manager, ma
from website.authentication.utils import hash_pass
from sqlalchemy.sql import func
from sqlalchemy import event
from website.settings.models import Producto
from datetime import datetime, date
from ..settings.models import Producto

class Reporte(db.Model):
    __tablename__='reportes'
    id = db.Column(db.Integer, primary_key=True)
    id_estacion = db.Column(db.Integer, db.ForeignKey('estaciones.id'), nullable=True, index=True)
    estacion = db.relationship('Estacion', backref='estacion', passive_deletes=True)
    fecha = db.Column(db.Date)
    estado = db.Column(db.String(50))
    creado_en = db.Column(db.DateTime(timezone=False),default=func.now())
    creado_por = db.Column(db.Integer)
    escrito_en = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    escrito_por = db.Column(db.Integer)
    compra = db.relationship('Reporte_Linea_Compra', backref='compra', passive_deletes=True)
    venta = db.relationship('Reporte_Linea_Venta', backref='venta', passive_deletes=True)
    excel = db.Column(db.Text)
    dispensarios = db.Column(db.Integer)
    mangueras = db.Column(db.Integer)
    
class Reporte_Linea_Compra(db.Model):
    __tablename__='reporte_lineas_compras'
    id = db.Column(db.Integer, primary_key=True)
    id_reporte = db.Column(db.Integer, db.ForeignKey('reportes.id'), nullable=False, index=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False, index=True)
    producto = db.relationship("Producto", backref='producto', passive_deletes=False)
    numeroTanque = db.Column(db.String(2))
    volumenUtil = db.Column(db.Float)
    volumenFondaje = db.Column(db.Float)
    volumenAgua = db.Column(db.Float)
    volumenDisponible = db.Column(db.Float)
    volumenExtraccion = db.Column(db.Float)
    volumenRecepcion = db.Column(db.Float)
    temperatura = db.Column(db.Float)
    capacidadTotalTanque = db.Column(db.Float)
    capacidadOperativaTanque = db.Column(db.Float)
    capacidadUtilTanque = db.Column(db.Float)
    capacidadFondajeTanque = db.Column(db.Float)
    volumenMinimoOperacion = db.Column(db.Float)
    estadoTanque = db.Column(db.String(1))
    creado_en = db.Column(db.DateTime(timezone=False),default=func.now())
    creado_por = db.Column(db.Integer)
    escrito_en = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    escrito_por = db.Column(db.Integer)
    
class Reporte_Linea_Venta(db.Model):
    __tablename__='reporte_lineas_venta'
    id = db.Column(db.Integer, primary_key=True)
    id_reporte = db.Column(db.Integer, db.ForeignKey('reportes.id'), nullable=False, index=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False, index=True)
    numeroTotalRegistrosDetalle = db.Column(db.Integer, nullable=False)
    numeroDispensario = db.Column(db.String(2))
    identificadorManguera = db.Column(db.String(1))
    sumatoriaVolumenDespachado = db.Column(db.Float)
    sumatoriaVentas = db.Column(db.Float)
    creado_en = db.Column(db.DateTime(timezone=False),default=func.now())
    creado_por = db.Column(db.Integer)
    escrito_en = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    escrito_por = db.Column(db.Integer)

