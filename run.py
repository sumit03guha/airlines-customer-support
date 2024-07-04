"""
Main entry point for running the Flask application.
"""

from flask import Flask

from app import create_app
from app.config.config import get_config

app_config = get_config()

app: Flask = create_app(app_config)

if __name__ == "__main__":
    app.run(debug=True)
