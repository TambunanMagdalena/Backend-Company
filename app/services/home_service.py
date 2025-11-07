from flask import render_template, Response
from app.utils import response 

def index():
    return render_template('frontend.html')
