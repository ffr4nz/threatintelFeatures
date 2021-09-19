import os

from flask import Flask
from flask_restful import Resource, Api

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from marshmallow import Schema, fields
import configparser

from features.fastfood.ddns import DDns
from features.fastfood.idnhomographattack import IDNHomographAttack
from features.fastfood.favicon import Favicon
from features.fastfood.stringcomparison import StrComparison
from features.fastfood.webshell import WebShell
from features.fastfood.domainage import DomainAge
from features.fastfood.dnsttl import DnsTTL
from features.fastfood.fw import FW
from features.fastfood.numberips import NumberIPs
from features.fastfood.numbercountries import NumberCountries
from features.fastfood.subdomains import Subdomains
from features.fastfood.hsts import HSTS
from features.fastfood.iframe import Iframe
from features.fastfood.sfh import SHF
from features.fastfood.formmail import FormMail
from features.fastfood.msltags import MSLtags
from features.fastfood.phishingbrands import PhishingBrands
from features.fastfood.tor import Tor
from features.fastfood.tldprice import TLDPrice

app = Flask(__name__)
api = Api(app)

config = configparser.ConfigParser()
config.read('config/config.ini')
cfg = config['features']


class AwesomeResponseSchema(Schema):
    message = fields.Str(default='Success')


if cfg.getboolean("ddns"): api.add_resource(DDns, '/ff/ddns/<domain>')
if cfg.getboolean("idnhattack"): api.add_resource(IDNHomographAttack, '/ff/idnhattack/<domain>')
if cfg.getboolean("favicon"): api.add_resource(Favicon, '/ff/favicon/<domain>')
if cfg.getboolean("strcomparison"): api.add_resource(StrComparison, '/ff/strcomparison/<domain>')
if cfg.getboolean("webshell"): api.add_resource(WebShell, '/ff/webshell/<domain>')
if cfg.getboolean("domainage"): api.add_resource(DomainAge, '/ff/domainage/<domain>')
if cfg.getboolean("dnsttl"): api.add_resource(DnsTTL, '/ff/dnsttl/<domain>')
if cfg.getboolean("fw"): api.add_resource(FW, '/ff/fw/<domain>')
if cfg.getboolean("numberips"): api.add_resource(NumberIPs, '/ff/numberips/<domain>')
if cfg.getboolean("numbercountries"): api.add_resource(NumberCountries, '/ff/numbercountries/<domain>')
if cfg.getboolean("subdomains"): api.add_resource(Subdomains, '/ff/subdomains/<domain>')
if cfg.getboolean("hsts"): api.add_resource(HSTS, '/ff/hsts/<domain>')
if cfg.getboolean("iframe"): api.add_resource(Iframe, '/ff/iframe/<domain>')
if cfg.getboolean("sfh"): api.add_resource(SHF, '/ff/sfh/<domain>')
if cfg.getboolean("formmail"): api.add_resource(FormMail, '/ff/formmail/<domain>')
if cfg.getboolean("msltags"): api.add_resource(MSLtags, '/ff/msltags/<domain>')
if cfg.getboolean("phishingbrands"): api.add_resource(PhishingBrands, '/ff/phishingbrands/<domain>')
if cfg.getboolean("tor"): api.add_resource(Tor, '/ff/tor/<domain>')
if cfg.getboolean("tldprice"): api.add_resource(TLDPrice, '/ff/tldprice/<domain>')

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='Threat Intel Features',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='2.0.0',
            info=dict(description="Everything you need to properly cook threat intelligence data.")
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
        'APISPEC_SWAGGER_UI_URL': '/'  # URI to access UI of API Doc
    })
    docs = FlaskApiSpec(app)
    docs.register(Favicon)
    docs.register(IDNHomographAttack)
    docs.register(DDns)
    docs.register(StrComparison)
    docs.register(WebShell)
    docs.register(DomainAge)
    docs.register(DnsTTL)
    docs.register(FW)
    docs.register(NumberIPs)
    docs.register(NumberCountries)
    docs.register(Subdomains)
    docs.register(HSTS)
    docs.register(Iframe)
    docs.register(SHF)
    docs.register(FormMail)
    docs.register(MSLtags)
    docs.register(PhishingBrands)
    docs.register(Tor)
    docs.register(TLDPrice)

    app.run(host='0.0.0.0', port=PORT, debug=True)
