from flask import Flask, render_template, jsonify, request
import requests
from flask_pymongo import PyMongo
import itertools
import re
import math
import constants
import json
import random


class Helpers:

  def isSublist(self, dataFromBBDD, inputData):
    trueCounter = 0;
    for element in inputData:
      for elementFromBBDD in dataFromBBDD:
        if element.lower() == elementFromBBDD.lower():
          trueCounter = trueCounter + 1
    if trueCounter == len(inputData):
      return True
    else:
      return False 
      
  def paginate(self, output, initialPoint, PAGINATION):    
    thereIsPrev = False
    thereIsNext = False

    if initialPoint != 0:          
      prevSlice = output[ : initialPoint - 1]
    else:
      prevSlice = []

    sliceOutput = output[initialPoint : initialPoint + PAGINATION]
    nextSlice = output[initialPoint + PAGINATION : ]

    if len(prevSlice) > 0:
      thereIsPrev = True
    if len(nextSlice) > 0:
      thereIsNext = True

    numberOfPages = int(math.ceil(len(output)/PAGINATION))

    return sliceOutput, thereIsPrev, thereIsNext, numberOfPages
    

helpers = Helpers()

class MongoDatabase:
 
  def getDatabaseMongoDB(self, databaseName, port):
        
    app = Flask(__name__)

    app.config['MONGO_DBNAME'] = databaseName
    app.config['MONGO_URI'] = 'mongodb://' + constants.domain + ':' + str(port) + '/' + databaseName 

    mongo = PyMongo(app)
    return app, mongo

  #GET
  def getAll(self, ddbb, collection):
    
    if collection == constants.projects_route:
      
      output = []
      for document in ddbb.db.projects.find():
          output.append({'_id' : document['_id'], 'name' : document['name'], 'description' : document['description'],
                        'category': document['category'], 'technologies': document['technologies'],
                        'photo': document['photo'], 'person_id': document['person_id'], 'manager_id': document['manager_id'],
                        'workplace': document['workplace'], 'duration': document['duration']})
      print(request)
      page = request.json['page']
      initialPoint = constants.PROJECTS_PAGINATION * page

      json, thereIsPrev, thereIsNext, numberOfPages = helpers.paginate(output, initialPoint, constants.PROJECTS_PAGINATION)

      return jsonify({'result' : json, 'hasPrevPage': thereIsPrev, 'hasNextPage': thereIsNext, 'numberOfPages': numberOfPages})
    
    elif collection == constants.persons_route:
          
      output = []
      for document in ddbb.db.persons.find():
          output.append({'_id' : document['_id'], 'name' : document['name'], 'description' : document['description'],
                         'roles' : document['roles'], 'technologies' : document['technologies'], 
                         'photo' : document['photo'], 'phone' : document['phone'], 'email' : document['email']})

      page = request.json['page']
      initialPoint = constants.PERSONS_PAGINATION * page

      json, thereIsPrev, thereIsNext, numberOfPages = helpers.paginate(output, initialPoint, constants.PERSONS_PAGINATION)

      return jsonify({'result' : json, 'hasPrevPage': thereIsPrev, 'hasNextPage': thereIsNext, 'numberOfPages': numberOfPages})
    

  def getTechnologiesList(self, ddbb, collection):
    output = []
    if collection == constants.projects_route:
      for document in ddbb.db.projects.find(): 
        output.append(document['technologies'])
      output = list(set(itertools.chain(*output)))
      output.sort()
      output2 = []
      for element in output:
        output2.append({'name': element})
      return jsonify({'result' : output2})
    elif collection == constants.persons_route:
      for document in ddbb.db.persons.find(): 
        output.append(document['technologies'])
      output = list(set(itertools.chain(*output)))
      output.sort()
      output2 = []
      for element in output:
        output2.append({'name': element})
      return jsonify({'result' : output2})


  def getCategoriesList(self, ddbb):
    output = []
    for document in ddbb.db.projects.find(): 
      output.append(document['category'])
    output = list(set(output))
    output.sort()
    output2 = []
    for element in output:
      output2.append({'name': element})
    return jsonify({'result' : output2})


  def getWorkplacesList(self, ddbb):
    output = []
    for document in ddbb.db.projects.find(): 
      output.append(document['workplace'])
    output = list(set(output))
    output.sort()
    output2 = []
    for element in output:
      output2.append({'name': element})
    return jsonify({'result' : output2})

    
  def getRolesList(self, ddbb):
    output = []
    for document in ddbb.db.persons.find(): 
      output.append(document['roles'])
    output = list(set(itertools.chain(*output)))
    output.sort()
    output2 = []
    for element in output:
      output2.append({'name': element})
    return jsonify({'result' : output2})

  def getNamesList(self, ddbb, collection):
    output = []
    if collection == constants.projects_route:
      for document in ddbb.db.projects.find():
        output.append({'_id' : document['_id'], 'name' : document['name'], 'workplace': document['workplace']})
      return jsonify({'result' : output})
    if collection == constants.persons_route:
      for document in ddbb.db.persons.find():
        output.append({'_id' : document['_id'], 'name' : document['name'],  
                      'photo' : document['photo'], 'email' : document['email']})
      return jsonify({'result' : output})


  #POST
  def postSomething(self, ddbb, collection):
        
    if collection == constants.projects_route:
      
      id = request.json['_id']
      name = request.json['name']
      description = request.json['description']
      category = request.json['category']
      technologies = request.json['technologies']
      photo = request.json['photo']
      personId = request.json['person_id']
      managerId = request.json['manager_id']
      workplace = request.json['workplace']
      duration = request.json['duration']

      ddbb.db.projects.insert({'_id' : id, 'name' : name, 'description' : description,
                                    'category': category, 'technologies': technologies,
                                    'photo': photo, 'person_id': personId,
                                    'manager_id': managerId,
                                    'workplace': workplace, 'duration': duration})

      output = []
      for document in ddbb.db.projects.find():
          output.append({'_id' : document['_id'], 'name' : document['name'], 'description' : document['description'],
                        'category': document['category'], 'technologies': document['technologies'],
                        'photo': document['photo'], 'person_id': document['person_id'], 'manager_id': document['manager_id'],
                        'workplace': document['workplace'], 'duration': document['duration']})
                        
      return jsonify({'result' : output})

    elif collection == constants.persons_route:
          
      id = request.json['_id']
      name = request.json['name']
      description = request.json['description']
      roles = request.json['roles']
      technologies = request.json['technologies']
      photo = request.json['photo']
      phone = request.json['phone']  
      email = request.json['email']
      
      ddbb.db.persons.insert({'_id' : id, 'name' : name, 'description' : description, 
                                    'roles' : roles, 'technologies' : technologies, 'photo' : photo,
                                    'phone' : phone, 'email' : email})

      output = []
      for document in ddbb.db.persons.find():
          output.append({'_id' : document['_id'], 'name' : document['name'], 'description' : document['description'],
                         'roles' : document['roles'], 'technologies' : document['technologies'], 
                         'photo' : document['photo'], 'phone' : document['phone'], 'email' : document['email']})

      return jsonify({'result' : output})


  def searchByTechnologies(self, ddbb, collection):
    output = []
    if collection == constants.projects_route:
      technologies = request.json['request']            
      page = request.json['page']

      for document in ddbb.db.projects.find({ '$query': { 'technologies':  re.compile(r'\b(?:%s)\b' % '|'.join(technologies), re.IGNORECASE) }, '$orderby': { 'name': 1 }} ):
        output.append({'_id' : document['_id'], 'name' : document['name'], 'description' : document['description'],
                    'category': document['category'], 'technologies': document['technologies'],
                    'photo': document['photo'], 'person_id': document['person_id'], 'manager_id': document['manager_id'],
                    'workplace': document['workplace'], 'duration': document['duration']})
      output2 = []
      for element in output:
        if helpers.isSublist(element.get('technologies'), technologies):
          output2.append(element)
      
      initialPoint = constants.PROJECTS_PAGINATION * page
      json, thereIsPrev, thereIsNext, numberOfPages = helpers.paginate(output2, initialPoint, constants.PROJECTS_PAGINATION)
      return jsonify({'result' : json, 'hasPrevPage': thereIsPrev, 'hasNextPage': thereIsNext, 'numberOfPages': numberOfPages})
    
    elif collection == constants.persons_route:
      technologies = request.json['request']       
      page = request.json['page']

      for tech in technologies:
        for document in ddbb.db.persons.find({ '$query': { 'technologies':  re.compile(r'\b(?:%s)\b' % '|'.join(technologies), re.IGNORECASE) }, '$orderby': { 'name': 1 }} ):
          output.append({'_id' : document['_id'], 'name' : document['name'], 'description' : document['description'],
                        'roles' : document['roles'], 'technologies' : document['technologies'], 
                        'photo' : document['photo'], 'phone' : document['phone'], 'email' : document['email']})
      output2 = []
      for element in output:
        if helpers.isSublist(element.get('technologies'), technologies):
          output2.append(element)

      initialPoint = constants.PERSONS_PAGINATION * page
      json, thereIsPrev, thereIsNext, numberOfPages = helpers.paginate(output2, initialPoint, constants.PERSONS_PAGINATION)
      return jsonify({'result' : json, 'hasPrevPage': thereIsPrev, 'hasNextPage': thereIsNext, 'numberOfPages': numberOfPages})
    
  
  def searchByCategories(self, ddbb):
      output = []
      categories = request.json['request']
      page = request.json['page']

      for document in ddbb.db.projects.find({ '$query': { 'category':  re.compile(r'\b(%s)\b' % categories, re.IGNORECASE) }, '$orderby': { 'name': 1 }} ):
        output.append({'_id' : document['_id'], 'name' : document['name'], 'description' : document['description'],
                    'category': document['category'], 'technologies': document['technologies'],
                    'photo': document['photo'], 'person_id': document['person_id'], 'manager_id': document['manager_id'],
                    'workplace': document['workplace'], 'duration': document['duration']})

      initialPoint = constants.PROJECTS_PAGINATION * page
      json, thereIsPrev, thereIsNext, numberOfPages = helpers.paginate(output, initialPoint, constants.PROJECTS_PAGINATION)
      return jsonify({'result' : json, 'hasPrevPage': thereIsPrev, 'hasNextPage': thereIsNext, 'numberOfPages': numberOfPages})
    

  def searchByWorkplaces(self, ddbb):
      output = []
      workplaces = request.json['request']
      page = request.json['page']

      for document in ddbb.db.projects.find({ '$query': { 'workplace':  re.compile(r'\b(%s)\b' % workplaces, re.IGNORECASE) }, '$orderby': { 'name': 1 }} ):
        output.append({'_id' : document['_id'], 'name' : document['name'], 'description' : document['description'],
                    'category': document['category'], 'technologies': document['technologies'],
                    'photo': document['photo'], 'person_id': document['person_id'], 'manager_id': document['manager_id'],
                    'workplace': document['workplace'], 'duration': document['duration']})

      initialPoint = constants.PROJECTS_PAGINATION * page
      json, thereIsPrev, thereIsNext, numberOfPages = helpers.paginate(output, initialPoint, constants.PROJECTS_PAGINATION)
      return jsonify({'result' : json, 'hasPrevPage': thereIsPrev, 'hasNextPage': thereIsNext, 'numberOfPages': numberOfPages})
 

  def searchByRoles(self, ddbb):
      output = []
      roles = request.json['request']
      page = request.json['page']

      for document in ddbb.db.persons.find({ '$query': { 'roles':  re.compile(r'\b(?:%s)\b' % '|'.join(roles), re.IGNORECASE) }, '$orderby': { 'name': 1 }} ):
        output.append({'_id' : document['_id'], 'name' : document['name'], 'description' : document['description'],
                        'roles' : document['roles'], 'technologies' : document['technologies'], 
                        'photo' : document['photo'], 'phone' : document['phone'], 'email' : document['email']})
      output2 = []
      for element in output:
        if helpers.isSublist(element.get('roles'), roles):
          output2.append(element)

      initialPoint = constants.PERSONS_PAGINATION * page
      json, thereIsPrev, thereIsNext, numberOfPages = helpers.paginate(output2, initialPoint, constants.PERSONS_PAGINATION)
      return jsonify({'result' : json, 'hasPrevPage': thereIsPrev, 'hasNextPage': thereIsNext, 'numberOfPages': numberOfPages})
 

  def searchByName(self, ddbb, collection):
    output = []
    if collection == constants.projects_route:
      name = request.json['request']
      page = request.json['page']

      for document in ddbb.db.projects.find({ '$query': { 'name':  re.compile(r'(%s)' % name, re.IGNORECASE) }, '$orderby': { 'name': 1 }} ):
        output.append({'_id' : document['_id'], 'name' : document['name'], 'description' : document['description'],
                'category': document['category'], 'technologies': document['technologies'],
                'photo': document['photo'], 'person_id': document['person_id'], 'manager_id': document['manager_id'],
                'workplace': document['workplace'], 'duration': document['duration']})

      initialPoint = constants.PROJECTS_PAGINATION * page
      json, thereIsPrev, thereIsNext, numberOfPages = helpers.paginate(output, initialPoint, constants.PROJECTS_PAGINATION)
      return jsonify({'result' : json, 'hasPrevPage': thereIsPrev, 'hasNextPage': thereIsNext, 'numberOfPages': numberOfPages})
 
    elif collection == constants.persons_route:
      name = request.json['request']
      page = request.json['page']

      for document in ddbb.db.persons.find({ '$query': { 'name':  re.compile(r'(%s)' % name, re.IGNORECASE) }, '$orderby': { 'name': 1 }} ):
        output.append({'_id' : document['_id'], 'name' : document['name'], 'description' : document['description'],
                      'roles' : document['roles'], 'technologies' : document['technologies'], 
                      'photo' : document['photo'], 'phone' : document['phone'], 'email' : document['email']})

      initialPoint = constants.PERSONS_PAGINATION * page
      json, thereIsPrev, thereIsNext, numberOfPages = helpers.paginate(output, initialPoint, constants.PERSONS_PAGINATION)
      return jsonify({'result' : json, 'hasPrevPage': thereIsPrev, 'hasNextPage': thereIsNext, 'numberOfPages': numberOfPages})
 

  def searchById(self, ddbb, collection):
    output = []
    if collection == constants.projects_route:
      id = request.json['request']

      for document in ddbb.db.projects.find({ '$query': { '_id':  re.compile(r'\b(?:%s)\b' % '|'.join(id), re.IGNORECASE) }, '$orderby': { 'name': 1 }}):
        output.append({'_id' : document['_id'], 'name' : document['name'], 'description' : document['description'],
                'category': document['category'], 'technologies': document['technologies'],
                'photo': document['photo'], 'person_id': document['person_id'], 'manager_id': document['manager_id'],
                'workplace': document['workplace'], 'duration': document['duration']})

      return jsonify({'result' : output})
 
    elif collection == constants.persons_route:
      id = request.json['request']

      for document in ddbb.db.persons.find({ '$query': { '_id':  re.compile(r'\b(?:%s)\b' % '|'.join(id), re.IGNORECASE) }, '$orderby': { 'name': 1 }}):
        output.append({'_id' : document['_id'], 'name' : document['name'], 'description' : document['description'],
                      'roles' : document['roles'], 'technologies' : document['technologies'], 
                      'photo' : document['photo'], 'phone' : document['phone'], 'email' : document['email']})

      return jsonify({'result' : output})


# GET PARA ORGANIGRAMA:

  def getNamesOrganigram(self, ddbb):
    
    jsonNames = []
    outputTree = []

    childrens = 6
    numNamesInChildren = 5

    children = []
    
    for document in ddbb.db.persons.find():
      jsonNames.append({'name': document['name']})

    print (len(jsonNames))

    for i in range(childrens):
          
      if (i==0) | (i==1) | (i==3) | (i==5):
         
        jsonChildren = []

        for _ in range(numNamesInChildren):
              
            if len(jsonChildren) < numNamesInChildren:
                
              jsonChildren.append(jsonNames[random.randrange(0, len(jsonNames))])
     
        children.append({'name': jsonNames[random.randrange(0, len(jsonNames))]['name'],
                          'children': jsonChildren})
      
      elif (i==2) | (i==4):

        jsonChildren = []    
                      
        #jsonChildren.append(jsonNames[random.randrange(0, len(jsonNames))])

        children.append({'name': jsonNames[random.randrange(0, len(jsonNames))]['name'],
                          'children': jsonChildren})
                          
    outputTree.append({'name': jsonNames[random.randrange(0, len(jsonNames))]['name'],
                       'children': children})

    return jsonify({'result' : outputTree})
