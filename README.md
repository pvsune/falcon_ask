# Falcon-Ask [![Build Status](https://travis-ci.org/pvsune/falcon_ask.svg?branch=master)](https://travis-ci.org/pvsune/falcon_ask)
Minimal Python3 toolkit to create Amazon Alexa skills with [Falcon](https://falconframework.org/).

Builds on top of [Alexa Skills Kit (ASK)](https://developer.amazon.com/docs/ask-overviews/build-skills-with-the-alexa-skills-kit.html) to bootstrap boilerplate code so you don't have to!

Inspired by [Flask-Ask](https://github.com/johnwheeler/flask-ask) and [Alexandra](https://github.com/erik/alexandra).

# Synopsis
A Falcon app might look like this.
```python
import json

import falcon
from falcon_ask import dispatch_request, FalconAskMiddleware, respond


def intent_fn(body):
    # "body" contains request POST data.
    return 'Congratulations! Your new alexa skill works great.'


class AlexaResource(object):
    # Dictionary mapping of "IntentRequest" to function.
    intent_maps = {
        'GreetingIntent': intent_fn,
    }

    # Message to return when "LaunchRequest" is received.
    welcome = 'Hi, welcome to your new alexa skill.'

    def on_post(self, req, resp):
        response = dispatch_request(req)
        resp.body = json.dumps(respond(response, end_session=False))


app = falcon.API(middleware=[
    # Do validation of request certificate and timestamp.
    FalconAskMiddleware(AlexaResource, validate=True),
])
app.add_route('/', AlexaResource())
```
Save above code to `alexa.py` and run via `$ gunicorn alexa:app`. Make sure [gunicorn](http://gunicorn.org/) is installed.

# Installation
To install Falcon-Ask, simply use [pipenv](http://pipenv.org/) (or pip, of
course):

```bash
$ pip install falcon-ask
✨🍰✨
```

Satisfaction guaranteed.
# Thank You
Thanks for checking this library out! I hope you find it useful.

Of course, there's always room for improvement. Feel free to open an issue so we can make Falcon-Ask better.

Special thanks to [@muxspace](https://github.com/muxspace) for giving me an Echo Dot.
