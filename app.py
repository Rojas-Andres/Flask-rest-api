from flask import Flask,jsonify,request
from db import Session , engine
from config import connection_db
import json
from werkzeug.security import generate_password_hash,check_password_hash
import datetime
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import jwt
from api.controllers import bp_api
app = Flask(__name__)
app.config['SECRET_KEY']='Th1s1ss3cr3t'

#BD 
app.config['SQLALCHEMY_DATABASE_URI'] = connection_db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
session = Session()

from models import *
app.register_blueprint(bp_api)

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'No has enviado el token!'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            #current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'El token no es valido!'})
        return f(data['public_id'],*args, **kwargs)
   return decorator
@app.route('/login',methods=['GET'])
def login():
    auth = request.authorization   

    if not auth or not auth.username or not auth.password:  
        return jsonify({"Repuesta":"No se puede verificar"})
    
    with engine.connect() as con:
        user = con.execute(f"select * from usuario where username='{auth.username}'").one()
    print(user)       
    if check_password_hash(user[2], auth.password):  
        token = jwt.encode({'public_id': user[1], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])  
        return jsonify({'token' : token.decode('UTF-8')}) 
    else:

        return jsonify({"respuesta": "Contraseña incorrecta!"})

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hola este es el get'})


@app.route('/create_user',methods=['POST'])
def crear_usuario():
    #print(current_user)
    #if current_user == "administrador":
    data = json.loads(request.data)
    if 'username' not in data :
        return jsonify({"respuesta":"No estas enviando el username!"})
    
    if 'password' not in data :
        return jsonify({"respuesta":"No estas enviando el password!"})
    
    if len(data["username"])==0:
        return jsonify({"respuesta":"Username no puede estar vacio"})
    
    if len(data["password"])==0:
        return jsonify({"respuesta":"Password no puede estar vacio"})
    with engine.connect() as con:
        hash_password = generate_password_hash(data["password"],method="sha256")
        nuevo_usuario = Usuario(username=data["username"],password=hash_password)
        session.add(nuevo_usuario)
        try:
            session.commit()
        except:
            return jsonify({"respuesta":"Usuario ya esta creado en la base de datos!"})
    return jsonify({"respuesta":"Usuario creado correctamente!"})
    #else:
    #    return jsonify({"Repuesta":"El usuario no tiene permitido crear mas usuarios!"})

@app.route('/obtener_venta',methods=['GET'])
def obtener_venta():
    data = json.loads(request.data)
    if 'username' not in data:
        return jsonify({"respuesta":"Username no enviado , validar datos!"})
    with engine.connect() as con:
        obtener_usuario = f"select * from usuario where username = '{data['username']}'"
        respuesta = con.execute(obtener_usuario).one()
        obtener_venta = f"select venta from ventas where username_id = '{respuesta[0]}'"
        respuesta_ventas = con.execute(obtener_venta)
        respuesta_ventas = [i[0] for i in respuesta_ventas]
        return jsonify({"ventas_usuario":{"usuario":data['username'], "ventas":respuesta_ventas}})

@app.route('/ventas',methods=["GET"])
def obtener_ventas():
    with engine.connect() as con:
        obtener_ventas = "select * from ventas"
        respuesta_ventas = con.execute(obtener_ventas)
        lista = list()
        for i in respuesta_ventas:
            lista.append({"ID_VENTA":i[0],"valor_venta":i[2]})
    return jsonify({"Ventas":lista})

@app.route('/ventas',methods=["POST"])
def crear_venta():
    data = json.loads(request.data)
    if 'id_username' not in data:
        return jsonify({"Respuesta":"Id no esta en el body validar datos!"})
    if 'valor' not in data:
        return jsonify({"Respuesta":"La venta no esta en el body validar datos!"})
    if 'veta_productos' not in data:
        return jsonify({"Respuesta":"La venta no esta en el body validar datos!"})
    nueva_venta = Ventas(username_id=data["id_username"],venta = data["valor"],ventas_productos =data["veta_productos"] )
    db.session.add(nueva_venta)
    db.session.commit()
    return jsonify({"Repuesta":"Venta Creada!"})

@app.route('/ventas',methods=["PUT"])
def cambiar_venta():
    data = json.loads(request.data)
    if 'id' not in data:
        return jsonify({"Respuesta":"Id no esta en el body validar datos!"})
    if 'valor' not in data:
        return jsonify({"Respuesta":"La venta no esta en el body validar datos!"})
    venta = Ventas.query.get(data["id"])
    venta.venta = data["valor"]
    db.session.commit()
    return jsonify({"Respuesta":"Venta actualizada!"})

@app.route('/ventas',methods=["DELETE"])
def eliminar_venta():
    data = json.loads(request.data)
    if 'id' not in data:
        return jsonify({"Respuesta":"Id no esta en el body validar datos!"})
    
    venta = Ventas.query.get(data["id"])
    db.session.delete(venta)
    db.session.commit()
    return jsonify({"Respuesta":"Venta eliminada!"})

if __name__ == "__main__":
    app.run(debug=True)