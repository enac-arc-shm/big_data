''' Instalar
pip install pymongo
pip install certifi
pip install pymongo[srv]
pip install flask
'''

from pymongo import MongoClient
import certifi

client = MongoClient()

def dbConexion():
    try:
        client = MongoClient('mongodb+srv://21300062:mongoatlas@cluster02023.aoycnel.mongodb.net')
        db = client['db_sensor']
    except ConnectionError:
        print("Error al conectar con la db")
    return db

def consulta_sensores():
    db = dbConexion()
    sensores = db['sensores']
    c_sensores = sensores.find()
    return c_sensores