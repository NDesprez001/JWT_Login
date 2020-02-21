"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_jwt_simple import JWTManager, create_jwt, jwt_required
from utils import APIException, generate_sitemap
from models import db, Users
import seeds
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['JWT_SECRET_KEY'] = os.environ.get('USER_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/login', methods=['POST', 'GET'])
def handle_login():
    return seeds.run()

@app.route('/profile', methods=['POST'])
def user_login():
    return jsonify(create_jwt(identity='email'))
    
    json = request.get_json()
    user = Users.query.filter_by(
        username = json["username"],
        email = json["email"]
    ).first()
    if user is None:
        return 'User not found', 404
@app.route('/salute')
@jwt_required
def salute():
    return 'Hello World'


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
