from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding
import os
from flask import current_app


def CerData(cer_file_path):
    # Leer el archivo .cer
    with open(cer_file_path, "rb") as f:
        cert_data = f.read()

    # Cargar el certificado en formato DER
    cert = x509.load_der_x509_certificate(cert_data, default_backend())

    # Convertir el certificado a formato PEM
    pem_data = cert.public_bytes(Encoding.PEM).decode('utf-8')  # Convertir a string

    # Extraer el contenido sin encabezados ni pies de página
    lines = pem_data.strip().splitlines()
    content = ''.join(lines[1:-1])

    return content