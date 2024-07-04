"""
Module to define data models for the API.
"""

from flask_restx import Model, fields

# Booking data model
booking_model = Model(
    "Booking",
    {
        "pnr": fields.String(readonly=True, description="The booking PNR"),
        "customer_name": fields.String(required=True, description="Customer name"),
        "last_name": fields.String(required=True, description="Customer last name"),
        "flight_number": fields.String(required=True, description="Flight number"),
        "departure_date": fields.String(required=True, description="Departure date"),
        "status": fields.String(required=True, description="Booking status"),
        "vas": fields.List(fields.String, description="Value Added Services"),
    },
)

# VAS (Value Added Services) data model
vas_model = Model(
    "VAS",
    {
        "vas": fields.List(
            fields.String, required=True, description="Value Added Services"
        )
    },
)
