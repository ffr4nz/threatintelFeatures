from flask import jsonify
from flask_restful import Resource
from flask_apispec.views import MethodResource
import dns
import dns.resolver

class NumberIPs(MethodResource,Resource):
    # @requires_auth
    def get(self, domain):
        numberip = -1
        ips = list()
        try:
            for i in range(10):
                resolver = dns.resolver.Resolver();
                a = resolver.resolve(domain, 'A', lifetime=1)
                for item in a:
                    ips.append(item)
        except Exception as err:
            print(err)
            numberip = -1

        detail = "Found multiple IPs" if len(ips) > 1 else "Not IP found to "+str(domain)
        return jsonify({"feature": "numberips", "domain": domain, "result": len(list(dict.fromkeys(ips))), "detail": detail})