import json
import logging
import unicodedata

from flask import Flask
from flask import make_response
from flask import request


class Server:
    def __init__(self, port, cache_provider):
        self._port = port
        self._app = Flask(__name__)
        self._cache_provider = cache_provider

        @self._app.route("/get-cache", methods=['POST'])
        def main_page():
            logging.log(logging.INFO, request.values)
            key = unicodedata.normalize('NFKD', request.values.get('key')).encode('utf-8', 'ignore')
            doc_str = cache_provider.get(key)
            if doc_str is None:
                return ""

            doc = json.dumps(doc_str, default=convert_to_builtin_type).encode('utf-8')
            response = make_response(json.dumps(doc, sort_keys=True, indent=4))
            response.headers['Content-type'] = "application/json"
            return response

    def start(self):
        self._app.run(host='0.0.0.0', port=self._port, debug=True)


def convert_to_builtin_type(obj):
    d = {}
    d.update(obj.__dict__)
    return d
