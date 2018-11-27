# -*- coding: utf-8 -*-
import pymongo
import pprint
import sys
import constants

class InitBBDD:

    db = None
    client = None

    def getBBDD(self, bbdd):
        self.client = pymongo.MongoClient(constants.domain, 27017)
        self.db = self.client[bbdd]


if __name__ == '__main__':
    bbdd_name = 'quantumdb'
    object = InitBBDD()
    object.getBBDD(bbdd_name)
   
