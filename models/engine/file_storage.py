#!/usr/bin/python3
""" import json and os modules """

import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
""" FileStorage calss """


class FileStorage:
    """ FileStorage class """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ returns the dictionary __objects """
        return (FileStorage.__objects)

    def new(self, obj):
        """ sets in __objects the obj with key <obj class name>.id """
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """ serializes __objects to the JSON file (path: __file_path)"""
        tmp = {}
        for key, value in FileStorage.__objects.items():
            tmp[key] = value.to_dict()
        with open(FileStorage.__file_path, 'w') as file:
            json.dump(tmp, file)

    def reload(self):
        """ deserializes the JSON file to __objects (only if the JSON file
        (__file_path) exists ; otherwise, do nothing.If the file doesn’t exist
        no exception should be raised)"""
        fileName = FileStorage.__file_path
        if os.path.exists(fileName) and os.path.isfile(fileName):
            with open(fileName, 'r') as file:
                tmp_1 = json.load(file)
            for key, value in tmp_1.items():
                ClassName = value.get('__class__')
                if ClassName:
                    class_obj = globals()[ClassName]
                    obj = class_obj(**value)
                    self.new(obj)
