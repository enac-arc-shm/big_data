class Sensor:
    def __init__(self, nombre, valor1, valor2, fecha):
        self.nombre = nombre
        self.valor1 = valor1
        self.valor2 = valor2
        self.fecha = fecha

    def toDBCollection(self):
        return{
            'sensor':self.nombre,
            'valor1':self.valor1,
            'valor2':self.valor2,
            'fecha':self.fecha
        }