# 0. ejecutamos pip install flask flask-sqlalchemy flask-migrate flask-cors flask-jwt-extended
# 1. Crear modelos
# 2. importamos las librerias de flask
from crypt import methods
from flask import Flask, request, jsonify, session
from flask_migrate import Migrate
from models import db, Usuario, Regiones, Provincias, Comunas, Clientes
from flask_cors import CORS, cross_origin

# 16. jwt seguridad
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

# 3. instanciamos la app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Conten-Type'
app.url_map.strict_slashes = False
app.config['DEBUG'] = False
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# 17. configuracion de seguridad
app.config['JWT_SECRET_KEY'] = "secret-key"
app.config["JWT_SECRET_KEY"] = "os.environ.get('super-secret')"
jwt = JWTManager(app)

db.init_app(app)

Migrate(app, db)


# 18. Ruta de login
@app.route("/login", methods=["POST"])
def create_token():
    email = request.json.get("email")
    password = request.json.get("password")

    user = Usuario.query.filter(Usuario.email == email, Usuario.password == password).first()

    if user == None:
        return jsonify({ 
            "estado": "error",
            "msg": "Error en email o password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token, usuario_id=user.id),200


# 5. Creamos la ruta por defecto para saber si mi app esta funcionado
# 6. ejecutamos el comando en la consola: python app.py o python3 app.py y revisamos nuestro navegador
@app.route('/')
# @jwt_required()
def index():
    return 'Hola desde gitpod'

######## Usuarios #########

# 7. Ruta para consultar todos los Usuarios
@app.route('/usuarios', methods=['GET'])
def getUsuarios():
    user = Usuario.query.all()
    user = list(map(lambda x: x.serialize(), user))
    return jsonify(user),200

# 12. Ruta para agregar usuario
@app.route('/usuarios', methods=['POST'])
def addUsuario():
    user = Usuario()
    # asignar a variables lo que recibo mediante post
    user.primer_nombre = request.json.get('primer_nombre')
    user.segundo_nombre = request.json.get('segundo_nombre')
    user.apellido_paterno = request.json.get('apellido_paterno')
    user.apellido_materno = request.json.get('apellido_materno')
    user.direccion = request.json.get('direccion')

    Usuario.save(user)

    return jsonify(user.serialize()),200

# 13. Creamos método para consultar un usuario en específico
@app.route('/usuarios/<id>', methods=['GET'])
def getUsuario(id):
    user = Usuario.query.get(id)
    return jsonify(user.serialize()),200

# 14. Borrar usuario en específico
@app.route('/usuarios/<id>', methods=['DELETE'])
def deleteUsuario(id):
    user = Usuario.query.get(id)
    Usuario.delete(user)
    return jsonify(user.serialize()),200

# 15. Modificar Usuario
@app.route('/usuarios/<id>', methods=['PUT'])
def updateUsuario(id):
    user = Usuario.query.get(id)

    user.primer_nombre = request.json.get('primer_nombre')
    user.segundo_nombre = request.json.get('segundo_nombre')
    user.apellido_paterno = request.json.get('apellido_paterno')
    user.apellido_materno = request.json.get('apellido_materno')
    user.direccion = request.json.get('direccion')
    user.email = request.json.get('email')
    user.password = request.json.get('password')

    Usuario.update(user)

    return jsonify(user.serialize()),200

######## Regiones #########
@app.route('/regiones', methods=['GET'])
def getRegiones():
    regiones = Regiones.query.all()
    regiones = list(map(lambda x: x.serialize(), regiones))
    return jsonify(regiones),200

# obtener listado de todas las comunas de la región solicitada
@app.route('/regiones/<id>/comunas', methods=['GET'])
def getComunasByRegion(id):
    comunas = db.session.query(Comunas).filter(Regiones.id == id).filter(Provincias.region_id == id).filter(Comunas.provincia_id == Provincias.id)
    comunas = list(map(lambda x: x.serialize(), comunas))
    # print(comunas)
    return jsonify(comunas),200

######## Provincia #########
@app.route('/provincias', methods=['GET'])
def getProvincias():
    provincias = Provincias.query.all()
    provincias = list(map(lambda x: x.serialize(), provincias))
    return jsonify(provincias),200

######## Comunas #########
@app.route('/comunas', methods=['GET'])
def getComunas():
    comunas = Comunas.query.all()
    comunas = list(map(lambda x: x.serialize(), comunas))
    return jsonify(comunas),200

@app.route('/comunas/<id>', methods=['GET'])
def getComuna(id):
    comuna = Comunas.query.get(id)
    return jsonify(comuna.serialize()),200



######### Clientes #########
@app.route('/clientes', methods=['GET'])
def getClientes():
    clientes = Clientes.query.all()
    clientes = list(map(lambda x: x.serialize(), clientes))
    return jsonify(clientes),200

@app.route('/clientes', methods=['POST'])
def addCliente():
    cliente = Clientes()
    # asignar a variables lo que recibo mediante post
    cliente.nombre = request.json.get('nombre')
    cliente.apellido_paterno = request.json.get('apellido_paterno')
    cliente.apellido_materno = request.json.get('apellido_materno')
    cliente.direccion = request.json.get('direccion')
    cliente.telefono = request.json.get('telefono')
    cliente.email = request.json.get('email')
    cliente.password = request.json.get('password')

    Clientes.save(cliente)

    return jsonify(cliente.serialize()),200

@app.route('/clientes/<id>', methods=['GET'])
def getCliente(id):
    cliente = Clientes.query.get(id)
    return jsonify(cliente.serialize()),200

@app.route('/clientes/<id>', methods=['DELETE'])
def deleteCliente(id):
    cliente = Clientes.query.get(id)
    Clientes.delete(cliente)
    return jsonify(cliente.serialize()),200

@app.route('/clientes/<id>', methods=['PUT'])
def updateCliente(id):
    cliente = Clientes.query.get(id)

    cliente.nombre = request.json.get('nombre')
    cliente.apellido_paterno = request.json.get('apellido_paterno')
    cliente.apellido_materno = request.json.get('apellido_materno')
    cliente.direccion = request.json.get('direccion')
    cliente.telefono = request.json.get('telefono')
    cliente.email = request.json.get('email')
    cliente.password = request.json.get('password')

    Clientes.update(cliente)

    return jsonify(cliente.serialize()),200





# 8. comando para iniciar mi app flask:     flask db init
# 9. comando para migrar mis modelos:       flask db migrate
# 10. comando para crear nuestros modelos como tablas : flask db upgrade
# 11. comando para iniciar la app flask:    flask run

# 4. Configurar los puertos nuestra app
# va al final del código de este archivo
if __name__ == '__main__':
    app.run(port=5000, debug=True)