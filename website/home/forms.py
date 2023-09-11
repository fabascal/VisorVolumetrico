from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField, BooleanField, SelectMultipleField, DateField,StringField, Form, IntegerField
from wtforms.fields import FieldList, FormField
from wtforms.validators import  InputRequired, NumberRange
from wtforms.widgets import CheckboxInput
from website.settings.models import Tanques
from datetime import date


class GenXmlTanquesCampos(Form):
    no_tanque = StringField('Numero tanque', render_kw={'readonly': True})
    producto = StringField('Producto', render_kw={'readonly': True})
    claveProducto = StringField('claveProducto')
    claveSubProducto = StringField('claveSubProducto')
    claveProductoPEMEX = StringField('claveProductoPEMEX')
    composicionOctanajeDeGasolina = StringField('composicionOctanajeDeGasolina')
    gasolinaConEtanol = StringField('gasolinaConEtanol')
    volumenUtil = StringField('volumenUtil')
    volumenFondaje = StringField('volumenFondaje')
    volumenAgua = StringField('volumenAgua')
    temperatura = StringField('temperatura')
    volumenDisponible = DecimalField('Volumen Disponible')
    volumenExtraccion = DecimalField('Volumen Extraccion')
    volumenRecepcion = DecimalField('Volumen Recepcion')
    
class GenXmlRecepcionesCampos(Form):
    recepcion = BooleanField('¿Recepción?', widget=CheckboxInput())
    no_tanque_recepcion = StringField('Numero tanque', render_kw={'readonly': True})
    producto = StringField('Producto', render_kw={'readonly': True})
    claveProducto = StringField('claveProducto')
    claveSubProducto = StringField('claveSubProducto')
    composicionOctanajeDeGasolina = StringField('composicionOctanajeDeGasolina')
    gasolinaConEtanol = StringField('gasolinaConEtanol')
    folioUnicoRecepcionCabecera = StringField('Folio Unico Recepcion', render_kw={'readonly': True})
    folioUnicoRecepcion = StringField('Folio Unico Recepcion', render_kw={'readonly': True})
    volumenInicialTanque = StringField('Volumen Inicial', render_kw={'readonly': True})
    volumenFinalTanque = StringField('Volumen Final', render_kw={'readonly': True})
    volumenRecepcion = StringField('Volumen Recepcion', render_kw={'readonly': True})
    temperatura = StringField('Temperatura')
    fechaYHoraRecepcion = StringField('Fecha y Hora Recepcion')
    folioUnicoRelacion = StringField('Folio Unico Relacion', render_kw={'readonly': True})

class GenXmlVentas(Form):
    id_producto = IntegerField('id_producto', render_kw={'readonly': True})
    producto = StringField('Producto', render_kw={'readonly': True})
    claveProductoPEMEX = StringField('claveProductoPEMEX', render_kw={'readonly': True})
    litros = DecimalField('Litros',validators=[NumberRange(min=0)])
    precio = DecimalField('Precio',validators=[NumberRange(min=0)])
    
class GeneratorXmlForm(FlaskForm):
    id_estacion = SelectMultipleField('Estación', coerce=int)
    fecha = DateField('Fecha', validators=[InputRequired()], default=date.today())
    primernrotrn = IntegerField('Primer Numero de Transaccion', validators=[
        InputRequired(message="Este campo es obligatorio"),
        NumberRange(min=1)])
    ultimonrotrn = StringField('Ultimo Numero de Transaccion')
    id_version = SelectMultipleField('Version', coerce=int)
    tanques = FieldList(FormField(GenXmlTanquesCampos),min_entries = 0)
    recepciones = FieldList(FormField(GenXmlRecepcionesCampos),min_entries = 0)
    ventas = FieldList(FormField(GenXmlVentas), min_entries = 0)
    submit = SubmitField("Generar XML")
    
    