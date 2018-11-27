
from flask import Flask, render_template, jsonify, request
import requests
from flask_pymongo import PyMongo
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

import constants
from MongoDatabase import MongoDatabase

database = MongoDatabase()

def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):
    
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        
        def wrapped_function(*args, **kwargs):
            
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

class Controller:
    
    def endPoints(self, app, mongo):

        #PROJECTS ENDPOINTS
        
        @app.route(constants.projects_route + constants.technologies_route, methods = ['GET'])
        @crossdomain(origin = '*')
        def runGetProjectsTechnologiesList():
            return database.getTechnologiesList(mongo, constants.projects_route)

        @app.route(constants.projects_route + constants.categories_route, methods = ['GET'])
        @crossdomain(origin = '*')
        def runGetProjectsCategoriesList():
            return database.getCategoriesList(mongo)

        @app.route(constants.projects_route + constants.workplaces_route, methods = ['GET'])
        @crossdomain(origin = '*')
        def runGetProjectsWorkplacesList():
            return database.getWorkplacesList(mongo)
        
        @app.route(constants.projects_route + constants.name_route, methods = ['GET'])
        @crossdomain(origin = '*')
        def runGetProjectsNamesList():
            return database.getNamesList(mongo, constants.projects_route)

        @app.route(constants.projects_route + constants.add_route, methods = ['POST'])
        @crossdomain(origin = '*')
        def runPostProjects():
            return database.postSomething(mongo, constants.projects_route)

        @app.route(constants.projects_route + constants.technologies_route, methods = ['POST'])
        @crossdomain(origin = '*')
        def runPostProjectsByTechnologies():
            return database.searchByTechnologies(mongo, constants.projects_route)

        @app.route(constants.projects_route + constants.categories_route, methods = ['POST'])
        @crossdomain(origin = '*')
        def runPostProjectsByCategories():
            return database.searchByCategories(mongo)

        @app.route(constants.projects_route + constants.workplaces_route, methods = ['POST'])
        @crossdomain(origin = '*')
        def runPostProjectsByWorkplaces():
            return database.searchByWorkplaces(mongo)

        @app.route(constants.projects_route + constants.name_route, methods = ['POST'])
        @crossdomain(origin = '*')
        def runPostProjectsByName():
            return database.searchByName(mongo, constants.projects_route)

        @app.route(constants.projects_route, methods = ['POST'])
        @crossdomain(origin = '*')
        def runGetProjects():
            return database.getAll(mongo, constants.projects_route)

        @app.route(constants.projects_route + constants.id_route, methods = ['POST'])
        @crossdomain(origin = '*')
        def runPostProjectsById():
            return database.searchById(mongo, constants.projects_route)

       


        #PERSONS ENDPOINTS
        
        @app.route(constants.persons_route + constants.technologies_route, methods = ['GET'])
        @crossdomain(origin = '*')
        def runGetPersonsTechnologiesList():
            return database.getTechnologiesList(mongo, constants.persons_route)

        @app.route(constants.persons_route + constants.roles_route, methods = ['GET'])
        @crossdomain(origin = '*')
        def runGetPersonsRolesList():
            return database.getRolesList(mongo)

        @app.route(constants.persons_route + constants.name_route, methods = ['GET'])
        @crossdomain(origin = '*')
        def runGetPersonsNamesList():
            return database.getNamesList(mongo, constants.persons_route)
        
        @app.route(constants.persons_route + constants.add_route, methods = ['POST'])
        @crossdomain(origin = '*')
        def runPostPersons():
            return database.postSomething(mongo, constants.persons_route)

        @app.route(constants.persons_route + constants.technologies_route, methods = ['POST'])
        @crossdomain(origin = '*')
        def runPostPersonsByTechnologies():
            return database.searchByTechnologies(mongo, constants.persons_route)

        @app.route(constants.persons_route + constants.roles_route, methods = ['POST'])
        @crossdomain(origin = '*')
        def runPostPersonsByRoles():
            return database.searchByRoles(mongo)

        @app.route(constants.persons_route + constants.name_route, methods = ['POST'])
        @crossdomain(origin = '*')
        def runPostPersonsByName():
            return database.searchByName(mongo, constants.persons_route)

        @app.route(constants.persons_route + constants.id_route, methods = ['POST'])
        @crossdomain(origin = '*')
        def runPostPersonsById():
            return database.searchById(mongo, constants.persons_route)

        @app.route(constants.persons_route, methods = ['POST'])
        @crossdomain(origin = '*')
        def runGetPersons():
            return database.getAll(mongo, constants.persons_route)


# Endpoint para el organigrama:

        @app.route(constants.persons_route + constants.organigram_route, methods = ['GET'])
        @crossdomain(origin = '*')
        def runGetNamesOrganigram():
            return database.getNamesOrganigram(mongo)

            