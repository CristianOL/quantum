import MongoDatabase
import unittest
from mock import patch, MagicMock
from flask import Flask, render_template, jsonify, request
import requests
from flask_pymongo import PyMongo
import flask_pymongo

@patch.object(flask_pymongo.wrappers.Collection,'find', return_value={
      "result": 
      [{"_id": "0", "name": "Fran Ramirez", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit velit varius maximus condimentum. Pellentesque luctus interdum convallis. Sed et molestie sapien.",
                            "roles": ["Backend"], "technologies": ["Vue", "Flask"], "photo": "https://i.imgur.com/0KHJtni.jpg", 
                            "phone": 739040303, "email": "fran@beeva.com"}]
   })
def test_searchByRoles(self,mock_collection):
    result = MongoDatabase.searchByRoles()
    mock_collection.assert_called_once()
    assert result == [{"_id": "0", "name": "Fran Ramirez", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit velit varius maximus condimentum. Pellentesque luctus interdum convallis. Sed et molestie sapien.",
                        "roles": ["Backend"], "technologies": ["Vue", "Flask"], "photo": "https://i.imgur.com/0KHJtni.jpg", 
                        "phone": 739040303, "email": "fran@beeva.com"}]