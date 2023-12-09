#!/usr/bin/python3
"""importing BaseModel"""

from models.base_model import BaseModel


class Review(BaseModel):
    """a review class that inherits from BaseModel"""
    place_id = ""
    user_id = ""
    text = ""
