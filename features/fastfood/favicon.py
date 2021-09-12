from flask import jsonify
from flask_restful import Resource
from flask_apispec.views import MethodResource
import mmh3, requests, codecs
import numpy as np
import pandas as pd

# data from https://github.com/sansatart/scrapts/blob/master/shodan-favicon-hashes.csv
df = pd.read_csv('data/shodan-favicon-hashes.csv')


class Favicon(MethodResource,Resource):
    # @requires_auth
    def get(self, domain):
        result = False
        response = None
        detail = ""
        hash = None
        sslStatus = None
        try:
            response = requests.get('http://'+domain+'/favicon.ico')
            sslStatus = False
        except:
            response = requests.get('https://'+domain+'/favicon.ico')
            sslStatus = True
        if response != None:
            if response.status_code == 200:
                favicon = codecs.encode(response.content, "base64")
                hash = mmh3.hash(favicon)
                r = np.where(df['http.favicon.hash'] == hash)
                try:
                    result = False if str(r[0][0]) == '' else True
                except Exception as error:
                    print(error)
                    result = False
                detail = "Favicon found and It's listed on known favicon hashes list." \
                    if result else "Favicon found but It's not listed on known favicon hashes."
            else:
                result = True
                detail = "Favicon not found"
        return jsonify({"feature": "favicon", "domain": domain, "result": result, "detail": detail, "meta":{"hash": hash, "ssl": sslStatus}})
