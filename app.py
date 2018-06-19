from flask import Flask, request, jsonify, redirect
from flask_pymongo import PyMongo

from werkzeug.security import generate_password_hash, check_password_hash

from bson import json_util

from config import MONGO_URI

app = Flask(__name__)
app.config['MONGO_URI'] = MONGO_URI
app.config['DEBUG'] = True

app_context = app.app_context()
app_context.push()

mongo = PyMongo(app)

col_users = mongo.db.users
col_questions = mongo.db.questions

@app.route('/v1/users', methods=['GET'])
def index():
    res = col_users.find({})
    return json_util.dumps(list(res)), 200
    


@app.route('/v1/users', methods=['POST'])
def create_user():
    data = request.get_json()
    data['password'] = generate_password_hash(data['password'])
    if (col_users.find_one({'username':data['username'] })):
       return 'Usuario ja Cadastrado...',203
    else:
       col_users.insert_one(data)
    return 'usuario ' + data['username'] + ' criado.', 201

@app.route('/v1/users/<username>', methods=['GET'])
def get_user(username):
    return username, 200


# rota para exemplificar como utilizar obter variaveis
# de url. teste acessando 
# http://localhost:8088/questions/search?disciplina=BancoDeDados 
@app.route('/questions/search', methods=['GET'])
def search():
    disciplina = request.args.get('disciplina')
    return disciplina, 200
