#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.
Unittest classes:
    TestFileStorage_instantiation
    TestFileStorage_methods
"""
import os
import models
import unittest
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

from models.engine.file_storage import FileStorage


class TestFileStorage_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""
    def test_FileStorage_instantiation_no_args(self):
        self.assertIsInstance(FileStorage(), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_private_str(self):
        self.assertIsInstance(FileStorage._FileStorage__file_path, str)

    def testFileStorage_objects_is_private_dict(self):
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)

    def test_storage_initializes(self):
        self.assertIsInstance(models.storage, FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""
    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        self.cls_bm = BaseModel()
        self.cls_u = User()
        self.cls_s = State()
        self.cls_c = City()
        self.cls_p = Place()
        self.cls_a = Amenity()
        self.cls_r = Review()
        models.storage.new(self.cls_bm)
        models.storage.new(self.cls_u)
        models.storage.new(self.cls_s)
        models.storage.new(self.cls_c)
        models.storage.new(self.cls_p)
        models.storage.new(self.cls_a)
        models.storage.new(self.cls_r)

        models.storage.save()

    @classmethod
    def tearDown(self):

        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertIsInstance(models.storage.all(), dict)

    def test_all_with_arg(self):
        self.assertRaises(TypeError, models.storage.all, None)

    def test_new(self):

        self.assertIn("BaseModel." + self.cls_bm.id,
                      models.storage.all().keys())
        self.assertIn("User." + self.cls_u.id, models.storage.all().keys())
        self.assertIn("State." + self.cls_s.id, models.storage.all().keys())
        self.assertIn("City." + self.cls_c.id, models.storage.all().keys())
        self.assertIn("Place." + self.cls_p.id, models.storage.all().keys())
        self.assertIn("Amenity." + self.cls_a.id, models.storage.all().keys())
        self.assertIn("Review." + self.cls_r.id, models.storage.all().keys())

    def test_new_with_None(self):
        self.assertRaises(AttributeError, models.storage.new, None)

    def test_save(self):
        save_text = ""
        with open("file.json", "r") as json_file:
            save_text = json_file.read()
            self.assertIn("BaseModel." + self.cls_bm.id, save_text)
            self.assertIn("User." + self.cls_u.id, save_text)
            self.assertIn("State." + self.cls_s.id, save_text)
            self.assertIn("City." + self.cls_c.id, save_text)
            self.assertIn("Place." + self.cls_p.id, save_text)
            self.assertIn("Amenity." + self.cls_a.id, save_text)
            self.assertIn("Review." + self.cls_r.id, save_text)

    def test_save_with_arg(self):
        self.assertRaises(TypeError, models.storage.save, None)

    def test_reload(self):

        FileStorage._FileStorage__objects = {}
        models.storage.reload()
        self.assertIn("BaseModel." + self.cls_bm.id,
                      FileStorage._FileStorage__objects.keys())

    def test_reload_with_arg(self):
        self.assertRaises(TypeError, models.storage.reload, None)


if __name__ == "__main__":
    unittest.main()
