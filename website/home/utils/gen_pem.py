from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from werkzeug.utils import secure_filename
import os
from flask import current_app
import base64

def GenPem(der_key_path_fragment, name):
    # Cargar la clave privada desde el formato DER en formato PKCS8
    full_der_key_path = os.path.join(current_app.config['UPLOAD_FOLDER'], der_key_path_fragment)
    with open(full_der_key_path, 'rb') as key_file:
        der_key_data = key_file.read()
    private_key = serialization.load_der_private_key(
        der_key_data,
        password='COMBU-EXPRESS'.encode(),
        backend=default_backend()
    )

    # Guardar la clave privada en formato PEM
    pem_key_data = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,  # Usar este formato
        encryption_algorithm=serialization.NoEncryption()  # No se encripta
    )

    # Si pem_key_data tiene contenido, guardamos en un archivo
    pem_content = None
    if pem_key_data:
        pem_filename = secure_filename(name + ".pem")
        station_directory = os.path.join(current_app.config['UPLOAD_FOLDER'], name)
        pem_file_path = os.path.join(station_directory, pem_filename)
        
        # Escribir la clave PEM en un archivo
        with open(pem_file_path, 'wb') as pem_file:
            pem_file.write(pem_key_data)
        # Leer el contenido del archivo PEM y retornarlo
        with open(pem_file_path, 'rb') as pem_file:
            pem_content = pem_file.read()
            
    return pem_content
