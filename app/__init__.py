# app/__init__.py

from flask import Flask
import os
from pathlib import Path
import yaml
from dotenv import load_dotenv
from logger import CustomLogger  # Import your custom logger

# Load environment variables from the project .env file before importing any modules that depend on them
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# Keep both variable names available for compatibility with the rest of the project
if os.getenv('API_KEY') and not os.getenv('GROQ_API_KEY'):
    os.environ['GROQ_API_KEY'] = os.getenv('API_KEY')

from .routes import main as main_blueprint


class AppConfig:
    """Class to handle application configuration."""

    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from config.yaml."""
        with open(BASE_DIR / 'config' / 'config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        # Replace API key placeholder with actual value from environment variables
        if 'api' in config and 'key' in config['api']:
            config['api']['key'] = os.getenv('GROQ_API_KEY') or os.getenv('API_KEY')

        return config


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, template_folder=str(BASE_DIR / 'app' / 'templates'))  # Initialize the Flask app

    # Load configuration
    app_config = AppConfig()
    app.config.update(app_config.config)

    # Set up logging
    logger = CustomLogger().get_logger()  # Initialize your custom logger
    logger.info("Flask application starting...")

    # Import and register routes
    app.register_blueprint(main_blueprint)

    return app