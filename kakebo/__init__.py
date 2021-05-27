#Hacemos que kakebo sea importable desde cualquier sitio
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')

from kakebo import views
