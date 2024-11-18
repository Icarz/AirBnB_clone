#!/usr/bin/python3
import cmd
import json
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter for AirBnB clone"""
    prompt = "(hbnb) "

    classes = {
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
        """Overrides empty line behavior to do nothing"""
        pass

    def do_create(self, arg):
        """Create a new instance of a class"""
        if not arg:
            print("** class name missing **")
            return
        if arg not in self.classes:
            print("** class doesn't exist **")
            return
        new_instance = self.classes[arg]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Show an instance based on class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
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
        """Delete an instance based on class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
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
<<<<<<< HEAD
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
=======
        """Show all instances, or all instances of a specific class"""
        if arg and arg not in self.classes:
            print("** class doesn't exist **")
            return
        instances = storage.all()
        if arg:
            print([str(obj) for key, obj in instances.items() if key.startswith(arg)])
        else:
            print([str(obj) for obj in instances.values()])
>>>>>>> 651932ad71584304a4420bf6e10cb4553afebee1

    def do_update(self, arg):
        """Update an instance by adding or updating attributes"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
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
        if hasattr(instance, attr_name):
            attr_type = type(getattr(instance, attr_name))
            setattr(instance, attr_name, attr_type(attr_value))
        else:
            setattr(instance, attr_name, attr_value)
        instance.save()

    def do_count(self, arg):
        """Count the number of instances of a class"""
        if not arg:
            print("** class name missing **")
            return
        if arg not in self.classes:
            print("** class doesn't exist **")
            return
        count = sum(1 for key in storage.all() if key.startswith(arg))
        print(count)

    def default(self, line):
        """Handle <class name>.<command> syntax"""
        args = line.split('.', 1)
        if len(args) != 2:
            print(f"*** unknown syntax: {line}")
            return
        class_name, rest = args
        if class_name not in self.classes:
            print(f"*** unknown class: {class_name}")
            return

        try:
            command, params = rest.split('(', 1)
            params = params[:-1]  # Remove closing parenthesis

            # Pre-process params to remove quotes
            params = params.replace('"', '')  # Remove all double quotes

            if command == "all":
                self.do_all(class_name)
            elif command == "count":
                self.do_count(class_name)
            elif command == "show":
                self.do_show(f"{class_name} {params}")
            elif command == "destroy":
                self.do_destroy(f"{class_name} {params}")
            elif command == "update":
                if params.startswith("{") and params.endswith("}"):
                    instance_id, attr_dict = params.split(", ", 1)
                    attr_dict = json.loads(attr_dict)
                    for key, value in attr_dict.items():
                        self.do_update(f"{class_name} {instance_id.strip()} {key} {value}")
                else:
                    instance_id, attr_name, attr_value = params.split(", ")
                    self.do_update(f"{class_name} {instance_id.strip()} {attr_name.strip()} {attr_value.strip()}")
            else:
                print(f"*** unknown syntax: {line}")
        except Exception:
            print(f"*** unknown syntax: {line}")


if __name__ == '__main__':
    HBNBCommand().cmdloop()

