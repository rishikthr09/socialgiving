from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.googlemaps import GoogleMaps
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config.from_object('config')
db = SQLAlchemy(app)
GoogleMaps(app)
lm = LoginManager()
lm.init_app(app)

from app import views, models