import socket
from socket import *
import datetime
import time
from flask import jsonify
from flask_restful import Resource
from flask_apispec.views import MethodResource

class FW(MethodResource,Resource):
    # @requires_auth
    def get(self, domain):
        result = True
        proto = "tcp"
        open_ports = list()
        close_ports = list()
        filter_ports = list()
        ports = {21,22,23,25,26,53,80,81,110,111,113,135,139,143,179,199,443,445,465,514,515,548,554,587,646,993,995,1025,1027,1433,1720,1723,2000,2001,3306,3389,5060,5666,5900,6001,8000,8008,8080,8443,8888,10000,32768,49152,49154}
        try:
            insert_data = {}
            for port in ports:
                try:
                    # socket initialization
                    if proto == 'udp':
                        sckt = socket(AF_INET, SOCK_DGRAM)
                    elif proto == 'tcp':
                        sckt = socket(AF_INET, SOCK_STREAM)
                    received = ''
                    sckt.settimeout(0.2)
                    sckt.connect((domain, int(port)))
                    if port == 80:
                        sckt.send('GET / HTTP/1.0\r\n\r\n'.encode('utf-8'))
                        results = sckt.recv(1024)
                    elif port == 21:
                        results = sckt.recv(1024)
                    elif port == 161:
                        results = sckt.recv(1024)
                    else:
                        sckt.send('Hello\r\n'.encode('utf-8'))
                    results = sckt.recv(1024)
                    open_ports.append(port)
                except timeout as terr:
                    #print('Timeout! ', terr)
                    filter_ports.append(port)
                except Exception as err:
                    print('Error! ', err)
                finally:
                    sckt.close()

            if len(open_ports) + len(close_ports) > len(filter_ports):
                result = False
        except Exception as err:
            print(err)
        detail = "Found FW" if result else "Not FW found before "+str(domain)
        return jsonify({"feature": "fw", "domain": domain, "result": result, "detail": detail})


