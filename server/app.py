from flask import Flask
from flask_cors import CORS

from server.routes.users import users_bp


def create_app():
    app = Flask(__name__)

    CORS(app, origins=["http://localhost:5173"])

    app.register_blueprint(users_bp, url_prefix="/users")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
