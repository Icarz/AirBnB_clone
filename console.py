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
        """Show all instances, or all instances of a specific class"""
        if arg and arg not in self.classes:
            print("** class doesn't exist **")
            return
        instances = storage.all()
        if arg:
            print([str(obj) for key, obj in instances.items() if key.startswith(arg)])
        else:
            print([str(obj) for obj in instances.values()])

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
            params = params.rstrip(')')  # Remove closing parenthesis

            if command == "all":
                self.do_all(class_name)
            elif command == "count":
                self.do_count(class_name)
            elif command == "show":
                param = params.strip('"')  # Precompute the stripped value
                self.do_show(f"{class_name} {param}")
            elif command == "destroy":
                param = params.strip('"')  # Precompute the stripped value
                self.do_destroy(f"{class_name} {param}")
            elif command == "update":
                if params.startswith("{") and params.endswith("}"):
                    instance_id, attr_dict = params.split(", ", 1)
                    instance_id = instance_id.strip('"')  # Precompute the stripped value
                    attr_dict = json.loads(attr_dict)
                    for key, value in attr_dict.items():
                        self.do_update(f"{class_name} {instance_id} {key} {value}")
                else:
                    instance_id, attr_name, attr_value = params.split(", ")
                    instance_id = instance_id.strip('"')  # Precompute the stripped value
                    attr_name = attr_name.strip('"')
                    attr_value = attr_value.strip('"')
                    self.do_update(f"{class_name} {instance_id} {attr_name} {attr_value}")
            else:
                print(f"*** unknown syntax: {line}")
        except Exception as e:
            print(f"*** unknown syntax: {line}")


if __name__ == '__main__':
    HBNBCommand().cmdloop()

