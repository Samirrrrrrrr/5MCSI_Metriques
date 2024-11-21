from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
from flask import Flask, jsonify
from urllib.request import urlopen
from datetime import datetime
import sqlite3
import json

                                                                                                                                       
app = Flask(__name__)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route('/tawarano/')
def meteo():
    # Requête vers l'API OpenWeatherMap
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    # Charger le JSON brut
    json_content = json.loads(raw_content.decode('utf-8'))
    
    results = []
    # Extraire les données des dates et températures
    for list_element in json_content.get('list', []):
        dt_value = datetime.utcfromtimestamp(list_element.get('dt')).strftime('%Y-%m-%d %H:%M:%S')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion Kelvin -> °C
        results.append({'Jour': dt_value, 'Température (°C)': round(temp_day_value, 2)})
    
    # Retourner les données sous forme de JSON
    return jsonify(results=results)


@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm2
  
if __name__ == "__main__":
  app.run(debug=True)
