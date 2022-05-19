from flask import Flask, jsonify,request, render_template
import pandas as pd
import requests


app = Flask(__name__)

#Api Information
token = "26acf72248d97bde0a9eeb8c7a7b9279c3a67740a5fc2053d05d98faeab573f3"
uri = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/"
header = {"Bmx-Token":token}
params={"token":token}

UDIS = "SP68257"
DOLAR = "SF43718"
TIIE_I = "SF60648" #Por 28 dias
TIIE_II = "SF60649" #Por 91 dias
USD = 19.90
UDIS_VALUE = 6.63938
ROUND = 3


@app.route("/udis")
def getUDIS():
    #Los valores en pesos de las UDIS para cada día para el rango definido
    #El promedio, valor máximo y mínimo de las UDIS para el rango definido
    
    start = request.json['start']
    end = request.json['end']
    
    uri_new = "{u}/datos/{s}/{e}".format(u=UDIS,s=start,e=end)
    response = requests.get(uri + uri_new,params).json()["bmx"]["series"][0]["datos"]
    out = []

    for i in response:
        out.append(float(i["dato"]))
        
    s = pd.Series(out)
    udi_to_mx = list(map (lambda x: round(x * UDIS_VALUE,3), out))
        
    return jsonify({
        "udis_mxn":udi_to_mx,
        "max_udis": s.max(),
        "min_udis": s.min(),
        "mean_udis": round(s.mean(),ROUND)
        })    
      
@app.route("/dolar")
def getDolar():
    #Los valores en pesos del dólar para cada día para el rango definido
    #El promedio, valor máximo y mínimo del dólar para el rango definido
    
    start = request.json['start']
    end = request.json['end']
    
    uri_new = "{u}/datos/{s}/{e}".format(u=DOLAR,s=start,e=end)
    response = requests.get(uri + uri_new,params).json()["bmx"]["series"][0]["datos"]
    out = []

    for i in response:
        out.append(float(i["dato"]))
        
    s = pd.Series(out)
    udi_to_mx = list(map (lambda x: round(x * USD,ROUND), out))
        
    return jsonify({
        "dolar_to_mxn":udi_to_mx,
        "max_dolar": s.max(),
        "min_dolar": s.min(),
        "mean_dolar": round(s.mean(),ROUND)
        })    

@app.route("/tiie")
def getTIIE():
    #Se requiere además otro dato financiero, la TIIE (Tasas de Interés Interbancarias)
    
    start = request.json['start']
    end = request.json['end']
    
    uri_tiie_i = "{u}/datos/{s}/{e}".format(u=TIIE_I,s=start,e=end)
    uri_tiie_ii = "{u}/datos/{s}/{e}".format(u=TIIE_II,s=start,e=end)
    
    response_tiie_i = requests.get(uri + uri_tiie_i,params).json()["bmx"]["series"][0]["datos"]
    response_tiie_ii = requests.get(uri + uri_tiie_ii,params).json()["bmx"]["series"][0]["datos"]
    
    out_response_tiie_i = []
    out_response_tiie_ii = []

    for i in response_tiie_i:
        out_response_tiie_i.append(float(i["dato"]))
        
    for i in response_tiie_ii:
        out_response_tiie_ii.append(float(i["dato"]))    
        
    return jsonify({
        "tiie_i":out_response_tiie_i,
        "tiie_ii":out_response_tiie_ii})


if __name__ == '__main__':
   app.run(debug = True)
   
