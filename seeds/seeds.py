from website.authentication.models import Grupo, Usuario
from website.settings.models import Producto, Version
from flask_seeder import Seeder


def create_groups(self):
  admin = Grupo(nombre='Administradores',descripcion='Grupo de administradores, perfil con acceso a todos los menus.',creado_por=1)
  self.db.session.add(admin)
  self.db.session.commit()

def create_user_admin(self):
  grupo = Grupo.query.filter_by(nombre='Administradores').first()
  admin = Usuario(nombre="Administrador",email='admin@mail.com',username='Admin',full_name='ADMINISTRADOR',password=str(1234),id_grupo=grupo.id,creado_por=1)
  self.db.session.add(admin)
  self.db.session
  self.db.session.commit()
  
def create_products(self):
    magna = Producto(nombre='GASOLINA CONTENIDO MINIMO 87 OCTANO',claveProductoPEMEX='32011',nombre_corto='Magna',claveProducto='07',claveSubProducto='1',creado_por=1)
    premium = Producto(nombre='GASOLINA CONTENIDO MINIMO 92 OCTANO',claveProductoPEMEX='32012',nombre_corto='Premium',claveProducto='07',claveSubProducto='2',creado_por=1)
    diesel = Producto(nombre='DIESEL AUTOMOTRIZ',claveProductoPEMEX='34006',claveProducto='03',nombre_corto='Diesel',claveSubProducto='3',creado_por=1)
    self.db.session.add(magna)
    self.db.session.add(premium)
    self.db.session.add(diesel)
    self.db.session.commit()
    

def create_version(self):
    version_1 = Version(nombre="1.1", creado_por=1)
    version_2 = Version(nombre="1.2", creado_por=1)
    version_3 = Version(nombre="1.3", creado_por=1)
    self.db.session.add(version_1)
    self.db.session.add(version_2)
    self.db.session.add(version_3)
    self.db.session.commit() 
    
# All seeders inherit from Seeder
class DemoSeeder(Seeder):
  # run() will be called by Flask-Seeder
  def run(self):
    create_groups(self)
    create_user_admin(self)
    create_products(self)
    create_version(self)
