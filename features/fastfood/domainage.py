from flask import jsonify
from flask_restful import Resource
from flask_apispec.views import MethodResource
import whois
from datetime import datetime, timedelta

class DomainAge(MethodResource,Resource):
    # @requires_auth
    def get(self, domain):
        try:
            w = whois.whois(domain)
            da = datetime.now() - w.creation_date
            days = da.days
        except:
            days = -1
        detail = "Found creation date : " + w.creation_date.strftime('%Y-%m-%d') if days != -1 else "Not creation date found to "+str(domain)
        return jsonify({"feature": "domainage", "domain": domain, "result": days, "detail": detail})