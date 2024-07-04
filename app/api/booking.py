"""
Module to define API endpoints for booking operations.
"""

import random
import string

from flask import request
from flask_restx import Namespace, Resource

from app.db.repository import BookingRepository

from ..models.booking import booking_model, vas_model

# Namespace for booking operations
ns = Namespace("bookings", description="Booking operations")


def generate_pnr():
    """
    Generate a unique PNR.

    Returns:
        str: Generated PNR.
    """
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


@ns.route("/")
class BookingList(Resource):
    """
    Resource class for creating a new booking.
    """

    @ns.doc("create_booking")
    @ns.expect(booking_model)
    @ns.marshal_with(booking_model, code=201)
    def post(self):
        """
        Create a new booking.

        Returns:
            dict: Created booking data.
            int: HTTP status code 201.
        """
        new_booking = request.json
        new_booking["pnr"] = generate_pnr()
        new_booking["status"] = "confirmed"
        new_booking["vas"] = []
        BookingRepository().create_booking(new_booking)

        return new_booking, 201


@ns.route("/<string:pnr>/<string:last_name>")
@ns.response(404, "Booking not found")
class Booking(Resource):
    """
    Resource class for fetching, modifying, and deleting a booking.
    """

    @ns.doc("get_booking")
    @ns.marshal_with(booking_model)
    def get(self, pnr, last_name):
        """
        Fetch a booking given its PNR and last name.

        Args:
            pnr (str): PNR of the booking.
            last_name (str): Last name of the customer.

        Returns:
            dict: Booking data.
        """
        booking = BookingRepository().find_booking(pnr, last_name)
        if booking is None:
            ns.abort(404, "Booking not found")

        return booking

    @ns.doc("modify_booking")
    @ns.expect(booking_model)
    @ns.marshal_with(booking_model)
    def patch(self, pnr, last_name):
        """
        Modify a booking given its PNR and last name.

        Args:
            pnr (str): PNR of the booking.
            last_name (str): Last name of the customer.

        Returns:
            dict: Updated booking data.
        """
        updated_data = request.json
        if BookingRepository().update_booking(pnr, last_name, updated_data) == 0:
            ns.abort(404, "Booking not found")
        booking = BookingRepository().find_booking(pnr, last_name)

        return booking

    @ns.doc("delete_booking")
    @ns.response(204, "Booking deleted")
    def delete(self, pnr, last_name):
        """
        Cancel a booking given its PNR and last name.

        Args:
            pnr (str): PNR of the booking.
            last_name (str): Last name of the customer.

        Returns:
            str: Empty string.
            int: HTTP status code 204.
        """
        if BookingRepository().delete_booking(pnr, last_name) == 0:
            ns.abort(404, "Booking not found")

        return "", 204


@ns.route("/<string:pnr>/<string:last_name>/vas")
@ns.response(404, "Booking not found")
class BookingVAS(Resource):
    """
    Resource class for adding value-added services (VAS) to a booking.
    """

    @ns.doc("add_vas")
    @ns.expect(vas_model)
    @ns.marshal_with(booking_model)
    def post(self, pnr, last_name):
        """
        Add VAS to a booking given its PNR and last name.

        Args:
            pnr (str): PNR of the booking.
            last_name (str): Last name of the customer.

        Returns:
            dict: Updated booking data.
        """
        new_vas = request.json.get("vas", [])
        if BookingRepository().add_vas(pnr, last_name, new_vas) == 0:
            ns.abort(404, "Booking not found")
        booking = BookingRepository().find_booking(pnr, last_name)

        return booking
