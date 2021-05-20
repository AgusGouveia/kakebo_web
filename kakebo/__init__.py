#Hacemos que kakebo sea importable desde cualquier sitio
from flask import Flask
app = Flask(__name__)
from kakebo import views
