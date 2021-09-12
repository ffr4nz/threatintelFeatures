from flask import jsonify
from flask_restful import Resource
from flask_apispec.views import MethodResource
import numpy as np
import pandas as pd

df = pd.read_csv('data/ddns.csv')


class DDns(MethodResource,Resource):
    # @requires_auth
    def get(self, domain):
        r = np.where(df['domain'] == domain)
        try:
            result = False if str(r[0][0]) == '' else True
        except:
            result = False
        detail = "Domain listed as Dynamic DNS" if result else "Domain not listed as Dynamic DNS"
        return jsonify({"feature": "ddns", "domain": domain, "result": result, "detail": detail})
