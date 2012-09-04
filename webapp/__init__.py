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
        super(GreaseTrapUI, self).__init__(name, static_folder="webapp/static", template_folder="webapp/templates")

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
        @self.route('/', methods=["GET"])
        def index():
            return render_template('index.html',
                                   clusters=url_for('clusters.index'),
                                   nodes=url_for('nodes.index'),
                                   roles=url_for('roles.index'),
                                   css=url_for('static', filename='site.css'))
  
        @self.errorhandler(StandardError)
        def special_exception_handler(error):
            error = "It appears that the Roush API has vanished. " + str(error)
            return render_template('exception.html', 
                                   clusters=url_for('clusters.index'),
                                   nodes=url_for('nodes.index'),
                                   roles=url_for('roles.index'),
                                   css=url_for('static', filename='site.css'),
                                   data=error)

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
        try:
            resp, content = conn.request(url, verb, data, headers)

        except StandardError, e:
            return str(e)

        return content

