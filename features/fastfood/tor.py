import requests
from flask import jsonify
from flask_restful import Resource
from flask_apispec.views import MethodResource
import dns
import dns.resolver

class Tor(MethodResource,Resource):
    # @requires_auth
    def get(self, domain):
        result = False
        try:
            answer = dns.resolver.resolve(str(domain), 'A')
            if len(answer.rrset) > 0:
                server_ip = answer.rrset[0]
                tor_info = requests.get('https://onionoo.torproject.org/details?search=' + str(server_ip))
                tor_info_json = tor_info.json()
                if "relays" in tor_info_json.keys():
                    result = True if len(tor_info_json["relays"]) > 0 else True
        except Exception as err:
            print(err)
        detail = "Domain resolve an IP that is used as part of TOR network" if result else "Domain resolve an IP that is NOT used as part of TOR network"
        return jsonify({"feature": "tor", "domain": domain, "result": result, "detail": detail})