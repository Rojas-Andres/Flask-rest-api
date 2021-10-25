from flask import Flask,jsonify,request,render_template,redirect,url_for,session
from db import Session , engine,connection_db
import json
from werkzeug.security import generate_password_hash,check_password_hash
import datetime
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import jwt
from api.controllers import bp_api
import requests

app = Flask(__name__)
app.config['SECRET_KEY']='Th1s1ss3cr3t'

#BD 
app.config['SQLALCHEMY_DATABASE_URI'] = connection_db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
session_bd = Session()

from models import *
app.register_blueprint(bp_api)

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
        try:
            data = jwt.decode(session["token"], app.config['SECRET_KEY'])
            print("Excelente")
        except:
            print("El token no es valido o no esta logueado")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
   return decorator

@app.route('/', methods=['GET'])
@token_required
def index():
    return render_template('index.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return render_template('login.html')

@app.route('/registro',methods=['GET','POST'])
def registro():
    if request.method=='POST':
        username = request.form["username"]
        password = request.form["password"]
        args = {
            "username":username,
            "password":password
        }
        response = requests.post('http://localhost:5000/ApiVentas/Ventas/',json=args)
        if response.status_code == 200:
            return render_template('index.html')
        else:
            return render_template('registro.html')
    return render_template('registro.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form["username"]
        password = request.form["password"]
        args = {
            "username":username,
            "password":password
        }
        response = requests.post('http://localhost:5000/Api/Methods/Login/',json=args)
        if response.status_code == 200:
            response_api = json.loads(response.text)
            session["token"] = response_api["token"]
            return render_template('index.html')
        else:
            return render_template('login.html')
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")