from flask import jsonify
from flask_restful import Resource
from flask_apispec.views import MethodResource
import dns
import dns.resolver

class DnsTTL(MethodResource,Resource):
    # @requires_auth
    def get(self, domain):
        ttl = -1
        try:
            get_ns = dns.resolver.resolve(domain, 'NS')
            if len(get_ns.rrset) > 0:
                name_server = get_ns.rrset[0]
                answer_ns = dns.resolver.resolve(str(name_server), 'A')
                if len(answer_ns.rrset) > 0:
                    name_server_ip = answer_ns.rrset[0]
                    resolver = dns.resolver.Resolver()
                    resolver.nameservers = [str(name_server_ip)]
                    answer_a = resolver.resolve(domain, 'A')
                    ttl = answer_a.rrset.ttl
        except Exception as err:
            print(err)
            ttl = -1
        detail = "Found TTL" if ttl != -1 else "Not TTL found to "+str(domain)
        return jsonify({"feature": "dnsttl", "domain": domain, "result": ttl, "detail": detail})