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
    sensores = db['sensores']
    sensoresReceived = sensores.find()
    print(sensoresReceived)
    #for sensor in sensoresReceived:
     #   print(sensor.get("sensor"))
      #  print(sensor["sensor"])
    return render_template('index.html', sensores = sensoresReceived)
    # "Sensor"
#Method Post
@app.route('/sensores', methods=['POST'])
def addSensores():
    sensores = db['sensores']
    nombre = request.form['nombre']
    valor1 = request.form['valor1']
    valor2 = request.form['valor2']
    fecha = datetime.now()


    if nombre and valor1 and  valor2 and fecha:
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
        return notFound()

#Method delete
@app.route('/delete/<string:sensor_name>')
def delete(sensor_name):
    sensores = db['sensores']
    sensores.delete_one({'sensor' : sensor_name})
    return redirect(url_for('home'))

#Method Put
@app.route('/edit/<string:sensor_name>', methods=['POST'])
def edit(sensor_name):
    sensores = db['sensores']
    nombre = request.form['nombre']
    valor1 = request.form['valor1']
    valor2 = request.form['valor2']
    fecha = datetime.now()

    if nombre and valor1 and valor2 and fecha:
        sensores.update_one({'sensor' : sensor_name}, {'$set' : {'sensor' : nombre, 'valor1' : valor1, 'valor2' : valor2, 'fecha': fecha}})
        response = jsonify({'message' : 'Sensor ' + sensor_name + ' actualizado correctamente'})
        return redirect(url_for('home'))
    else:
        return notFound()

@app.errorhandler(404)
def notFound(error=None):
    message ={
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response




if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True, port=4000)