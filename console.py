#!/usr/bin/python3
""" import necessary modules """

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
""" HBNBCommand class for cmd moudule """


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.
    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def do_EOF(self, line):
        "signal to exit the program using CTRL+D"
        return True

    def do_quit(self, line):
        "Quit command to exit the program\n"
        return True

    def emptyline(self):
        """ this method that is called when an empty line is entered """
        pass

    def do_create(self, line):
        """create <class>\ncreate a new instance"""
        if len(line.split()) != 1:
            print("** class name missing **")
            return
        Class = line.split()[0]
        Class = globals().get(Class)
        if Class and issubclass(Class, BaseModel):
            my_model = Class()
            my_model.save()
            print(my_model.id)
        else:
            print("** class doesn't exist **")

    def do_show(self, line):
        """show <class> <instance id>\nshows the class created
        """
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
        """destroy <class> <isntance id>
deletes an instance based on the class name and id
(save the change into the JSON file)"""
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
        """
        all or all <class>
all : show all instances created for all classes
all <class> : show all instances for specific class

        """
        if line:
            Class = line.split()[0]
            Class = globals().get(Class)
            if not Class or not issubclass(Class, BaseModel):
                print("** class doesn't exist **")
                return
        all_obj = {}
        fileName = FileStorage._FileStorage__file_path
        if os.path.exists(fileName) and os.path.isfile(fileName):
            with open(fileName, 'r') as file:
                all_obj = json.load(file)
        print("[", end='')
        is_first = True
        for key, value in all_obj.items():
            class_name, obj_id = key.split(".")
            obj_dict = value
            obj_dict.pop('__class__', None)
            if line and line.split()[0] != class_name:
                continue
            if not is_first:
                print(", ", end='')
            print(f"\"[{class_name}] ({obj_id}) {obj_dict}\"", end='')
            is_first = False
        print("]")

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
        """
        Usage : <class name>.count().
command to retrieve the number of instances of a class
        """
        if line:
            ClassName = line.split()[0]
            Class = globals().get(ClassName)
            if not Class or not issubclass(Class, BaseModel):
                print("** class doesn't exist **")
                return
        objects = FileStorage._FileStorage__objects
        c = 0
        for key, value in objects.items():
            Class_Name = key.split(".")[0]
            if Class_Name == ClassName:
                c += 1
        print(c)

    def default(self, line):
        """Default behavior for cmd module when input is invalid"""
        linedict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", line)
        if match is not None:
            linel = [line[:match.span()[0]], line[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", linel[1])
            if match is not None:
                command = [linel[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in linedict.keys():
                    call = "{} {}".format(linel[0], command[1])
                    return linedict[command[0]](call)
        print("*** Unknown syntax: {}".format(line))
        return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
