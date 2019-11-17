from flask import Flask, jsonify, render_template, send_from_directory
import json
from flask_cors import CORS


app = Flask(__name__,template_folder='templates')
CORS(app)


@app.route("/KSP/TopAccidentCity/<unit_id>")
def TopAccidentCity(unit_id):
	with open('result.json') as f:
  		data = json.load(f)
	return jsonify(data[str(unit_id)])

@app.route("/KSP/Dashboard")
def Dashboard():
	return render_template('pag3.html')

@app.route("/KSP/Dashboard/descriptive_result.png")
def image():
	return send_from_directory('./templates',filename='descriptive_result.png')
	

@app.route("/KSP/Details/<unit_id>")
def Details(unit_id):
	return render_template('dashboard.html')



if __name__ == "__main__":
	app.run(host='0.0.0.0', port = 8080)