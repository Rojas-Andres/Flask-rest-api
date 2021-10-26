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
        except:
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
        response = requests.post('http://localhost:5000/Api/Usuario/CreateUser/',json=args)
        if response.status_code == 200:
            return render_template('login.html')
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
            response_user = requests.post('http://localhost:5000/Api/Usuario/ValidarUsuario/',json={"username":username})
            response_user = json.loads(response_user.text)
            session["token"] = response_api["token"]
            session["rol"] = response_user["rol"]
            return render_template('index.html')
        else:
            return render_template('login.html')
    return render_template('login.html')

@app.route('/venta',methods=['GET','POST'])
@token_required
def venta():
    if session["rol"]=="admin":
        if request.method=="POST":
            id_username = request.form["id_username"]
            venta = request.form["venta"]
            venta_producto = request.form["venta_producto"]
            args = {
                "id_username":int(id_username),
                "venta":int(venta),
                "venta_producto":int(venta_producto)
            }
            response = requests.post('http://localhost:5000/Api/ApiVentas/Ventas/',json=args)
            if response.status_code == 200:
                return render_template('ventas.html')
            else:
                return render_template('ventas.html')
        return render_template('ventas.html')
    else:
        return render_template('permisos.html')
@app.route('/permisos',methods=["GET"])
def permisos():
    return render_template('permisos.html')
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")