# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - NovaRet
"""
from flask_login import UserMixin
from website import db , login_manager, ma
from website.authentication.utils import hash_pass
from sqlalchemy.sql import func
from sqlalchemy import event
from dataclasses import dataclass
    

class Grupo(db.Model):
    __tablename__ = 'grupos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=True, nullable=False, default="Grupo")
    descripcion = db.Column(db.String(150), nullable=False, default="Descripción")
    creado_en = db.Column(db.DateTime(timezone=False),default=func.now())
    creado_por = db.Column(db.Integer)
    escrito_en = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    escrito_por = db.Column(db.Integer)
    
    def as_dict(self):
           return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class GroupSchema(ma.ModelSchema):
    class Meta:
        model = Grupo
        sqla_session = db.session

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150))
    password = db.Column(db.String(150), unique=False)
    activo = db.Column(db.Boolean, default=True)
    id_grupo = db.Column(db.Integer, db.ForeignKey('grupos.id'), nullable=True, index=True)
    grupo = db.relationship('Grupo', backref='grupo', passive_deletes=True)
    creado_en = db.Column(db.DateTime(timezone=False),default=func.now())
    creado_por = db.Column(db.Integer)
    escrito_en = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    escrito_por = db.Column(db.Integer)
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)
    
    def as_dict(self):
           return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class UserSchema(ma.ModelSchema):
    class Meta:
        model = Usuario
        sqla_session = db.session

@login_manager.user_loader
def user_loader(id):
    return Usuario.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Usuario.query.filter_by(username=username).first()
    return user if user else None
    
    
@event.listens_for(Grupo.__table__,'after_create')
def create_groups(*args, **kwargs):
    admin = Grupo(nombre='Administrador',descripcion='Grupo de administradores, perfil con acceso a todos los menus.',creado_por=1)
    portal = Grupo(nombre='Portal',descripcion='Grupo portal, es el grupo por defecto creado desde el portal.',creado_por=1)
    db.session.add(admin)
    db.session.add(portal)
    db.session.commit()
    
@event.listens_for(Usuario.__table__,'after_create')
def create_user(*args, **kwargs):
    grupo = Grupo.query.filter_by(nombre='Administrador').first()
    admin = Usuario(email='admin@mail.com',username='Admin',password=str(1234),id_grupo=grupo.id,creado_por=1)
    db.session.add(admin)
    db.session.commit()

   