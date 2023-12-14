import requests
import secrets
import json

from cryptography import x509  # python3-cryptography.x86_64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs7
from cryptography.hazmat.backends import default_backend as x509_backend

class AdcsToRestBackend:
    """ Serles Backend for AdcsToRest"""

    def __init__(self, config):
        print("init")
        try:
            self.apiUrl = config["adcstorest"]["apiUrl"]
            self.apiUsername = config["adcstorest"]["apiUsername"]
            self.apiPassword = config["adcstorest"]["apiPassword"]
            self.apiCertificateTemplate = config["adcstorest"]["apiCertificateTemplate"]
            caBundle = config["adcstorest"]["caBundle"]
            self.caBundle = dict(default=True, none=False).get(caBundle, caBundle)
        except KeyError as e:
            raise Exception(f"missing config key {e}") 
        
    def sign(self, csr, subjectDN, subjectAltNames, email):
        print("sign:", self, csr, subjectDN, subjectAltNames, email)
        #subjectAltName = ",".join(f"DNSNAME={name}" for name in subjectAltNames)

        #read csr object and prepare as string for API POST request
        csr_obj = x509.load_pem_x509_csr(csr)
        csr_pem = csr_obj.public_bytes(serialization.Encoding.PEM)
        csr_string = csr_pem.decode()

        try:
            response = requests.post(
                self.apiUrl,
                json={
                    "Request": csr_string,
                    "RequestAttributes": ["CertificateTemplate:" + self.apiCertificateTemplate]
                },
                headers={"Content-Type": "application/json"},
                auth=(self.apiUsername, self.apiPassword),
                verify=self.caBundle
            )
        except ConnectionError as e:
            print(f"Connection error: {e}")
            return None, f"Connection error: {e}"
        except Exception as e:
             print(f"Unexpected error: {e}")
             return None, f"Unexpected error: {e}"
        

        print(response.status_code)
        resultjson = response.json()

        print(f"'requestId: {resultjson['requestId']}, 'disposition': {resultjson['disposition']}, 'status': {resultjson['status']}")

        try:
            if(response.status_code == 200):
                
                certchain = resultjson['certificate']
                #result should contain certificate in pkcs7 string when successfully issued
                begin = '-----BEGIN PKCS #7 SIGNED DATA-----\n'
                end = '\n-----END PKCS #7 SIGNED DATA-----'

                #for encoding to work, begin and end string with linebreaks must be added to the returned pkcs7 string from AdcsToRest API
                return pkcs7_to_pem_chain((begin + certchain + end).encode()), None
            else:
                return None, f"Error: 'requestId: {resultjson['requestId']}, 'disposition': {resultjson['disposition']}, 'status': {resultjson['status']}"
        except Exception as e:
            message = e.message
            print("Exception Error:", message)
            return None, message   
    
def pkcs7_to_pem_chain(pkcs7_input):
    """ Converts a PKCS#7 cert chain to PEM format.
    Args:
        pkcs7_input (bytes): the PKCS#7 chain as stored in the database.
    Returns:
        str: PEM encoded certificate chain as expected by ACME clients.
    """
    certs = pkcs7.load_pem_pkcs7_certificates(pkcs7_input)
    return "\n".join(
        [
            cert.public_bytes(serialization.Encoding.PEM).decode("ascii")
            for cert in certs
        ]
    )