#!/usr/bin/python3
"""Command interpreter for the HBNB project"""

import cmd

class HBNBCommand(cmd.Cmd):
    """Command interpreter for AirBnB clone"""
    prompt = "(hbnb) "  # Custom prompt

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()  # Prints a new line for clean exit
        return True

    def emptyline(self):
        """Overrides the empty line + ENTER behavior to do nothing."""
        pass

if __name__ == '__main__':
    HBNBCommand().cmdloop()
