import requests
from bs4 import BeautifulSoup
from flask import jsonify
from flask_restful import Resource
from flask_apispec.views import MethodResource
#https://iopscience.iop.org/article/10.1088/1742-6596/1140/1/012048/pdf

class SHF(MethodResource, Resource):
    # @requires_auth
    def get(self, domain):
        result = 0
        try:
            try:
                req = requests.get("https://" + domain)
            except:
                req = requests.get("http://" + domain)
            soup = BeautifulSoup(req.text, features="html.parser")
            formhandle = soup.find_all('<form.*(?!>)action="([^ >"]*)".*>')
            for form in formhandle:
                if form.startswith("about:blank"):
                    result = 1
                elif form.startswith('http://') or form.startswith('https://') or form.startswith('//'):
                    result = 0
        except Exception as err:
            print(err)
            result = 0
        detail = "Found " + str(result) + " Server Form Handler" if result else "Not Server Form Handler found"
        return jsonify({"feature": "shf", "domain": domain, "result": result, "detail": detail})

