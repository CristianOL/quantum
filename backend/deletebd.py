# -*- coding: utf-8 -*-
import pymongo
import pprint
import sys
import constants

class DeleteDB:

    db = None
    client = None

    def getBBDD(self, bbdd):
        self.client = pymongo.MongoClient(constants.domain, 27017)
        self.db = self.client[bbdd]

    def deleteBBDD(self, bbdd):
        self.client.drop_database(bbdd)

        
if __name__ == '__main__':
    bbdd_name = 'quantumdb'
    object = DeleteDB()
    object.getBBDD(bbdd_name)
    object.deleteBBDD(bbdd_name)

