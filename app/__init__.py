from flask import Flask 
from config import Config

app = Flask(__name__)
app.config.from_object(Config)      # Applying configuration from Config.py

from app import routes              # Added  routes from routes.py