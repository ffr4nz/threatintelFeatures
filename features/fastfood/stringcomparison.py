from flask import jsonify
from flask_restful import Resource
from flask_apispec.views import MethodResource
import pandas as pd
import jellyfish

df = pd.read_csv('data/trancotop1m.csv')
df_dict = df.to_dict('records')

class StrComparison(MethodResource,Resource):
    # @requires_auth
    def get(self, domain):
        domain_found = ""
        similar = False
        for row in df_dict:
            result = jellyfish.jaro_winkler_similarity(str(row['domain']), str(domain))
            if result > 0.97:
                similar = True
                break
        detail = "Found near domain by distance string comparison: " + str(result) if similar else "Not similar domain found."
        domain_found = str(row['domain']) if similar else ""
        return jsonify({"feature": "strcomparison", "domain": domain, "result": domain_found, "detail": detail})