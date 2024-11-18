#!/usr/bin/python3
import json
from models.base_model import BaseModel
import os
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

classes = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Place": Place,
    "Amenity": Amenity,
    "Review": Review,
}

class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON file to instances."""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary of stored objects."""
        if cls is None:
            return self.__objects
        else:
            return {
                key: obj for key, obj in self.__objects.items()
                if obj.__class__.__name__ == cls
            }

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file."""
        obj_dict = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes the JSON file to __objects if it exists."""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r') as f:
                obj_dict = json.load(f)
                for key, value in obj_dict.items():
                    class_name = key.split('.')[0]
                    if class_name in classes:
                        self.__objects[key] = classes[class_name](**value)

    def delete(self, obj=None):
        """Deletes an object from __objects."""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]

