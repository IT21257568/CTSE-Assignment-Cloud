from flask import Flask
from config import Config
from database import mongo
from app.routes.booking_routes import booking_bp
from app.routes.test_routes import test_routes
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # initialize PyMongo
    mongo.init_app(app)

    # registering blueprints
    app.register_blueprint(booking_bp, url_prefix="/api/booking")
    app.register_blueprint(test_routes, url_prefix='/test')

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
