import requests
from bs4 import BeautifulSoup
from flask import jsonify
from flask_restful import Resource
from flask_apispec.views import MethodResource


# https://iopscience.iop.org/article/10.1088/1742-6596/1140/1/012048/pdf
# https://github.com/brandonfire/A-machine-learning-approach-for-phishing-detection/blob/5b3c378a8c867049cea0f77ce235edacdd28ce8d/myURLTMv3Cbhv5.02.py#L211
class FormMail(MethodResource, Resource):
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
                if form.contains("mail(") or form.contains("mailto:"):
                    result = 1
                elif form.startswith('http://') or form.startswith('https://') or form.startswith('//'):
                    result = 0
        except Exception as err:
            print(err)
            result = 0
        detail = "Found " + str(result) + " Mail to Form Handler" if result else "Not Mail Form Handler found"
        return jsonify({"feature": "formmail", "domain": domain, "result": result, "detail": detail})
