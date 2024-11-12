#!/usr/bin/python3
"""Tests 'Base Model' module"""
import unittest
from models.base_model import BaseModel
from datetime import datetime

class TestBaseModel(unittest.TestCase):
    """Test case for the BaseModel module"""

    def test_isinstance(self):
        """Tests if instances are correctly of type BaseModel."""
        base = BaseModel()
        self.assertIsInstance(base, BaseModel)

    def test_attrs(self):
        """Tests for existence and types of attributes."""
        base = BaseModel()
        self.assertIn('id', base.__dict__)
        self.assertIn('created_at', base.__dict__)
        self.assertIn('updated_at', base.__dict__)
        self.assertIsInstance(base.id, str)
        self.assertIsInstance(base.created_at, datetime)
        self.assertIsInstance(base.updated_at, datetime)

    def test_save(self):
        """Tests that save method updates 'updated_at' timestamp."""
        base = BaseModel()
        old_updated_at = base.updated_at
        base.save()
        new_updated_at = base.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertTrue(new_updated_at > old_updated_at)

    def test_str(self):
        """Tests the string representation of the instance."""
        base = BaseModel()
        expected_str = f"[BaseModel] ({base.id}) {base.__dict__}"
        self.assertEqual(str(base), expected_str)

    def test_attrs_types(self):
        """Tests the data types of BaseModel attributes."""
        base = BaseModel()
        self.assertIsInstance(base.id, str)
        self.assertIsInstance(base.created_at, datetime)
        self.assertIsInstance(base.updated_at, datetime)

    def test_to_dict(self):
        """Tests that to_dict method returns a correct dictionary."""
        base = BaseModel()
        base_dict = base.to_dict()
        
        # Ensure the dictionary has required keys
        self.assertIn('id', base_dict)
        self.assertIn('created_at', base_dict)
        self.assertIn('updated_at', base_dict)
        self.assertIn('__class__', base_dict)

        # Check types in dictionary
        self.assertEqual(base_dict['__class__'], 'BaseModel')
        self.assertIsInstance(base_dict['created_at'], str)
        self.assertIsInstance(base_dict['updated_at'], str)
        self.assertEqual(base_dict['id'], base.id)
        
        # Check ISO format for created_at and updated_at
        try:
            datetime.fromisoformat(base_dict['created_at'])
            datetime.fromisoformat(base_dict['updated_at'])
        except ValueError:
            self.fail("created_at or updated_at is not in ISO format")

if __name__ == "__main__":
    unittest.main()
