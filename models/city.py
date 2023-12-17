#!/usr/bin/python3
"""importing BsaeModel"""

from models.base_model import BaseModel


class City(BaseModel):
    """a city class that inherits from BaseModel"""
    state_id = ""
    name = ""
