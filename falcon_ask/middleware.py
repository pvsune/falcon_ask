import base64
import json
import logging
import os.path
from datetime import datetime
from urllib.parse import urlparse
from urllib.request import urlopen

import falcon
from OpenSSL import crypto

from . import util


logger = logging.getLogger(__name__)
cert_cache = {}


class FalconAskMiddleware(object):
    """Alexa Skill Kit Middleware."""

    def __init__(self, resource, validate=True):
        self.resource = resource
        self.validate = validate

    def _get_certificate(self, cert_url):
        global cert_cache
        if cert_url in cert_cache:
            cert = cert_cache[cert_url]
            if not cert.has_expired():
                return cert
            cert_cache = {}

        # Sanity check location so we don't get some random person's cert.
        url = urlparse(cert_url)
        host = url.netloc.lower()
        path = os.path.normpath(url.path)
        if url.scheme != 'https' or \
                host not in ['s3.amazonaws.com', 's3.amazonaws.com:443'] or \
                not path.startswith('/echo.api/'):
            logger.error('Invalid certificate location: %s.', cert_url)
            return None

        resp = urlopen(cert_url)
        if resp.getcode() != 200:
            logger.error('Failed to download certificate.')
            return None

        cert = crypto.load_certificate(crypto.FILETYPE_PEM, resp.read())

        if cert.has_expired() or \
                cert.get_subject().CN != 'echo-api.amazon.com':
            logger.error('Certificate expired or invalid.')
            return None

        cert_cache[cert_url] = cert
        return cert

    def validate_request_certificate(self, req, body):
        cert_url = req.get_header('SignatureCertChainUrl', required=True)
        sig = base64.b64decode(req.get_header('Signature', required=True))

        # FU Bezos ¯\_(ツ)_/¯
        cert = self._get_certificate(cert_url)
        if not cert:
            return False

        data = req.context['raw_body']
        try:
            crypto.verify(cert, sig, data, 'sha1')
            return True
        except Exception:
            logger.exception('Invalid request signature.')
            return False

    def validate_request_timestamp(self, body, max_diff=150):
        time_str = body.get('request', {}).get('timestamp')
        if not time_str:
            logger.error('Timestamp not found: %s', body)
            return False

        req_ts = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
        diff = (datetime.utcnow() - req_ts).total_seconds()
        if abs(diff) > max_diff:
            logger.error('Timestamp difference too high: %d sec', diff)
            return False

        return True

    def process_resource(self, req, resp, resource, params):
        if not isinstance(resource, self.resource):
            return

        allowed_methods = ['POST']
        if req.method not in allowed_methods:
            raise falcon.HTTPMethodNotAllowed(allowed_methods)

        # TODO: Validate application ID if intended for this service.

        if self.validate:
            body = req.context.get('doc') or util._get_json_body(req)
            valid_cert = self.validate_request_certificate(req, body)
            valid_ts = self.validate_request_timestamp(body)
            if not valid_cert or not valid_ts:
                logger.error('Failed to validate request.')
                raise falcon.HTTPForbidden()

        welcome = getattr(resource, 'welcome', None)
        req.context['welcome'] = welcome

        intent_maps = getattr(resource, 'intent_maps', None)
        if intent_maps is None:
            logger.error('Missing attribute "intent_maps" in resource.')
            raise falcon.HTTPInternalServerError()
        req.context['intent_maps'] = intent_maps

    def process_response(self, req, resp, resource, req_succeeded):
        """Always return valid json response.

        If resp.body is not valid json, e.g. string, do respond properly.
        """
        body = json.loads(resp.body or '{}')
        if type(body) == str:
            # Safer not to end sesion.
            response = util.respond(body, end_session=False)
            resp.body = json.dumps(response)
