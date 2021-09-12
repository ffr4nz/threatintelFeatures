import requests
from flask import jsonify
from flask_restful import Resource
from flask_apispec.views import MethodResource
import dns
import dns.resolver

class NumberCountries(MethodResource,Resource):
    # @requires_auth
    def get(self, domain):
        ips = list()
        try:
            for i in range(10):
                resolver = dns.resolver.Resolver();
                a = resolver.resolve(domain, 'A', lifetime=1)
                for item in a:
                    geojson = requests.get("http://ip-api.com/json/"+str(item)).json()
                    ips.append(geojson['countryCode'])
        except Exception as err:
            print(err)

        detail = "Found multiple Domains "+ str(','.join(list(dict.fromkeys(ips)))) if len(ips) > 0 else "Not Countries found to "+str(domain)
        return jsonify({"feature": "numbercountries", "domain": domain, "result": len(list(dict.fromkeys(ips))), "detail": detail})