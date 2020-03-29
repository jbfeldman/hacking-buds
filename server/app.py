#!flask/bin/python
from flask import Flask, jsonify, request
import logging
import logging.handlers
from logging.handlers import RotatingFileHandler
import json
from flask_cors import CORS, cross_origin


DEFAULT_LIST = [
    {'phrase': 'Jathan', 'reason': "He's a scary dude"},
    {'phrase': 'Hande', 'reason': 'she said some mean things once'},
    {'phrase': 'Julius', 'reason': 'Swedish; yet speaks with British accent?'}

    ]
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler('/home/jonahbf/hackin/server/virt/log/application.log', maxBytes=1024,backupCount=5)
#handler = RotatingFileHandler('/opt/python/log/application.log', maxBytes=1024,backupCount=5)
#handler = RotatingFileHandler('/var/log/application.log', maxBytes=1024,backupCount=5)
handler.setFormatter(formatter)


application = Flask(__name__)
application.logger.addHandler(handler)
CORS(application, support_credentials=True)


@application.route('/api/', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_tasks():
    return 'a very simple answer'

@application.route('/api', methods=['POST'])
@cross_origin(supports_credentials=True)
def process_html():
    json_html = json.dumps(request.get_json())
    query_html = str(request.args.get('html'))
    form_html = request.form.get('html')
    application.logger.debug('json is ' + json_html)
    application.logger.debug('query is ' + str(query_html))
    application.logger.debug('form_html is ' + str(form_html))
    return form_html
    #return DEFAULT_LIST

if __name__ == '__main__':
    application.run(debug=True)
