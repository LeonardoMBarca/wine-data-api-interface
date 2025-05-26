from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flasgger import swag_from

auth_bp = Blueprint("auth", __name__)

USERS = {
    "user": "user"
}

@auth_bp.route("/login", methods=["POST"])
@swag_from({
    'tags': ['Autenticação'],
    'summary': 'Login do usuário',
    'description': 'Retorna um token JWT válido com base no nome de usuário e senha.',
    'consumes': ['application/json'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'example': 'user'},
                    'password': {'type': 'string', 'example': 'user'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Token JWT gerado com sucesso',
            'examples': {
                'application/json': {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                }
            }
        },
        401: {
            'description': 'Credenciais inválidas'
        }
    }
})
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username in USERS and USERS[username] == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Credenciais inválidas"}), 401
