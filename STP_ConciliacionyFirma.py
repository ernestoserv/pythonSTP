import base64
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import requests


def sign(cadena, ruta):
    with open(ruta, 'rb') as f:
        llave = RSA.import_key(f.read())

    # Calcular el hash SHA256 de la cadena
    hash = SHA256.new(cadena.encode('utf-8'))

    # Firmar el hash con la llave privada RSA
    firma = pkcs1_15.new(llave).sign(hash)

    # Codificar la firma en base64
    signature_b64 = base64.b64encode(firma).decode('utf-8')

    return signature_b64


cadena = "||CLUB_DE_RENTAS|E|||"
ruta = "/Users/claudiaeenriquezgracia/Documents/STP/llave_privada_cdr.pem"
# password = "#cdr1234"
resultado = sign(cadena, ruta)
#print(resultado)
url = "https://prod.stpmex.com:7002/efws/API/V2/conciliacion"
headers = {
    "Content-Type": "application/json",
    "Encoding": "UTF-8"
}
data = {
    "empresa": "CLUB_DE_RENTAS",
    "page": 0,
    "tipoOrden": "E",
    "firma": resultado,  # firma_encirptada
}

respuesta_stp = requests.post(url, headers=headers, json=data)
print(respuesta_stp.text)
