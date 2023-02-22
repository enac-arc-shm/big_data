from flask import Flask, render_template, request, Response,jsonify, redirect, url_for
import flask_dbmongo as dbase
from sensor import Sensor
from datetime import date
from datetime import datetime

#Día actual
today = date.today()

#Fecha actual
db = dbase.dbConexion()
app = Flask(__name__)

#Rutas de la aplicación
@app.route('/')
def home():
    sensores = db['db_sensor']
    sensoresReceived = sensores.find()
    return render_template('index.html', sensores = sensoresReceived)

#Method Post
@app.route('/sensores', methods=['POST'])
def addSensores():
    sensores = db['sensores']
    nombre = request.form['nombre']
    valor1 = request.form['valor1']
    valor2 = request.form['valor2']
    fecha = datetime.now()
    if nombre and valor1 and valor2 and fecha:
        sensor = Sensor(nombre, valor1, valor2, fecha)
        sensores.insert_one(sensor.toDBCollection())
        response = jsonify({
        'sensor' : nombre,
        'valor1' : valor1,
        'valor2' : valor2,
        'fecha': fecha
        })
        return redirect(url_for('home'))
    else:
        return print("ERROR")

    
    
if __name__ == "__main__":
    app.run(debug=True, port=4000)