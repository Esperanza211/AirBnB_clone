#!/usr/bin/python3
""" import necessary modules """

from uuid import uuid4
from datetime import datetime
import models



class BaseModel:
    """ BaseModel class """

    def __init__(self, *args, **kwargs):
        """ Constructor for the BaseModel class.
            Args:
                id (str(uuid)): id of the new instance
        """
        if args is not None and len(args) > 0:
            pass
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)
        else:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key == "created_at" or key == "updated_at":
                    value = datetime.fromisoformat(value)
                setattr(self, key, value)

    def __str__(self):
        """ returns [<class name>] (<self.id>) <self.__dict__> """
        ClassName = self.__class__.__name__
        return f"[{ClassName}] ({self.id}) {self.__dict__}"

    def save(self):
        """ updates the public instance attribute updated_at
            with the current datetime """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):

        """Returns a dictionary that contains all
        keys/values of the instance"""
        my_dict = self.__dict__.copy()
        my_dict['updated_at'] = self.updated_at.isoformat()
        my_dict['created_at'] = self.created_at.isoformat()
        my_dict['__class__'] = self.__class__.__name__

    return my_dict
