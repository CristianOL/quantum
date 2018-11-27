# -*- coding: utf-8 -*-
import pymongo
import pprint
import sys
import constants

class FillDB:

    db = None
    client = None

    def getBBDD(self, bbdd):
        self.client = pymongo.MongoClient(constants.domain, 27017)
        self.db = self.client[bbdd]

    def fillProjects(self):
        try:
            projects = self.db['projects']

            list_projects = [{"_id": "0", "name": "Gefion", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit velit varius maximus condimentum. Pellentesque luctus interdum convallis. Sed et molestie sapien.", 
                            "category": "Banca", "technologies": ["Vue", "Flask"], "photo": "https://i.imgur.com/oOhlIfT.png", "person_id": [1,4,5], "manager_id": [1,4], "workplace": "Las Tablas", "duration": 6},
                            {"_id": "1", "name": "Trombone", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit velit varius maximus condimentum. Pellentesque luctus interdum convallis. Sed et molestie sapien.",
                            "category": "Tecnologia", "technologies": ["Java"], "photo": "https://i.imgur.com/pqOygXA.png", "person_id": [1,9,7,3], "manager_id": [1,9], "workplace": "Av. Burgos", "duration": 12},
                            {"_id": "2", "name": "Quantum Technologies", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit velit varius maximus condimentum. Pellentesque luctus interdum convallis. Sed et molestie sapien.",                            
                            "category": "Salud", "technologies": ["Flask", "React"], "photo": "https://i.imgur.com/a0aeT3V.png", "person_id": [3,8,4], "manager_id": [3,4], "workplace": "La Vaguada", "duration": 69},
                            {"_id": "3", "name": "Sundance", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit velit varius maximus condimentum. Pellentesque luctus interdum convallis. Sed et molestie sapien.",
                            "category": "Salud", "technologies": ["Cobol", "Fortran"], "photo": "https://i.imgur.com/lIE8S8z.png", "person_id": [2,4,6,54], "manager_id": [6,4], "workplace": "La Vaguada", "duration": 2},
                            {"_id": "4", "name": "Mako Project", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit velit varius maximus condimentum. Pellentesque luctus interdum convallis. Sed et molestie sapien.",
                            "category": "Banca", "technologies": ["Python", "Java"], "photo": "https://i.imgur.com/aiwBzOl.png", "person_id": [12,4,88], "manager_id": [12,4], "workplace": "Av. Burgos", "duration": 8},
                            {"_id": "5", "name": "Thierry", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit velit varius maximus condimentum. Pellentesque luctus interdum convallis. Sed et molestie sapien.",
                            "category": "Salud", "technologies": ["Vue", "Django"], "photo": "https://i.imgur.com/IeB52TP.png", "person_id": [23,455,56,24,343], "manager_id": [23,24], "workplace": "Av. Burgos", "duration": 23},
                            {"_id": "6", "name": "Aquarium Technologies", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit velit varius maximus condimentum. Pellentesque luctus interdum convallis. Sed et molestie sapien.",
                            "category": "Energia", "technologies": ["React"], "photo": "https://i.imgur.com/f2vP1Te.png", "person_id": [1], "manager_id": [1], "workplace": "Las Tablas", "duration": 34},
                            {"_id": "7", "name": "Amino", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit velit varius maximus condimentum. Pellentesque luctus interdum convallis. Sed et molestie sapien.",
                            "category": "Gestion", "technologies": ["Vue", "Flask"], "photo": "https://i.imgur.com/OXZfEFj.png", "person_id": [134,432], "manager_id": [134], "workplace": "Av. Burgos", "duration": 5}]


            # Insertamos la informacion en la BD:
            self.db.projects.insert_many(list_projects)
            print ("\n")
            print (self.db.collection_names(include_system_collections = False))
            for project in projects.find():
                print("\n")
                pprint.pprint(project)
            print ("\n")
            print (projects.count())
        except:
            print("Hay dos projectos con el mismo user_id")

    def fillPersons(self):
        try:
            persons = self.db['persons']
            list_persons = [{"_id": "0", "name": "Fran Ramirez", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit velit varius maximus condimentum. Pellentesque luctus interdum convallis. Sed et molestie sapien.",
                            "roles": ["Backend"], "technologies": ["Vue", "Flask"], "photo": "https://i.imgur.com/PLDPSHK.png", 
                            "phone": 739040303, "email": "fran@beeva.com"},
                            {"_id": "1", "name": "Emilio Perez", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit velit varius maximus condimentum. Pellentesque luctus interdum convallis. Sed et molestie sapien.",
                            "roles": ["Frontend", "DevOps"], "technologies": ["Java", "Vue"], "photo": "https://i.imgur.com/eKzy9XM.png", 
                            "phone": 987589403, "email": "emilio@beeva.com"},
                            {"_id": "2", "name": "Javier Vazquez", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit velit varius maximus condimentum. Pellentesque luctus interdum convallis. Sed et molestie sapien.",
                            "roles": ["Scrum Master"], "technologies": ["Python"], "photo": "https://i.imgur.com/QKSrUFV.png", 
                            "phone": 637489302, "email": "javier@beeva.com"},
                            {"_id": "3", "name": "Jesus Hernandez", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit velit varius maximus condimentum. Pellentesque luctus interdum convallis. Sed et molestie sapien.",
                            "roles": ["Backend", "DevOps"], "technologies": ["Vue", "Node"], "photo": "https://i.imgur.com/HwOkyi2.png", 
                            "phone": 354672839, "email": "jesus@beeva.com"},
                            {"_id": "4", "name": "Jesus Ortega", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit velit varius maximus condimentum. Pellentesque luctus interdum convallis. Sed et molestie sapien.",
                            "roles": ["ProductOwner", "DevOps"], "technologies": ["JavaScript", "Java"], "photo": "https://i.imgur.com/AI6zcUQ.png", 
                            "phone": 354627292, "email": "pedro@beeva.com"},
                            {"_id": "5", "name": "Emilio Pereña", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit velit varius maximus condimentum. Pellentesque luctus interdum convallis. Sed et molestie sapien.",
                            "roles": ["Backend", "ProductOwner"], "technologies": ["React", "Java"], "photo": "https://i.imgur.com/ORAEBKf.png", 
                            "phone": 453534534, "email": "aaron@beeva.com"},
                            {"_id": "6", "name": "Gabriel Tarancon", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit velit varius maximus condimentum. Pellentesque luctus interdum convallis. Sed et molestie sapien.",
                            "roles": ["Frontend"], "technologies": ["Vue", "Django"], "photo": "https://i.imgur.com/XBiCvgZ.png", 
                            "phone": 349823749, "email": "gabriel@beeva.com"},
                            {"_id": "7", "name": "Felipe Segovia", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit velit varius maximus condimentum. Pellentesque luctus interdum convallis. Sed et molestie sapien.",
                            "roles": ["DevOps", "Scrum Master"], "technologies": ["React", "Cobol"], "photo": "https://i.imgur.com/GhKmLE7.png", 
                            "phone": 234234234, "email": "felipe@beeva.com"}]


            self.db.persons.insert_many(list_persons)
            print ("\n")
            print (self.db.collection_names(include_system_collections = False))
            for person in persons.find():
                print("\n")
                pprint.pprint(person)
            print ("\n")
            print (persons.count())
        except:
            print("Hay dos personas con el mismo user_id")


    
if __name__ == '__main__':
    bbdd_name = 'quantumdb'
    object = FillDB()
    object.getBBDD(bbdd_name)
    object.fillProjects()
    object.fillPersons()



