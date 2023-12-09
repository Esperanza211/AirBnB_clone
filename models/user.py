#!/usr/bin/python3
""" import necessary modules """

from models.base_model import BaseModel

""" User calss that inherits from BaseModel """


class User(BaseModel):
    """ User calss that inherits from BaseModel """
    email = ""
    password = ""
    first_name = ""
    last_name = ""

   