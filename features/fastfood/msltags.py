import requests
from bs4 import BeautifulSoup
from flask import jsonify
from flask_restful import Resource
from flask_apispec.views import MethodResource


# https://iopscience.iop.org/article/10.1088/1742-6596/1140/1/012048/pdf
# https://github.com/brandonfire/A-machine-learning-approach-for-phishing-detection/blob/5b3c378a8c867049cea0f77ce235edacdd28ce8d/myURLTMv3Cbhv5.02.py#L211
class MSLtags(MethodResource, Resource):
    def checkpathdomain(self, pathlist, domain):
        count = 0
        try:
            for path in pathlist:
                if path.startswith('http://') or path.startswith('https://') or path.startswith('//'):
                    count += 1
                elif path.startswith('.') or path.startswith('/'):
                    continue
                else:
                    urldomain = path.split('/')[0]
                    if urldomain == domain:
                        continue
                    else:
                        count += 1
        except Exception as e:
            print("check path", e)
            pass
        return count

    # @requires_auth
    def get(self, domain):
        result = 0
        try:
            try:
                req = requests.get("https://" + domain)
            except:
                req = requests.get("http://" + domain)
            soup = BeautifulSoup(req.text, features="html.parser")
            metaurllist = soup.find_all('<meta.*(?!>)URL=(.*)".*>')
            scripturllist = soup.find_all('<script.*(?!>)src="(.*)">')
            linklist = soup.find_all('<link.*(?!>)href="(.*)">')
            total = len(metaurllist) + len(scripturllist) + len(linklist)
            count = self.checkpathdomain(metaurllist, domain) + self.checkpathdomain(scripturllist, domain) + self.checkpathdomain(
                linklist, domain)
            result = -1 if count < 0.17 * total else 1 if count > 0.81 * total else 0
        except Exception as err:
            print(err)
            result = 0
        detail = "Found " + str(result) + " Mail to Form Handler" if result else "Not Mail Form Handler found"
        return jsonify({"feature": "msltags", "domain": domain, "result": result, "detail": detail})
