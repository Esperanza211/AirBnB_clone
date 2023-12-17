#!/usr/bin/python3
"""importing BaseModel"""

from models.base_model import BaseModel


class State(BaseModel):
    """ a state class that inherits from BaseModel"""
    name = ""
