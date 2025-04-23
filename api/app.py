from flask import Flask
from flask_jwt_extended import JWTManager
from .routes.auth_routes import auth_bp
from .routes.data_routes import data_bp
from .routes.crawler_routes import crawler_bp

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "236278"
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(crawler_bp, url_prefix="/crawler")
app.register_blueprint(data_bp, url_prefix="/data")


if __name__ == "__main__":
    app.run(debug=True)