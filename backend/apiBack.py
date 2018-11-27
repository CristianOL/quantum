
from flask import Flask, render_template, jsonify, request
import requests
from flask_pymongo import PyMongo

from MongoDatabase import MongoDatabase
from Controller import Controller
import constants
from deletebd import DeleteDB 
from fillbd import FillDB


if __name__ == '__main__':
  
  databaseName = 'quantumdb'
  port = 27017

  deletedb = DeleteDB()
  filldb = FillDB()
  
  deletedb.getBBDD(databaseName)
  deletedb.deleteBBDD(databaseName)
  
  filldb.getBBDD(databaseName)
  filldb.fillProjects()
  filldb.fillPersons()


  database = MongoDatabase()
  app, mongo = database.getDatabaseMongoDB(databaseName, port)

  controller = Controller()
  controller.endPoints(app, mongo)

  app.run(host = '0.0.0.0')
