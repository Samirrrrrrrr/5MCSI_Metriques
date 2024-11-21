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

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

@app.route('/commits/')
def commits():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = urlopen(url)
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))

    minutes_count = {}
    for commit in json_content:
        date_string = commit['commit']['author']['date']
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minute = date_object.minute
        if minute not in minutes_count:
            minutes_count[minute] = 0
        minutes_count[minute] += 1

    results = [{'minute': k, 'count': v} for k, v in sorted(minutes_count.items())]
    return render_template('commits.html', data=results)

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

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
