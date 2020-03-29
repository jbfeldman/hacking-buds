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


application = Flask(__name__)
CORS(application)


# @application.route('/api', methods=['GET'])
# def get_tasks():
#     return 'a very simple answer'

@application.route('/api', methods=['GET', 'POST'])
def process_html():
    if request.method == 'POST':
        json_html = json.dumps(request.get_json()['html'])
        query_html = str(request.args.get('html'))
        form_html = request.form.get('html')
        logger.debug('json_html')
        return json.dumps(DEFAULT_LIST + [{'html': json_html[0:45]}])
    else:
        return 'try POSTING next time bud'


if __name__ == '__main__':
    application.run(debug=True)
