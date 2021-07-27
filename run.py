from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db

app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object('config.ProductionConfig')
elif app.config["ENV"] == "testing":
    app.config.from_object('config.TestingConfig')
else:
    app.config.from_object('config.DevelopmentConfig')
    
toolbar = DebugToolbarExtension(app)

connect_db(app)