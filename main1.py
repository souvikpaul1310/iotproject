from flask import Flask, jsonify, make_response
from flask_restful import Api, Resource
import secrets
import os

app = Flask(__name__)
api = Api(app)
auth_key = None

class KeyManager:
    @staticmethod
    def generate_key():
        global auth_key
        auth_key = secrets.token_hex(16)
        return auth_key
    
    @staticmethod
    def get_key():
        global auth_key
        return auth_key

class GenerateKey(Resource):
    def get(self):
        key = KeyManager.generate_key()
        return make_response({'auth_key': key}, 200)

class GetKey(Resource):
    def get(self):
        key = KeyManager.get_key()
        if key:
            return make_response({'auth_key': key}, 200)
        else:
            return make_response({'error': 'No authentication key has been generated'}, 404)

@app.errorhandler(404)
def not_found(error):
    return make_response({'error': 'Not Found'}, 404)

@app.errorhandler(405)
def method_not_allowed(error):
    return make_response({'error': 'Method Not Allowed'}, 405)

@app.errorhandler(500)
def internal_server_error(error):
    return make_response({'error': 'Internal Server Error'}, 500)

api.add_resource(GenerateKey, '/generate_key')
api.add_resource(GetKey, '/get_key')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
