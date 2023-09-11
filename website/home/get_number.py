import random
from website.settings.models import Dispensario, Manguera
import itertools
from website.home.utils.gen_hour import call_generar_horas


def get_number(data, estacion):
    servicios_dict = []
    for index, venta in data['ventas'].items():
        suma = 0
        dispensario_aleatorio = None
        manguera = None
        while suma < float(venta['litros']):
            dispensarios = Dispensario.query.filter_by(id_estacion=estacion).all()
            if dispensarios:
                dispensario_aleatorio = random.choice(dispensarios)
                manguera = Manguera.query.filter_by(id_dispensario=dispensario_aleatorio.id,id_producto=venta['id_producto']).fisrt()
            data['ultnrotrn'] += 1
            litro = round(random.uniform(2, 75), 2)
            servicio = {
                "tipoDeRegistro" : "D",
                "numeroUnicoTransaccionVenta" : data['ultnrotrn'],
                "numeroDispensario" : dispensario_aleatorio.numeroDispensario if dispensario_aleatorio else None,
                "identificadorManguera" : manguera.identificadorManguera if manguera else None,
                "claveProductoPEMEX" : venta['claveProductoPEMEX'],
                "volumenDespachado": litro,
                "precioUnitarioProducto" : venta['precio'],
                "importeTotalTransaccion" : litro * venta['precio'] 
            }
            servicios_dict.append(servicio)
            suma += litro
    return servicios_dict


def generate_sales_data(data):
    ventas_data = data['ventas']
    servicios_dict = {indice: [] for indice in ventas_data}
    indices = list(ventas_data.keys())  # Lista de claves de productos de la estacion, los indices del arreglo 
    ultnrotrn = int(data['primernrotrn']) #Numero de transaccion a partir del que se iniciara la secuencia
    
    while len(indices) > 0:
        ultnrotrn += 1
        indice_actual = random.choice(indices)  # Seleccionar un producto aleatorio
        venta = ventas_data[indice_actual]
        litros_objetivo = float(venta['litros'])
        if sum(d['volumenDespachado'] for d in servicios_dict[indice_actual]) < litros_objetivo :
            dispensarios_estacion = Dispensario.query.filter_by(id_estacion=data['id_estacion']).all()
            id_dispensarios = [dispensario.id for dispensario in dispensarios_estacion]
            manguera = Manguera.query.filter(Manguera.id_producto == venta['id_producto'], Manguera.id_Dispensario.in_(id_dispensarios)).all()
            manguera_random = random.choice(manguera)
            dispensario = Dispensario.query.filter_by(id=manguera_random.id_Dispensario).first()
            if venta['claveProductoPEMEX'] == '34006':
                litro = round(random.uniform(30, 150), 4)
            else:
                litro = round(random.uniform(1, 75), 4)
            servicio = {
                "tipoDeRegistro" : "D",
                "numeroUnicoTransaccionVenta" : ultnrotrn,
                "numeroDispensario" : dispensario.numeroDispensario,
                "identificadorManguera" : manguera_random.identificadorManguera,
                "claveProductoPEMEX" : venta['claveProductoPEMEX'],
                "volumenDespachado": litro,
                "precioUnitarioProducto" : venta['precio'],
                "importeTotalTransaccion" : round(litro * float(venta['precio']),2)
            }
            servicios_dict[indice_actual].append(servicio)
            
        else:
            indices.remove(indice_actual)

    # Unir los diccionarios internos en uno solo
    merged_data = []
    for lista in servicios_dict.values():
        merged_data.extend(lista)
    # Ordenar el diccionario resultante por clave 'numeroUnicoTransaccionVenta'
    merged_data.sort(key=lambda x: x['numeroUnicoTransaccionVenta'])
    print("="*20+"Merged Data"+"="*20)
    print(merged_data)
    full_data = call_generar_horas(merged_data,data['fecha'])
    return full_data


def generate_sales_data_ner(data):
    ventas_data = data['ventas']
    servicios_dict = {indice: [] for indice in ventas_data}
    indices = list(ventas_data.keys())
    ultimonrotrn = int(data['ultimonrotrn'])
    
    while len(indices) > 0:
        primernrotrn = int(data['primernrotrn'])
        ultimonrotrn = int(data['ultimonrotrn'])
        ultnrotrn = random.randint(primernrotrn, ultimonrotrn)
        
        indice_actual = random.choice(indices)
        venta = ventas_data[indice_actual]
        litros_objetivo = float(venta['litros'])
        
        litros_despachados = sum(d['volumenDespachado'] for d in servicios_dict[indice_actual])
        litros_restantes = litros_objetivo - litros_despachados
        
        if litros_restantes > 0:
            dispensarios_estacion = Dispensario.query.filter_by(id_estacion=data['id_estacion']).all()
            id_dispensarios = [dispensario.id for dispensario in dispensarios_estacion]
            manguera = Manguera.query.filter(Manguera.id_producto == venta['id_producto'], Manguera.id_Dispensario.in_(id_dispensarios)).all()
            manguera_random = random.choice(manguera)
            dispensario = Dispensario.query.filter_by(id=manguera_random.id_Dispensario).first()
            
            if venta['claveProductoPEMEX'] == '34006':
                litro = round(random.uniform(30, min(150, litros_restantes)), 4)
            else:
                litro = round(random.uniform(1, min(75, litros_restantes)), 4)
            
            servicio = {
                "tipoDeRegistro": "D",
                "numeroUnicoTransaccionVenta": ultnrotrn,
                "numeroDispensario": dispensario.numeroDispensario,
                "identificadorManguera": manguera_random.identificadorManguera,
                "claveProductoPEMEX": venta['claveProductoPEMEX'],
                "volumenDespachado": litro,
                "precioUnitarioProducto": venta['precio'],
                "importeTotalTransaccion": round(litro * float(venta['precio']), 2)
            }
            servicios_dict[indice_actual].append(servicio)
            
        else:
            indices.remove(indice_actual)

    # Unir los diccionarios internos en uno solo
    merged_data = []
    for lista in servicios_dict.values():
        merged_data.extend(lista)
    # Ordenar el diccionario resultante por clave 'numeroUnicoTransaccionVenta'
    merged_data.sort(key=lambda x: x['numeroUnicoTransaccionVenta'])
    return merged_data
