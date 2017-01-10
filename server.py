import json
import logging

from flask import Flask
from flask import request


class Server:
    def __init__(self, port, cache_provider):
        self._port = port
        self._app = Flask(__name__)
        self._cache_provider = cache_provider

        @self._app.route("/get-cache", methods=['POST'])
        def main_page():
            logging.log(logging.INFO, request.form)
            key = request.form.get('url')
            doc_str = cache_provider.get(key)
            if doc_str is None:
                return ""

            doc = json.dumps(doc_str, default=convert_to_builtin_type).encode('utf-8')
            logging.log(logging.INFO, doc)
            return doc

    def start(self):
        self._app.run(host='0.0.0.0', port=self._port, debug=True)


def convert_to_builtin_type(obj):
    d = {}
    d.update(obj.__dict__)
    return d
