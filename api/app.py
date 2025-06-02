import os
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from .routes.auth_routes import auth_bp
from .routes.data_routes import data_bp
from .routes.crawler_routes import crawler_bp
from dotenv import load_dotenv
from flasgger import Swagger
from dashboard.routes import dashboard_bp

load_dotenv()

app = Flask(__name__)

# Configuração JWT para API
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_secret_key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)

# Configuração para sessão do Flask (necessário para autenticação do dashboard)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dashboard_secret_key")
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=2)

app.config['SWAGGER'] = {
    'title': 'API Pública Embrapa',
    'uiversion': 3
}
swagger = Swagger(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(crawler_bp, url_prefix="/crawler")
app.register_blueprint(data_bp, url_prefix="/data")
app.register_blueprint(dashboard_bp, url_prefix="")


# if __name__ == "__main__":
#     app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
