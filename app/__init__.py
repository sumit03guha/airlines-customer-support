"""
Module to initialize the Flask application and register namespaces.
"""

from flask import Flask
from flask_restx import Api

from .api.booking import Booking, BookingList, BookingVAS
from .api.booking import ns as booking_ns
from .db.connection import MongoDBConnection
from .db.repository import BookingRepository
from .models.booking import booking_model, vas_model


def create_app(app_config) -> Flask:
    """
    Create and configure the Flask application.

    Returns:
        app: Configured Flask application instance.
    """

    app = Flask(__name__)
    api = Api(
        app,
        version="1.0",
        title="Airline Customer Support API",
        description="APIs for airline customer support",
    )

    app.config.from_object(app_config)

    # Register models
    api.models[booking_model.name] = booking_model
    api.models[vas_model.name] = vas_model

    # Initialize MongoDB
    mongo_conn = MongoDBConnection()
    mongo_conn.init_app(app)

    # Initialize repositories
    booking_repo = BookingRepository()

    # Add namespaces with repositories
    api.add_namespace(booking_ns)
    booking_ns.add_resource(
        BookingList, "/", resource_class_kwargs={"repo": booking_repo}
    )
    booking_ns.add_resource(
        Booking,
        "/<string:pnr>/<string:last_name>",
        resource_class_kwargs={"repo": booking_repo},
    )
    booking_ns.add_resource(
        BookingVAS,
        "/<string:pnr>/<string:last_name>/vas",
        resource_class_kwargs={"repo": booking_repo},
    )

    return app
