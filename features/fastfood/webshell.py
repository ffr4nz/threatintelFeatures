import os
import numpy as np
import pandas as pd
import requests
from flask import jsonify
from flask_restful import Resource
from flask_apispec.views import MethodResource
from urllib.parse import urlparse

df = pd.read_csv('data/webshell.csv')

class WebShell(MethodResource,Resource):
    # @requires_auth
    def get(self, domain):
        lc = 0
        ws = False
        url_list = requests.get('http://web.archive.org/cdx/search/cdx?url=*.'+domain+'/*&output=text&fl=original&collapse=urlkey')
        for url in url_list.iter_lines():
            lc = lc + 1
            o = urlparse(url)
            if "." in str(o.path):
                resource = os.path.basename(o.path)
                r = np.where(df['resource'] == resource)
                try:
                    ws = False if str(r[0][0]) == '' else True
                except:
                    ws = False
        detail = "Found resource compatible with a webshell : " + str(os.path.basename(o.path)) if ws else "Not webshell found in "+str(lc)+" urls from archive.org"
        ws_found = str(os.path.basename(o.path)) if ws else ""
        return jsonify({"feature": "webshell", "domain": domain, "result": ws_found, "detail": detail})