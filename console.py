#!/usr/bin/python3
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
        """Creates a new instance of a class, saves it, and prints the id."""
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
        """Shows an instance based on class name and id."""
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
        """Prints all string representations of instances, or all instances of a class."""
        if not arg:
            instances = storage.all()
            print([str(obj) for obj in instances.values()])
        else:
            if arg not in self.valid_classes:
                print("** class doesn't exist **")
                return
            instances = [
                str(obj) for key, obj in storage.all().items()
                if key.startswith(arg)
            ]
            print(instances)

    def do_count(self, class_name):
        """Counts the number of instances of a specific class."""
        if class_name not in self.valid_classes:
            print("** class doesn't exist **")
            return
        count = sum(1 for key in storage.all() if key.startswith(class_name))
        print(count)

    def default(self, line):
        """
        Overrides default behavior to handle <class name>.<command>(<id>, <attribute>, <value>) and similar patterns.
        """
        args = line.split('.', 1)
        if len(args) != 2:
            print(f"*** unknown syntax: {line}")
            return

        class_name, rest = args
        if class_name not in self.valid_classes:
            print(f"*** unknown class: {class_name}")
            return

        try:
            # Handle cases like <command>(<id>, <attribute>, <value>)
            if '(' in rest and ')' in rest:
                command, params = rest.split('(', 1)
                params = params[:-1]  # Remove closing parenthesis
                params = params.split(", ")

                # Remove the quotes from the parameters
                params = [p.strip('\"') for p in params]

                if command == "all":
                    self.do_all(class_name)
                elif command == "count":
                    self.do_count(class_name)
                elif command == "show":
                    self.do_show(f"{class_name} {params[0]}")
                elif command == "destroy":
                    self.do_destroy(f"{class_name} {params[0]}")
                elif command == "update":
                    if len(params) < 3:
                        print("** attribute value missing **")
                        return
                    obj_id = params[0]  # Already cleaned
                    attr_name = params[1]
                    attr_value = params[2]
                    self.do_update(f"{class_name} {obj_id} {attr_name} {attr_value}")
                else:
                    print(f"*** Unknown syntax: {line}")
            else:
                print(f"*** Unknown syntax: {line}")
        except ValueError:
            print(f"*** unknown syntax: {line}")

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

