import tldextract
from flask import jsonify
from flask_restful import Resource
from flask_apispec.views import MethodResource
import numpy as np
import pandas as pd

df = pd.read_csv('data/tldpricing.csv')
#https://support.google.com/domains/answer/6010092?hl=en#zippy=%2Cprice-by-domain-ending

class TLDPrice(MethodResource,Resource):
    # @requires_auth
    def get(self, domain):
        r = np.where(df['tld'] == tldextract.extract(domain).suffix)
        try:
            result = int(df.values[r[0][0]][1])
        except:
            result = -1
        detail = "Domain price found (€)" if result != -1 else "Domain price not found"
        return jsonify({"feature": "tldprice", "domain": domain, "result": result, "detail": detail})