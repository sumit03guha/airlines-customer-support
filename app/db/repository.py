"""
Module to define repository classes for interacting with the database.
"""

from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from .connection import MongoDBConnection


class BookingRepository:
    """
    Repository class for managing bookings in MongoDB.
    """

    def __init__(self):
        """
        Initializes the AuthRepository without connecting to the database.
        The connection is established when needed.
        """
        self._db = None

    @property
    def db_connection(self):
        if self._db is None:
            self._db = MongoDBConnection.get_instance().db
        return self._db

    def create_booking(self, booking) -> str:
        """
        Create a new booking.

        Args:
            booking (dict): Booking data.

        Returns:
            str: ID of the created booking.
        """
        result: InsertOneResult = self.db_connection.bookings.insert_one(booking)
        return str(result.inserted_id)

    def find_booking(self, pnr, last_name):
        """
        Find a booking by PNR and last name.

        Args:
            pnr (str): PNR of the booking.
            last_name (str): Last name of the customer.

        Returns:
            dict: Booking data.
        """
        return self.db_connection.bookings.find_one(
            {"pnr": pnr, "last_name": last_name}
        )

    def update_booking(self, pnr, last_name, updated_data) -> int:
        """
        Update a booking by PNR and last name.

        Args:
            pnr (str): PNR of the booking.
            last_name (str): Last name of the customer.
            updated_data (dict): Updated booking data.

        Returns:
            int: Number of matched documents.
        """
        result: UpdateResult = self.db_connection.bookings.update_one(
            {"pnr": pnr, "last_name": last_name}, {"$set": updated_data}
        )
        return result.matched_count

    def delete_booking(self, pnr, last_name) -> int:
        """
        Delete a booking by PNR and last name.

        Args:
            pnr (str): PNR of the booking.
            last_name (str): Last name of the customer.

        Returns:
            int: Number of deleted documents.
        """
        result: DeleteResult = self.db_connection.bookings.delete_one(
            {"pnr": pnr, "last_name": last_name}
        )
        return result.deleted_count

    def add_vas(self, pnr, last_name, new_vas) -> int:
        """
        Add value-added services to a booking.

        Args:
            pnr (str): PNR of the booking.
            last_name (str): Last name of the customer.
            new_vas (list): List of new value-added services.

        Returns:
            int: Number of matched documents.
        """
        result: UpdateResult = self.db_connection.bookings.update_one(
            {"pnr": pnr, "last_name": last_name},
            {"$addToSet": {"vas": {"$each": new_vas}}},
        )
        return result.matched_count
