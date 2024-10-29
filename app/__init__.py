# Necessary imports
import os
from flask import Flask
from .routes import main_bp

# Function to initialize application 
def create_app():
    # Initialize application
    app = Flask(__name__)

    # Initialize environment variable
    app.secret_key = os.getenv('APP_SECRET_KEY')
    
    # Load configuration for application
    # app.config.from_object('config.Config')

    # Register blueprints and initialize routes
    app.register_blueprint(main_bp)

    # Return application
    return app