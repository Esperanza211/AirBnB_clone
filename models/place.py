#!/usr/bin/python3
"""importing BaseModel"""

from models.base_model import BaseModel


class Place(BaseModel):
    """a place class that inherits from BaseModel"""
    name = ""
    city_id = ""
    user_id = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guests = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
