'''
Created on 25 janv. 2017

@author: TO75329
'''
import json
from pymongo import MongoClient


def JSON2Mongo(file_in = "C:\\Users\\to75329\\Desktop\\DataScience\\P3-OSM\\data\\TournefeuilleLarge\\cured.osm.json", mongo_url = "mongodb://localhost:27017"):    
    
    client = MongoClient(mongo_url)
    db = client.P3
    db.OSM.drop()
    

    with open(file_in) as f:
        data = json.loads(f.read())
        if data:
            print("json cured file read successfully")
        #pprint.pprint(data)
        for record in data:
            #pprint.pprint(record)
            db.OSM.save(record)    
    print db.OSM.find_one()

if __name__ == '__main__':
    JSON2Mongo()