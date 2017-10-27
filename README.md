# Falcon-Ask [![Build Status](https://travis-ci.org/pvsune/falcon_ask.svg?branch=master)](https://travis-ci.org/pvsune/falcon_ask)
Minimal Python3 toolkit to create Amazon Alexa skills with [Falcon](https://falconframework.org/). 

Builds on top of [Alexa Skills Kit (ASK)](https://developer.amazon.com/docs/ask-overviews/build-skills-with-the-alexa-skills-kit.html) to bootstrap boilerplate code so you don't have to!

Inspired by [Flask-Ask](https://github.com/johnwheeler/flask-ask) and [Alexandra](https://github.com/erik/alexandra).

# Synopsis
A Falcon app might look like this.
```python
import falcon
from falcon_ask import dispatch_request, FalconAskMiddleware, respond


def intent_fn(body):
    # "body" contains request POST data.
    return "Hello, here's a useless skill I can do for you: Hello, World!"


class AlexaResource(object):
    intent_maps = {
        'WhateverIntent': intent_fn
    }
    welcome = 'Hi, welcome to my alexa skill.'
    
    def on_post(self, req, resp):
        response = dispatch_request(req)
        return respond(response)


app = falcon.API(middleware=[FalconAskMiddleware(AlexaResource)])
app.add_route('/alexa', AlexaResource())
```
Save above code to `alexa.py` and run via `$ gunicorn alexa:app`. Make sure [gunicorn](http://gunicorn.org/) is installed.

# Installation
We are not yet in [PyPI](https://pypi.python.org/pypi), so for now we can install via  :smiling_imp: :octocat: :octocat: :octocat: :smiling_imp:!
```bash
$ pip install git+https://github.com/pvsune/falcon_ask.git
```
