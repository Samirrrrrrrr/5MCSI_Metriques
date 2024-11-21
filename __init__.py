from flask import Flask, render_template, jsonify
from datetime import datetime
from urllib.request import urlopen
import json

app = Flask(__name__)

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    try:
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/commits/')
def commits():
    try:
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "<h1>Bienvenue sur votre projet Flask</h1>"

if __name__ == "__main__":
    app.run(debug=True)
