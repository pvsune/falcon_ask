# Falcon-Ask
Minimal Python3 toolkit to create Amazon Alexa skills with [Falcon](https://falconframework.org/). 

Builds on top of Alexa Skills Kit (ASK) to bootstrap boilerplate code so you don't have to!

Inspired by [Flask-Ask](https://github.com/johnwheeler/flask-ask) and [Alexandra](https://github.com/erik/alexandra).

# Synopsis
A Falcon app might look like this.
```python
import falcon
from falcon_ask import dispatch_request, FalconAskMiddleware, respond

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

# Installation
We are not yet in PyPI, so for now we can install via GitHub!
```bash
pip install git+https://github.com/pvsune/falcon_ask.git
```
