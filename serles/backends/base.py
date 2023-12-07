# to implement your own backend, create a class Backend with a method
# sign(self,PEM_CSR,DN,[SAN],email) that returns (PEM_fullchain,error_or_None).

import base64
import csv
import requests
import secrets

from abc import ABC, abstractmethod


class Backend(ABC):
    """ Abstract Base Backend

    Inherit from this and implement ``sign()``, and optionally ``__init__()``
    to use this.
    """

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def sign(self, csr, subjectDN, subjectAltNames, email):
        pass
