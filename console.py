#!/usr/bin/python3

"""
Import necessary modules
"""

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

class_home = {
    "BaseModel": BaseModel,
    "User": User,
    "Place": Place,
    "Amenity": Amenity,
    "City": City,
    "Review": Review,
    "State": State
}


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb)"

    def do_EOF(self, line):
        "Signal to exit the program using CTRL+D"
        return True

    def do_quit(self, line):
        "Quit command to exit the program\n"
        return True

    def emptyline(self):
        """Overwriting the emptyline method"""
        return False

    def do_create(self, line):
        """Creates a new instance of a class"""
        if line:
            try:
                glo_cls = globals().get(line, None)
                obj = glo_cls()
                obj.save()
                print(obj.id)  # print the id
            except Exception:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_show(self, line):
        """Show <class> <instance id>\nShows the class created"""
        if not line:
            print("** class name missing **")
            return
        Class = line.split()[0]
        Class = globals().get(Class)
        if not Class or not issubclass(Class, BaseModel):
            print("** class doesn't exist **")
            return
        if len(line.split()) != 2:
            print("** instance id missing **")
            return
        all_obj = {}
        search_id = f"{line.split()[0]}.{line.split()[1]}"
        fileName = FileStorage._FileStorage__file_path
        if os.path.exists(fileName) and os.path.isfile(fileName):
            with open(fileName, 'r') as file:
                all_obj = json.load(file)
        for key, value in all_obj.items():
            if key == search_id:
                class_name, obj_id = key.split(".")
                obj_dict = value
                obj_dict.pop('__class__', None)
                print(f"[{class_name}] ({obj_id}) {obj_dict}")
                return
        print("** no instance found **")

    def do_destroy(self, line):
        """Destroy <class> <isntance id>\nDeletes an inst of the class & id"""
        parts = line.split()
        if len(parts) < 1:
            print("** class name missing **")
            return
        class_name = parts[0]
        obj_id = parts[1] if len(parts) > 1 else None
        Class = globals().get(class_name)
        if not Class or not issubclass(Class, BaseModel):
            print("** class doesn't exist **")
            return
        if not obj_id:
            print("** instance id missing **")
            return
        all_obj = {}
        search_id = f"{class_name}.{obj_id}"
        fileName = FileStorage._FileStorage__file_path
        if os.path.exists(fileName) and os.path.isfile(fileName):
            with open(fileName, "r") as file:
                all_obj = json.load(file)
                if search_id not in all_obj:
                    print("** no instance found **")
                    return
                del all_obj[search_id]
                objects = FileStorage._FileStorage__objects
                del objects[search_id]
                with open(fileName, "w") as file:
                    json.dump(all_obj, file)
                    return
        print("** no instance found **")

    def do_all(self, line):
        """Print all instances in string representation"""
        objects = []
        if line == "":
            print([str(value) for key, value in storage.all().items()])
        else:
            st = line.split(" ")
            if st[0] not in class_home:
                print("** class doesn't exist **")
            else:
                for key, value in storage.all().items():
                    clas = key.split(".")
                    if clas[0] == st[0]:
                        objects.append(str(value))
                print(objects)

    def do_update(self, line):
        """
        Usage : update <class> <id> <attribute name> <attribute value>
        Usage : <class name>.update(<id>, <attribute name>, <attribute value>)
        Usage : <class name>.update(<id>, <dictionary representation>)
        Updates an instance based on the class name
        and id by adding or updating attribute
        """
        if not line:
            print("** class name missing **")
            return
        Class = line.split()[0]
        Class = globals().get(Class)
        if not Class or not issubclass(Class, BaseModel):
            print("** class doesn't exist **")
            return
        if len(line.split()) < 2:
            print("** instance id missing **")
            return
        if len(line.split()) < 3:
            print("** attribute name missing **")
            return
        if len(line.split()) < 4:
            print("** value missing **")
            return
        all_obj = {}
        search_id = f"{line.split()[0]}.{line.split()[1]}"
        pat = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
        if not re.match(pat, search_id.split(".")[1]):
            print("** no instance found **")
            return
        attrib_name = line.split()[2]
        att_value = line.split()[3].strip('"')
        fileName = FileStorage._FileStorage__file_path
        if os.path.exists(fileName) and os.path.isfile(fileName):
            with open(fileName, 'r') as file:
                all_obj = json.load(file)
                if search_id not in all_obj:
                    print("** no instance found **")
                    return
        value = all_obj[search_id]
        if attrib_name in value:
            try:
                a_type = type(attrib_name).__name__
                att_value = ast.literal_eval(a_type + "('" + att_value + "')")
            except (ValueError, SyntaxError):
                pass
            value[attrib_name] = att_value
        else:
            value[attrib_name] = att_value
        with open(fileName, "w") as file:
            json.dump(all_obj, file)

    def do_count(self, line):
        """Print the count all class instances"""
        kclass = globals().get(line, None)
        if kclass is None:
            print("** class doesn't exist **")
            return
        count = 0
        for obj in storage.all().values():
            if obj.__class__.__name__ == line:
                count += 1
        print(count)

    def default(self)
