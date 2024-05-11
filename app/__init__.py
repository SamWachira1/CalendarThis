from flask import (Flask, render_template, redirect) 
from .config import Config


app = Flask(__name__)
app.config.from_object(Config)

from .routes import routes
app.register_blueprint(routes.bp)
