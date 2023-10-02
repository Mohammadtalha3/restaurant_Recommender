from flask import Flask

app= Flask(__name__)

@app.route('/')
def home():
    return "This is a home page"

from controller.user_controller import *  

