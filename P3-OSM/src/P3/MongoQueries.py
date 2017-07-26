#!/usr/bin/env python
"""
Use an aggregation query to answer the following question. 

Extrapolating from an earlier exercise in this lesson, find the average
regional city population for all countries in the cities collection. What we
are asking here is that you first calculate the average city population for each
region in a country and then calculate the average of all the regional averages
for a country.
  As a hint, _id fields in group stages need not be single values. They can
also be compound keys (documents composed of multiple fields). You will use the
same aggregation operator in more than one stage in writing this aggregation
query. I encourage you to write it one stage at a time and test after writing
each stage.

Please modify only the 'make_pipeline' function so that it creates and returns
an aggregation  pipeline that can be passed to the MongoDB aggregate function.
As in our examples in this lesson, the aggregation pipeline should be a list of
one or more dictionary objects. Please review the lesson examples if you are
unsure of the syntax.

Your code will be run against a MongoDB instance that we have provided. If you
want to run this code locally on your machine, you have to install MongoDB,
download and insert the dataset. For instructions related to MongoDB setup and
datasets please see Course Materials.

Please note that the dataset you are using here is a different version of the
cities collection provided in the course materials. If you attempt some of the
same queries that we look at in the problem set, your results may be different.
"""
from pymongo import MongoClient
import pprint as pp
  
def get_db():
    client = MongoClient('localhost:27017')
    db = client['P3']
    return db

def make_pipelineNbRecordsByType():
    # complete the aggregation pipeline
    # complete the aggregation pipeline
    #pipeline = [{ "$group": {"_id": Null, "count": { "$sum": 1 } } }]
    pipeline = [
        {"$group": {"_id": "$type",
                    "count":{"$sum":1}}},
        {"$sort": {"count": -1}}
                  ]

    return pipeline


def make_pipelineWithAddress():
    # complete the aggregation pipeline    
    #pipeline = [{"address": {"$exists": True,"count":{"$sum":1}}}]
    pipeline = [
                {"$group":{
                 #"_id": {"$ifNull": ["$address",False]},
                 #"_id": {"$cond":[{"$eq":["$address","null"]},True,False]},
                 "_id":{"$gt":["$address",None]},
                 "count": {"$sum":1}
                 }}
                ]
    return pipeline

def make_pipelineWithHouseNumber():
    # complete the aggregation pipeline    
    #pipeline = [{"address": {"$exists": True,"count":{"$sum":1}}}]
    pipeline = [
                {"$group":{
                 #"_id": {"$ifNull": ["$address",False]},
                 #"_id": {"$cond":[{"$eq":["$address","null"]},True,False]},
                 "_id":{"$gt":["$address.housenumber",None]},
                 "count": {"$sum":1}
                 }}
                ]
    return pipeline

def make_pipelinePostcodes():
    # complete the aggregation pipeline    
    #pipeline = [{"address": {"$exists": True,"count":{"$sum":1}}}]
    pipeline = [
                { "$group" : { "_id" : "$address.postcode", "count" : { "$sum" : 1}}},  
                { "$sort" : { "count" : -1}}
                ]
    return pipeline

def aggregate(pipeline):
    db = get_db()
    return [doc for doc in db.OSM.aggregate(pipeline)]

def getNbRecordsByType():    
    return aggregate(make_pipelineNbRecordsByType())    

def getNbRecordsWithAddress():    
    return aggregate(make_pipelineWithAddress())

def getNbRecordsWithHouseNumber():    
    return aggregate(make_pipelineWithHouseNumber())

def getPostCodes():    
    return aggregate(make_pipelinePostcodes())

if __name__ == '__main__':
    pp.pprint(getNbRecordsWithAddress())
    pp.pprint(getNbRecordsWithHouseNumber())