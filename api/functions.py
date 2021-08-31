

from werkzeug.security import generate_password_hash,check_password_hash
import datetime
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import jwt
from db import Session , engine

llave = "Th1s1ss3cr3t"
def valida_user(username,password):
        
    with engine.connect() as con:
        try:
            user = con.execute(f"select * from usuario where username='{username}'").one()
        except:
            user = None 
    if user : 
        if check_password_hash(user[2], password):  
            token = jwt.encode({'public_id': user[1], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, llave)  
            return {'token' : token.decode('UTF-8')}
        
    return {"respuesta": "Contraseña incorrecta!"}