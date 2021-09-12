import requests
from flask import jsonify
from flask_restful import Resource
from flask_apispec.views import MethodResource

SUBLIST3R_URL = "https://api.sublist3r.com/search.php?domain={}"


class Subdomains(MethodResource, Resource):
    # @requires_auth
    def get(self, domain):
        result = False
        subdomains = list()
        subdomains_count_list = list()
        subdomains_len_list = list()
        try:
            req = requests.get(SUBLIST3R_URL.format(domain))
            if req.status_code == 200:
                json_response = req.json()
                if json_response is not None:
                    for hostname in json_response:
                        if str(hostname).endswith('.' + domain):
                            subdomains_count_list.append(len(hostname.split(".")))
                            subdomains_len_list.append(len(hostname))
                            subdomains.append(str(hostname))
            print(subdomains)
            print(max(subdomains_count_list))
            print(max(subdomains_len_list))
        except Exception as err:
            print(err)
            result = False
        detail = "Found suspicious subdomains" if result else "Domain not listed as Dynamic DNS"
        return jsonify({"feature": "subdomains", "domain": domain, "result": result, "detail": detail})
