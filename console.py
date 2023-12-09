#!/usr/bin/python3
""" Import necessary modules """

import cmd
import os
import re
import sys
import ast
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage
from uuid import uuid4
""" HBNBCommand class for cmd module """


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb)"

    def do_EOF(self, line):
        """Signal to exit the program using CTRL+D"""
        return True

    def do_quit(self, line):
        """Quit command to exit the program\n"""
        return True

    def emptyline(self):
        """This method is called when an empty line is entered"""
        pass

    def do_create(self, line):
        """create <class>\ncreate a new instance"""
        if len(line.split()) != 1:
            print("* class name missing *")
            return
        class_name = line.split()[0]
        model_class = globals().get(class_name)
        if model_class and issubclass(model_class, BaseModel):
            new_instance = model_class()
            new_instance.save()
            print(new_instance.id)
        else:
            print("* class doesn't exist *")

    def do_show(self, line):
        """show <class> <instance id>\nshows the class created"""
        if not line:
            print("* class name missing *")
            return
        class_name = line.split()[0]
        model_class = globals().get(class_name)
        if not model_class or not issubclass(model_class, BaseModel):
            print("* class doesn't exist *")
            return
        if len(line.split()) != 2:
            print("* instance id missing *")
            return
        all_objects = FileStorage._FileStorage__objects
        search_id = f"{class_name}.{line.split()[1]}"
        if search_id in all_objects:
            obj = all_objects[search_id]
            print(obj)
        else:
            print("* no instance found *")

    # Other methods are unchanged

if _name_ == '__main__':
    HBNBCommand().cmdloop()
