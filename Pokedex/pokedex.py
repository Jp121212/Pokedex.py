
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/pokedex_jp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
class Pokemones(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    tipo = db.Column(db.String(80), nullable=True)
    edad = db.Column(db.Integer,nullable=False)
    fechadenacimiento = db.Column(db.String(80),nullable= False)
    ataque = db.Column(db.String(90),nullable=False)
    foto = db.Column(db.String(100),nullable= True)
def __repr__(self):
        return '<Usuario %r>' % self.nombre

##class SchemaValidator(object):
#   def __init__(self, response={}):
#       self.response = response
#   def isTrue(self):
#       errorMessages = []
#       try:
#           nombre = self.response.post("nombre",None)
#           if nombre is None or len(nombre) <= 1:
#               raise Exception("Error")
#        except Exception as e:errorMessages.append("El nombre es requerido obligatoriamente")
#        try:
#           edad = self.response.post("edad",None)
#           if edad is None or len(edad) <= 1:
#                raise Exception("Error")
#        except Exception as e:errorMessages.append("La edad es requerida obligatoriamente")
#        try:
#           fechadenacimento = self.response.post("fechadenacimiento",None)
#            if fechadenacimento is None or len(fechadenacimento) <= 1:
#               raise Exception("Error")
#        except Exception as e:errorMessages.append("La fecha de nacimiento requerida obligatoriamente")
#        try:
#            ataque = self.response.post("ataque",None)
#          if ataque is None or len(ataque) <= 1:
##                raise Exception("Error")
##        except Exception as e:errorMessages.append("El ataque es requerido obligatoriamente")
    
# *Controllers

class IndexRoute(Resource):
    def get(self):
        return {'response': 'Hola, Bienvenido A mi PokedexAPI :)'}
class IndexUsuario(Resource):
    def get(self):
        pokemones = Pokemones.query.all()
        response = []
        if pokemones:
            for pokemon in pokemones:
                response.append({
                "id": pokemon.id,
                "nombre": pokemon.nombre,
                "tipo": pokemon.tipo,
                "edad": pokemon.edad,
                "fechadenacimiento": pokemon.fechadenacimiento,
                "ataque": pokemon.ataque,
                "foto": pokemon.foto
                })
        return {'response': response}, 200

##  _init_ = SchemaValidator(response = pokemonacrear)
# ##   response = _init_.isTrue()
    def post(self):
        pokemonacrear = request.get_json()
        pokemonacrear = request.get_json()
        if pokemonacrear is None:
            return "Los campos estan vacios", 400
        if 'nombre' not in pokemonacrear:
            return 'Especificar nombre es obligatorio',400
        if 'edad' not in pokemonacrear:
            return 'Especificar edad es obligatorio', 400 
        if 'fechadenacimiento' not in pokemonacrear:
            return "Especificar la Fecha de nacimiento es obligatorio",400
        if "ataque" not in pokemonacrear:
            return "Especificar el ataque es obligatorio",400
        else:
            pokemon = Pokemones(nombre=pokemonacrear['nombre'], tipo=pokemonacrear['tipo'], edad=pokemonacrear['edad'], fechadenacimiento=pokemonacrear['fechadenacimiento'],ataque=pokemonacrear['ataque'],foto=pokemonacrear['foto'] )
            db.session.add(pokemon)
            db.session.commit()
            return { "response": "Pokemon registrado exitosamente!"}, 201


class PokemonbyID(Resource):
    def get(self, id):
        pokemon = Pokemones.query.filter_by(id=id).first()
        if pokemon == None:
            return ({"Malas noticias": "No se encuentran Pokemones registrados  con el id:  "+ str (id) }),200
        else:
            return {'Pokemon': {
                "id": pokemon.id,
                "nombre": pokemon.nombre,
                "tipo": pokemon.tipo,
                "edad": pokemon.edad,
                "fechadenacimiento": pokemon.fechadenacimiento,
                "ataque": pokemon.ataque,
                "foto": pokemon.foto
        }}, 200

    def put(self, id):
        pokemon = Pokemones.query.filter_by(id=id).first()
        datos = request.get_json()
        # TODO: LOOKUP 'ARGUMENT PARSING for Flask-RESTful'
        pokemon.nombre = datos['nombre']
        pokemon.tipo = datos['tipo']
        pokemon.edad = datos['edad']
        pokemon.fechadenacimiento = datos['fechadenacimiento']
        pokemon.ataque =  datos['ataque']
        pokemon.foto = datos['foto']
        db.session.commit()
        return {"response": "Pokemon actualizado con exito!"}

    def delete(self, id):
        pokemon = Pokemones.query.filter_by(id=id).first()
        db.session.delete(pokemon)
        db.session.commit()
        return { "response": "Usuario con id: {pokemon}. Borrado exitosamente. ".format(pokemon=id)}, 203




# *Routes
# GET
api.add_resource(IndexRoute, '/')
# GET, POST
api.add_resource(IndexUsuario, '/pokemones')
# GET, PUT, DELETE
api.add_resource(PokemonbyID, '/pokemones/<int:id>')
# ------------------------------------------------------
# !Create row
# admin = User(username='Pedro', tipo='Administrador', email='admin@sistema.com')
# usuario = User(username='Maria', tipo='Usuario', email='maria@sistema.com')
# db.session.add(admin)
# db.session.add(usuario)
# db.session.commit()
# !Get all rows
# informacionUsuario = User.query.all()
# print(informacionUsuario)
# if informacionUsuario:
# for usuario in informacionUsuario:
# print('id: {id}, username: {u}, tipo: {t}, correo: {c}'.format(id=usuario.id, u=usuario.username, t=usuario.tipo, c=usuario.email))
# !Get single row by filter
# usuarioDeId = User.query.filter_by(id=3,tipo='admin').first()
# print(usuarioDeId.id)
# print(usuarioDeId.username)
# !Update a row
# registroAActualizar = User.query.filter_by(username='Pedro').first()
# registroAActualizar.email = 'admin1@sistema.com'
# db.session.commit()
# !delete
# db.session.delete(registroAActualizar)
# db.session.commit()
db.create_all()
db.session.commit()