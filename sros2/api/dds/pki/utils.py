# Copyright 2017 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cryptography import hazmat, x509
# from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat
# from cryptography.hazmat.primitives.asymmetric import rsa, dsa, ec


def _dump_cert(cert, encoding=None):
    if encoding is None:
        encoding = Encoding.PEM
    return cert.public_bytes(encoding=encoding)


def save_cert(cert, cert_path, encoding=None):
    with open(cert_path, "wb") as f:
        f.write(_dump_cert(cert=cert, encoding=encoding))


def _dump_key(key, encoding=None, format=None, encryption_algorithm=None):
    if encoding is None:
        encoding = Encoding.PEM
    if format is None:
        format = PrivateFormat.PKCS8
    if encryption_algorithm is None:
        encryption_algorithm = serialization.NoEncryption()
    return key.private_bytes(encoding=encoding, format=format,
                             encryption_algorithm=encryption_algorithm)


def save_key(key, key_path, encoding=None, format=None, encryption_algorithm=None):
    with open(key_path, "wb") as f:
        f.write(_dump_key(key=key, encoding=encoding, format=format,
                          encryption_algorithm=encryption_algorithm))


def load_cert(cert_path, encoding=None, backend=None):
    if encoding is None:
        encoding = Encoding.PEM
    if backend is None:
        backend = default_backend()
    with open(cert_path, 'rb') as f:
        if encoding is Encoding.PEM:
            cert = x509.load_pem_x509_certificate(
                data=f.read(), backend=backend)
        elif encoding is Encoding.DER:
            cert = x509.load_der_x509_certificate(
                data=f.read(), backend=backend)
    return cert


def load_cert_data(cert_data, encoding=None, backend=None):
    if encoding is None:
        encoding = Encoding.PEM
    if backend is None:
        backend = default_backend()
    if encoding is Encoding.PEM:
        cert = x509.load_pem_x509_certificate(
            cert_data, backend=backend)
    elif encoding is Encoding.DER:
        cert = x509.load_der_x509_certificate(
            cert_data, backend=backend)
    return cert

def load_key(key_path, password=None, encoding=None, backend=None):
    if encoding is None:
        encoding = Encoding.PEM
    if backend is None:
        backend = default_backend()
    with open(key_path, 'rb') as f:
        if encoding is Encoding.PEM:
            key = serialization.load_pem_private_key(data=f.read(),
                                                     password=password,
                                                     backend=default_backend())
        elif encoding is Encoding.DER:
            key = serialization.load_der_private_key(data=f.read(),
                                                     password=password,
                                                     backend=default_backend())
    return key


def check_public_keys_match(keys):
    public_numbers = keys[0].public_key().public_numbers()
    match = all(key.public_key().public_numbers() == public_numbers for key in keys)
    return match
