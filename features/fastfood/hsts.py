import requests
from flask import jsonify
from flask_restful import Resource
from flask_apispec.views import MethodResource


class HSTS(MethodResource, Resource):
    # @requires_auth
    def get(self, domain):
        result = False
        try:
            req = requests.get("https://"+domain)
            if "x-frame-options" in req.headers.keys():
                result = True
        except Exception as err:
            print(err)
            result = False
        detail = "Found HSTS header - x-frame-options:" + req.headers['x-frame-options'] if result else "HSTS not found"
        return jsonify({"feature": "hsts", "domain": domain, "result": result, "detail": detail})
