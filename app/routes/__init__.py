from flask import (Flask, render_template, redirect) 

app = Flask(__name__)

from .routes import bp
app.register_blueprint(bp, )
