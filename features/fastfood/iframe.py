import requests
from bs4 import BeautifulSoup
from flask import jsonify
from flask_restful import Resource
from flask_apispec.views import MethodResource


class Iframe(MethodResource, Resource):
    # @requires_auth
    def get(self, domain):
        try:
            try:
                req = requests.get("https://" + domain)
            except:
                req = requests.get("http://" + domain)
            soup = BeautifulSoup(req.text, features="html.parser")
            iframes = soup.find_all('iframe')
            result = len(iframes)
        except Exception as err:
            print(err)
            result = 0
        detail = "Found " + str(result) + " iframes" if result else "Not iframes found"
        return jsonify({"feature": "iframe", "domain": domain, "result": result, "detail": detail})

