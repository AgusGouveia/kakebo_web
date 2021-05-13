from flask import Flask #En flask es donde tendremos guardada toda la app

app = Flask(__name__) #Crea una instancia de Flask. Flask es nuestra app, es donde inyectaremos la inf.

@app.route ('/') #Decorador. Asocia el contenido de nuestras funciones a nuestra ruta del servidor web
def index():
    return "Hola, mundo"

@app.route('/adios')
def bye():
    return "Hasta luego, cocodrilo"