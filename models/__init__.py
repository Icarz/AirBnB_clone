#!/usr/bin/python3
from models.engine.file_storage import FileStorage

# Create a single instance of FileStorage
storage = FileStorage()

# Load data from the storage file if it exists
storage.reload()
