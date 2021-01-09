from http.server import BaseHTTPRequestHandler
# from http.server import HTTPServer
from user_agents import parse as pua
from urllib.parse import urlparse as pur
from time import strftime,localtime
import requests as r
def getlocation(ip):
     print(str(ip))
     ip = str(ip)
     if ip == "127.0.0.1":
          return "LC-LC"
     elif ip == "None":
          return "UK-UK"
     else :
          response = r.get("https://api.ip.sb/geoip/"+ip).json()
          return str(response['country_code'])+" "+str(response['region_code'])
def makesvg(location,time,ip,os,browser):
     s = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"770\" height=\"345\" viewBox=\"0 0 770 345\" fill=\"none\"><style>.line { stroke:#707569; stroke-width:1 }</style><rect x=\"0.5\" y=\"0.5\" rx=\"4.5\" height=\"60%\" stroke=\"#f8e5e5\" width=\"60%\" fill=\"#fffefe\" stroke-opacity=\"1\" /><g transform=\"translate(25, 35)\"><g transform=\"translate(0, 0)\" font-family=\"Verdana, Microsoft Yahei\" text-rendering=\"geometricPrecision\" font-size=\"18\"><text x=\"0\" y=\"0\" fill=\"#ec2727\" font-weight=\"bold\" > 欢迎来自"+location+"的朋友 </text><line x1=\"0\" y1=\"5\" x2=\"200\" y2=\"5\" class=\"line\"/><text x=\"0\" y=\"30\" fill=\"#ec2727\" font-weight=\"bold\" > 今天是"+time+"</text><line x1=\"0\" y1=\"35\" x2=\"250\" y2=\"35\" class=\"line\"/><text x=\"0\" y=\"60\" fill=\"#ec2727\" font-weight=\"bold\" > 您的IP是:"+ip+"</text><line x1=\"0\" y1=\"65\" x2=\"210\" y2=\"65\" class=\"line\"/><text x=\"0\" y=\"90\" fill=\"#ec2727\" font-weight=\"bold\" > 您使用的是"+os+" </text><line x1=\"0\" y1=\"95\" x2=\"210\" y2=\"95\" class=\"line\"/><text x=\"0\" y=\"120\" fill=\"#ec2727\" font-weight=\"bold\" >"+browser+"</text><line x1=\"0\" y1=\"125\" x2=\"250\" y2=\"125\" class=\"line\"/><image href=\"https://cdn.jsdelivr.net/gh/lbr77/pictures@master/img/20210109093739.png\" x=\"300\" y=\"0\" height=\"100px\" width=\"100px\"/></g></g></svg> "
     return s
def gettime():
     return str(strftime("%Y年%m月%d日 星期%U",localtime()))
def getos(UA):
     return str(UA.os.family+" "+UA.os.version_string)+"操作系统"
def getbrowser(UA):
     return str(UA.browser.family+" "+UA.browser.version_string)+"浏览器"
class handler(BaseHTTPRequestHandler):
     def do_GET(self):
          UA = pua(str(self.headers.get("User-Agent")))
          ip = self.headers.get('x-forwarded-for')
          message = makesvg(getlocation(ip),gettime(),str(ip),getos(UA),getbrowser(UA))
          self.send_response(200)
          self.send_header("Content-type","image/svg+xml; charset=utf-8")
          self.end_headers()
          self.wfile.write(message.encode())
          return

