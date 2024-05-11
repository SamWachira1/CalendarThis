from flask import render_template, redirect, Blueprint

bp = Blueprint('main', __name__)

@bp.route('/')
def main():
    return "Calendar working"
