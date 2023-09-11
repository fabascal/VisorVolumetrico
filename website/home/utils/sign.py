from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import Encoding
import base64
import os
from flask import current_app



def signDoc(cadena_original, pem_file_path):
    formatted_cadena = "||" + "|".join(cadena_original) + "||"
    # Leer la clave privada desde el archivo key
    #with open('llave_pem.key', 'rb') as key_file:
    with open(os.path.join(current_app.config['UPLOAD_FOLDER'], pem_file_path), 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    # Firmar la cadena original con la clave privada
    signature = private_key.sign(
        formatted_cadena.encode('utf-8'),
        padding.PKCS1v15(),
        hashes.SHA1()
    )

    # Convertir la firma a base64
    #sellodigital = base64.b64encode(signature)
    sellodigital = base64.b64encode(signature).decode('utf-8')
    
    return sellodigital

