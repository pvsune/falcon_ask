import json
import logging

import falcon


logger = logging.getLogger(__name__)


def _get_json_body(req):
    # req.stream corresponds to the WSGI wsgi.input environ variable,
    # and allows you to read bytes from the request body.
    #
    # See also: PEP 3333
    if req.content_length in (None, 0):
        # Nothing to do
        return None

    body = req.stream.read()
    if not body:
        raise falcon.HTTPBadRequest(
            'Empty request body',
            'A valid JSON document is required.'
        )

    try:
        data = json.loads(body.decode('utf-8'))
        req.context['doc'] = data
        req.context['raw_body'] = body
        return data
    except (ValueError, UnicodeDecodeError):
        raise falcon.HTTPError(
           falcon.HTTP_753,
           'Malformed JSON',
           'Could not decode the request body. The '
           'JSON was incorrect or not encoded as '
           'UTF-8.'
        )


def get_req_type(body):
    return body.get('request', {}).get('type')


def get_slots(body):
    if get_req_type(body) != 'IntentRequest':
        return {}

    slots = body['request']['intent'].get('slots', {})
    return {item['name']: item.get('value') for _, item in slots.items()}


def dispatch_request(req):
    # Check if req.stream is consumed, otherwise get POST data.
    body = req.context.get('doc') or _get_json_body(req)
    logger.debug('Got body: %s' % body)

    req_type = get_req_type(body)
    intent_maps = req.context['intent_maps']

    if req_type == 'LaunchRequest':
        return req.context['welcome']
    elif req_type == 'IntentRequest':
        intent = body['request']['intent']['name']
        try:
            intent_fn = intent_maps[intent]
        except KeyError:
            logger.exception(
                'No intent function mapping found for intent: %s' % intent
            )
            try:
                intent_fn = intent_maps['UnknownIntent']
            except KeyError:
                logger.exception('UnknownIntent mapping also not found.')
                raise falcon.HTTPInternalServerError()
        return intent_fn(body)
    elif req_type == 'SessionEndedRequest':
        logger.info('SessionEndedRequest received. Session ended.')
        return None

    logger.error('Invalid request type: %s', req_type)
    raise falcon.HTTPBadRequest()


def respond(text=None, ssml=None, attributes=None, reprompt_text=None,
            reprompt_ssml=None, end_session=True, directives=None):
    obj = {
        'version': '1.0',
        'response': {
            'shouldEndSession': end_session
        },
        'sessionAttributes': attributes or {}
    }

    if text:
        obj['response']['outputSpeech'] = {'type': 'PlainText', 'text': text}
    elif ssml:
        obj['response']['outputSpeech'] = {'type': 'SSML', 'ssml': ssml}

    reprompt_output = None
    if reprompt_text:
        reprompt_output = {'type': 'PlainText', 'text': reprompt_text}
    elif reprompt_ssml:
        reprompt_output = {'type': 'SSML', 'ssml': reprompt_ssml}

    if reprompt_output:
        obj['response']['reprompt'] = {'outputSpeech': reprompt_output}

    obj['response']['directives'] = directives or []

    return obj
