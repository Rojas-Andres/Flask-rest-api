from flask import Blueprint,jsonify, request
from flask_restplus import Api, Resource,fields 
from api.functions import *
bp_api = Blueprint('Api',__name__,url_prefix="/Api")

api = Api(bp_api,version="1.0",title="Api",description="End Points")
ns_model = api.namespace('Methods', description='Metodos')
ns_model_venta = api.namespace('ApiVentas', description='Ventas')
ns_model_usuario = api.namespace('Usuario', description='Usuario')

class VerificarDatos():
    Login = api.model('login',{
        "username":fields.String(description=u"username",required=True,),
        "password":fields.String(description=u"password",required=True,),
    })
    Crear_Venta = api.model('venta',{
        "id_username":fields.Integer(description=u"id_username",required=True,),
        "venta":fields.Integer(description=u"valor de la venta",required=True,),
        "venta_producto":fields.Integer(description=u"venta Producto",required=True,),
    })
    CambiarVenta = api.model('cambiar venta',{
        "id":fields.Integer(description=u"id venta",required=True,),
        "venta":fields.Integer(description=u"valor de la venta",required=True,),
    })
    EliminarVenta =api.model('Eliminar venta',{
        "id":fields.Integer(description=u"id venta",required=True,),
    }) 
@ns_model.route('/Login/')
@api.doc(description="Correo y contraseña")
class Login(Resource):
    @ns_model.expect(VerificarDatos.Login,validate=True)
    def post(self):
        auth = request.json
        valida = valida_user(auth["username"],auth["password"])
        if 'token' in valida:
            return jsonify(valida)
        return jsonify({"Respuesta":"Login requerido!!!!"})


@ns_model_usuario.route('/CreateUser/')
@api.doc(description="Correo y contraseña")
class CrearUsuario(Resource):
    @ns_model_usuario.expect(VerificarDatos.Login,validate=True)
    def post(self):
        usuario = request.json
        usuario_creado = crear_usuario(usuario["username"],usuario["password"])
        return jsonify(usuario_creado)

@ns_model_venta.route('/Ventas/')
@api.doc(description="Ventas")
class Venta(Resource):
    def get(self):
        venta = obtener_venta()
        return jsonify(venta)
    
    @ns_model_venta.expect(VerificarDatos.Crear_Venta,validate=True)
    def post(self):
        datos = request.json
        venta = crear_venta(datos["id_username"],datos["venta"],datos["venta_producto"])
        return jsonify(venta)
    
    @ns_model_venta.expect(VerificarDatos.CambiarVenta,validate=True)
    def put(self):
        datos = request.json 
        venta = actualizar_venta(datos["id"],datos["venta"])
        return jsonify(venta)
    @ns_model_venta.expect(VerificarDatos.EliminarVenta,validate=True)
    def delete(self):
        dato = request.json 
        venta = eliminar_venta(dato["id"])
        return jsonify(venta)
