from flask import Flask, make_response, jsonify
import db_session, blueprints
from flask_restful import Api


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# Это одно и то же? типа

@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/accounts.db")
    app.register_blueprint(blueprints.blueprint)
    app.run()


if __name__ == '__main__':
    main()
