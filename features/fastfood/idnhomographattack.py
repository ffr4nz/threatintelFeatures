#
# Code from https://github.com/UndeadSec/checkURL
#
from flask import jsonify
from flask_restful import Resource
from flask_apispec.views import MethodResource

bad_chars = ['\u0430', '\u03F2', '\u0435', '\u043E', '\u0440', '\u0455', '\u0501', '\u051B', '\u051D']

class IDNHomographAttack(MethodResource,Resource):
    # @requires_auth
    def get(self, domain):
        idn = [bad_chars[i] for i in range(len(bad_chars)) if bad_chars[i] in domain]
        result = False if len(idn) == 0 else True
        detail = "Found IDN Homograph Attack character" if result else "Not Found IDN Homograph Attack character"
        return jsonify({"feature": "idnhomographattack", "domain": domain, "result": result, "detail": detail})
