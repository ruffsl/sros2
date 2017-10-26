# Copyright 2015 Open Source Robotics Foundation, Inc.
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

# Stuck with M2Crypto until somthing better comes along
# https://github.com/pyca/cryptography/issues/1621

import logging
from M2Crypto import BIO, SMIME, X509

from cryptography.hazmat.primitives.serialization import Encoding

from sros2keystore.api.dds import pki


class BadPKCS7Format(BaseException):
    pass


class BadKeySource(BaseException):
    pass


class MissingSignerCertificate(BaseException):
    pass


def _load_store(cert_store, certs, source_type, source_format=None):
    if source_format is None:
        source_format = X509.FORMAT_PEM
    if source_format is 'PEM':
        source_format = X509.FORMAT_PEM
    if source_format is 'DER':
        source_format = X509.FORMAT_DER
    if source_type is 'file':
        for cert in certs:
            cert_store.add_cert(X509.load_cert(
                file=cert, format=source_format))
    elif source_type is 'bio':
        for cert in certs:
            cert_store.add_cert(X509.load_cert_bio(
                bio=cert, format=source_format))
    elif source_type is 'pkcs11':
        for cert in certs:
            cert_store.add_cert(cert)
    else:
        msg = 'unknown source type: ' + source_type + \
            '; possible values: file, bio, pkcs11'
        logging.error(msg=msg)
        raise BadKeySource(msg)


def _verify_data(data_path, certs, source_type='file', source_format='PEM'):

    smime = SMIME.SMIME()
    cert_store = X509.X509_Store()
    _load_store(cert_store=cert_store, certs=certs,
                source_type=source_type, source_format=source_format)
    smime.set_x509_store(cert_store)
    data_bio = None

    with open(data_path, mode='rb') as data_fd:
        p7_bio = BIO.MemoryBuffer(data=data_fd.read())
        try:
            if source_format == 'PEM':
                pkcs7, data_bio = SMIME.smime_load_pkcs7_bio(p7_bio)
            # elif source_format == 'DER':
            #     pkcs7 = SMIME.PKCS7(m2.pkcs7_read_bio_der(
            #         p7_bio._ptr()), X509.FORMAT_DER)
            else:
                msg = 'unknown format: ' + source_format + \
                    '; possible formats: PEM, DER'
                logging.error(msg='pkcs7 format error: unknown format')
                raise BadPKCS7Format(msg)
        except SMIME.SMIME_Error as e:
            logging.error('load pkcs7 error: ' + str(e))
            raise

        if data_bio is not None:
            data = data_bio.read()
            data_bio = BIO.MemoryBuffer(bytes(data))

        cert_stack = pkcs7.get0_signers(X509.X509_Stack())
        if len(cert_stack) == 0:
            logging.error('missing certificate')
            raise MissingSignerCertificate('missing certificate')
        signer_certs = []
        for cert in cert_stack:
            signer_certs.append(cert)
        smime.set_x509_stack(cert_stack)
        v = None
        try:
            v = smime.verify(pkcs7=pkcs7, data_bio=data_bio)
        except SMIME.SMIME_Error as e:
            logging.error('smime error: ' + str(e))
            raise
        except SMIME.PKCS7_Error as e:
            logging.error('pkcs7 error: ' + str(e))
            raise
        if (data_bio is not None) and (data != v) and (v is not None):
            return
        return signer_certs


def verify_file(file_path, certs, source_format='PEM'):
    if source_format is 'PEM':
        encoding = Encoding.PEM
    if source_format is 'DER':
        encoding = Encoding.DER
    cert_bios = []
    for cert in certs:
        cert_dump = pki.utils._dump_cert(cert=cert, encoding=encoding)
        cert_bio = BIO.MemoryBuffer(data=cert_dump)
        cert_bios.append(cert_bio)
    raw_signed_certs = []
    raw_signed_certs = _verify_data(
        data_path=file_path, certs=cert_bios, source_type='bio', source_format=source_format)

    signed_certs = []
    for cert in raw_signed_certs:
        # FIXME importing both M2Crypto and cryptography results in flaky segfaults?
        # the X509 function as_pem() seems to be the issue
        # when not segfaulting, PEM cert is much too short and invalid
        # could be an upstream issue in _verify_data
        cert = cert.as_pem()
        signed_certs.append(pki.utils.load_cert_data(cert))

    return signed_certs
