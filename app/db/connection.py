from flask import current_app, g
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class MongoDBConnection:
    """
    Singleton for managing MongoDB connections within Flask context.

    This class ensures a single instance of MongoClient is used throughout the Flask application
    to manage connections to a MongoDB database. It uses Flask's application context to store
    the connection and the database object, and performs a quick operation to check the connection
    upon initialization.
    """

    def __init__(self):
        """
        Initializes the MongoDBConnection instance.
        """
        pass

    def init_connection(self):
        """
        Initializes the MongoDB connection and stores it in Flask's application context.

        This method creates a MongoClient instance if it doesn't already exist in the
        Flask's global context (`g`). It also checks the connection by running a simple
        `ping` command on the database.

        Raises:
            ConnectionFailure: If the connection to the MongoDB server fails.
        """
        if not hasattr(g, "_mongo_client"):
            try:
                g._mongo_client = MongoClient(
                    host=current_app.config["MONGO_HOST"],
                    port=int(current_app.config["MONGO_PORT"]),
                    username=current_app.config["MONGO_USER"],
                    password=current_app.config["MONGO_PASSWORD"],
                    authSource=current_app.config["MONGO_ADMIN"],
                )
                g._mongo_db = g._mongo_client[current_app.config["DB_NAME"]]
                # Perform a quick operation to check the connection
                g._mongo_db.command("ping")
            except ConnectionFailure as e:
                current_app.logger.error(f"Failed to connect to MongoDB: {str(e)}")
                raise ConnectionFailure(f"Database connection failed: {str(e)}")

    @property
    def db(self):
        """
        Returns the MongoDB database instance.

        If the database instance is not already initialized in Flask's application context (`g`),
        it initializes the connection first.

        Returns:
            Database: The MongoDB database instance.
        """
        if not hasattr(g, "_mongo_db"):
            self.init_connection()
        return g._mongo_db

    @classmethod
    def get_instance(cls):
        """
        Returns the MongoDBConnection instance from Flask's global context.

        If the instance does not already exist in Flask's global context (`g`), it creates one.

        Returns:
            MongoDBConnection: The MongoDBConnection instance.
        """
        if "mongo_connection" not in g:
            g.mongo_connection = cls()
        return g.mongo_connection

    def init_app(self, app):
        """
        Initializes the MongoDB connection when the Flask application context is pushed.

        This method ensures that the MongoDB connection is initialized and stored in the Flask
        application extensions when the application context is available.

        Args:
            app (Flask): The Flask application instance.
        """
        app.extensions["mongo"] = self
        with app.app_context():
            self.init_connection()

        app.logger.info("MongoDB connection initialized")
