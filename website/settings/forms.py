from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, BooleanField, SelectMultipleField, Form, SelectField, FileField, IntegerField, StringField
from wtforms.validators import Email, DataRequired
from wtforms.fields import FieldList, FormField
from flask_wtf.file import FileRequired, FileAllowed


class TanquesForm(FlaskForm):
    id_estacion = SelectMultipleField('Estación', coerce=int)
    id_producto = SelectMultipleField('Producto', coerce=int)
    no_tanque = TextField('Numero tanque', validators=[DataRequired()])
    volumenUtil = TextField('Volumen Util',validators=[DataRequired()])
    volumenFondaje = TextField('Volumen Fondaje',validators=[DataRequired()])
    volumenAgua = TextField('Volumen Agua',validators=[DataRequired()])
    volumenDisponible = TextField('Volumen Disponible',validators=[DataRequired()])
    volumenExtraccion = TextField('Volumen Extraccion',validators=[DataRequired()])
    volumenRecepcion = TextField('Volumen Recepcion',validators=[DataRequired()])
    temperatura = TextField('Temperatura',validators=[DataRequired()])
    activo = BooleanField('Activo:', default=True)
    submit = SubmitField("Guardar")
    
class ProductosForm(FlaskForm):
    nombre = TextField('Nombre comercial', validators=[DataRequired()])
    nombre_corto = TextField('Nombre corto', validators=[DataRequired()])
    claveProducto = TextField('Clave producto', validators=[DataRequired()])
    claveSubProducto = TextField('Clave sub-producto', validators=[DataRequired()])
    composicionOctanajeDeGasolina = TextField('Octanaje', validators=[])
    gasolinaConEtanol = TextField('Gasolina con etanol', validators=[])
    claveProductoPEMEX = TextField('Clave producto PEMEX', validators=[DataRequired()])
    submit = SubmitField("Guardar")
    
class MangueraForm(Form):
    identificadorManguera = TextField('Numero Manguera', validators=[DataRequired()])
    id_producto = SelectField('Producto', coerce=int)
    
    
class DispensariosForm(FlaskForm):
    numeroDispensario = TextField('Numero Dispensario', validators=[DataRequired()])
    id_estacion = SelectField('Estación', coerce=int)
    mangueras = FieldList(FormField(MangueraForm), min_entries = 0)
    submit = SubmitField("Guardar")
    
class EstacionTanquesForm(Form):
    no_tanque = TextField('Numero tanque', validators=[DataRequired()])
    producto = StringField('Producto', render_kw={'readonly': True})
    volumenUtil = StringField('Volumen Util')
    volumenDisponible = StringField('Volumen Disponible')
    

class EstacionForm(FlaskForm):
    nombre = TextField('Estacion', validators=[DataRequired()])
    id_zona = SelectMultipleField('Zona', coerce=int)
    numeroPermisoCRE = TextField('Numero Permiso CRE', validators=[DataRequired()])
    id_empresa = SelectMultipleField('Empresa', coerce=int)
    id_producto = SelectMultipleField('Productos', coerce=int)
    activo = BooleanField('Activo:', default=True)
    ruta = TextField('Ruta SFTP', validators=[DataRequired()])
    claveClientePEMEX = TextField('Clave Cliente Pemex', validators=[DataRequired()])
    claveEstacionServicio = TextField('Clave Estacion Servicio', validators=[DataRequired()])

    # Agregamos validadores para garantizar que se carguen los archivos y que sean de la extensión adecuada
    key_file = FileField('Archivo Key', validators=[FileAllowed(['key'], 'Solo archivos .key permitidos!')])
    cer_file = FileField('Archivo Cer', validators=[FileAllowed(['cer'], 'Solo archivos .cer permitidos!')])
    pem_file = FileField('Archivo Pem', validators=[FileAllowed(['pem'], 'Solo archivos .pem permitidos!')])
    
    noCertificado = TextField('Numero de Certificado')
    certificado_value = TextField('Valor de Certificado')

    tanques = FieldList(FormField(EstacionTanquesForm),min_entries = 0)
    submit = SubmitField("Guardar")
    
