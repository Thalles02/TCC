from flask import Flask
from src.main.routes.routes import api_route_bp
from src.main.routes.application import app_route_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(api_route_bp)
app.register_blueprint(app_route_bp)
