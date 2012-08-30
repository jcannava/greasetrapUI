from ConfigParser import ConfigParser
from flask import Flask, render_template, url_for
from pprint import pprint
from clusters import clusters
from nodes import nodes
from roles import roles

import logging
import json
import httplib2

class GreaseTrapUI(Flask):
    def __init__(self, name, configFile=None, configHash=None, debug=False):
        super(GreaseTrapUI, self).__init__(name)

        defaults = {'main':
                { 'bind_address': '0.0.0.0',
                  'bind_port': '8081',
                  'roush_address': '127.0.0.1',
                  'roush_port': '8080',
                  'loglevel': 'WARNING'}}

        if configFile:
            config = ConfigParser()
            config.readfp(open(configFile))

            defaults.update(
                dict([(s, dict(config.items(s))) for s in config.sections()]))
            self.config.update(defaults)

        LOG = logging.getLogger()

        if debug:
            LOG.setLevel(logging.DEBUG)
        else: 
            LOG.setLevel(logging.WARNING)

        if 'logfile' in defaults['main']:
            for handler in LOG.handlers:
                LOG.removeHandler(handler)

            handler = logging.FileHandler(defaults['main']['logfile'])
            LOG.addHandler(handler)

        if 'loglevel' in defaults['main']:
            LOG.setLevel(defaults['main']['loglevel'])

        # Register Blueprints
        self.register_blueprint(clusters, url_prefix='/clusters')
        self.register_blueprint(nodes, url_prefix='/nodes')
        self.register_blueprint(roles, url_prefix='/roles')
        self.testing = True
        
        # Set globals
        self.base_url = "http://%s:%d/" % ( 
                            self.config['main']['roush_address'], 
                            int(self.config['main']['roush_port']))

    def run(self):
        super(GreaseTrapUI, self).run(host=self.config['main']['bind_address'],
                                      port=self.config['main']['bind_port'])

    def build_request(self, url=None, verb=None, data=None):
        headers = {"Content-Type": "application/json"}
        conn = httplib2.Http()
        resp, content = conn.request(url, verb, data, headers)
        return content
