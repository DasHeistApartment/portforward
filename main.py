import os
from flask import Flask
import urllib.request
import json
import portforwardlib

configurationUrl = os.environ['CONFIG_URL']
port = os.environ['WEBSERVER_PORT']
host = os.environ['WEBSERVER_HOST']

app = Flask(__name__)

@app.route('/portforward/update')
def update_port_forwardings():
    response = ''
    page = urllib.request.urlopen(configurationUrl)
    config = json.load(page)
    for e in config:
        external_port = e['external']
        internal_port = e['internal']
        if not (external_port and internal_port):
            continue
        protocol = 'TCP'
        if e['protocol']:
            protocol = e['protocol']
        description = None
        if e['description']:
            description = e['description']
        result = portforwardlib.forwardPort(external_port, internal_port, router = None, lanip = None, disable = False, protocol = protocol, time = 0, description = description, verbose = True)
        if not result:
            response += 'Failed to forward port %d to %d.'%(external_port, internal_port)
    return response

if __name__ == '__main__':
    app.run(port = port, host = host)
