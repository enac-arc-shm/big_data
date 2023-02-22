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
        client = MongoClient('mongodb+srv://21300018:sergio123@cluster0.ctse5jc.mongodb.net/test')
        db = client['db_sensor']
    except ConnectionError:
        print("Error al conectar con la db")
    return db