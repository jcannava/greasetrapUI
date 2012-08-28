from ConfigParser import ConfigParser
from flask import Flask
from pprint import pprint
from clusters import clusters

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

        self.register_blueprint(clusters, url_prefix='/clusters')
        self.testing = True
        self.base_url = "http://%s:%d/" % ( 
                            self.config['main']['roush_address'], 
                            int(self.config['main']['roush_port']))

    def run(self):
        super(GreaseTrapUI, self).run(host=self.config['main']['bind_address'],
                                      port=self.config['main']['bind_port'])

    def build_request(url=None, verb=None, data=None):
        headers = {"Content-Type": "application/json"}
        conn = httplib2.Http()
        resp, content = conn.request(url, verb, data, headers)
        return content

    def templatify(htmlfile=None, action=None, extra=None, cluster_data=None, role_data=None):
        if htmlfile == 'cluster.html':
            return render_template(htmlfile,
                               clusters=url_for('clusters'),
                               nodes=url_for('nodes'),
                               roles=url_for('roles'),
                               css=url_for('static', filename='site.css'),
                               action=action,
                               data=extra)
        elif htmlfile == 'node.html':
            return render_template(htmlfile,
                               clusters=url_for('clusters'),
                               nodes=url_for('nodes'),
                               roles=url_for('roles'),
                               css=url_for('static', filename='site.css'),
                               action=action,
                               data=extra,
                               cluster_list=cluster_data,
                               role_list = role_data)
        elif htmlfile == 'role.html':
            return render_template(htmlfile,
                               clusters=url_for('clusters'),
                               nodes=url_for('nodes'),
                               roles=url_for('roles'),
                               css=url_for('static', filename='site.css'),
                               action=action,
                               data=extra)
        else:
            return render_template('index.html',
                               clusters=url_for('clusters'),
                               nodes=url_for('nodes'),
                               roles=url_for('roles'),
                               css=url_for('static', filename='site.css'))

