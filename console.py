#!/usr/bin/python3
"""Command interpreter for the HBNB project"""

import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter for AirBnB clone"""
    prompt = "(hbnb) "
    
    # Valid classes for the command interpreter
    valid_classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def emptyline(self):
        """Overrides the empty line + ENTER behavior to do nothing."""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it, and prints the id."""
        if not arg:
            print("** class name missing **")
            return
        if arg not in self.valid_classes:
            print("** class doesn't exist **")
            return
        new_instance = self.valid_classes[arg]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance based on class name and id."""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        instance = storage.all().get(key)
        if not instance:
            print("** no instance found **")
            return
        print(instance)

    def do_destroy(self, arg):
        """Deletes an instance based on class name and id."""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """Prints all string representations of all instances based on class name or all classes."""
        if arg.endswith(".all()"):
            # Extract the class name before .all()
            class_name = arg[:-5]
            
            # Validate the class name
            if class_name not in self.valid_classes:
                print("** class doesn't exist **")
                return
            
            # Get all instances of the class
            class_type = self.valid_classes[class_name]
            instances = storage.all(class_type)
            
            # If no instances are found, print a message
            if not instances:
                print("** no instances found **")
            else:
                # Print all instances of that class
                print([str(instance) for instance in instances.values()])
        else:
            # If no argument is passed, print all instances from all classes
            if not arg:
                instances = storage.all()
                print([str(instance) for instance in instances.values()])
            else:
                # If a class name is provided, print instances of that class
                if arg not in self.valid_classes:
                    print("** class doesn't exist **")
                    return
                instances = storage.all()
                class_instances = [str(instance) for key, instance in instances.items() if key.startswith(arg)]
                if not class_instances:
                    print("** no instances found **")
                else:
                    print(class_instances)

    def do_update(self, arg):
        """Updates an instance by adding or updating an attribute."""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        instance = storage.all().get(key)
        if not instance:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attr_name = args[2]
        attr_value = args[3].strip('"')

        # Handle attribute type casting
        if hasattr(instance, attr_name):
            attr_type = type(getattr(instance, attr_name))
            setattr(instance, attr_name, attr_type(attr_value))
        else:
            setattr(instance, attr_name, attr_value)
        instance.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()

