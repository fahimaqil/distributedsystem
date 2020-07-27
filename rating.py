import json
from random import randint

class database(object):
    dictData={}
    def checkId(self,string,jsonMovie):
        idMovie=0
        found=False
        for  i in jsonMovie:
            if i["name"].lower()==string.lower():
                idMovie=i["movieId"]
                found=True
        if found:
            return idMovie
        if not found:
            return 0
        
    def calculateRating(self,idValue,jsonRating):
        rating=0
        counter=0
        for i in jsonRating:
            if i["movieId"]==idValue:
                rating+=i["rating"]
                counter+=1
        return rating/counter
   
    with open('movie.json','r') as fp:
        mov = json.load(fp)
    new=mov[0:30]
    for i in new:
        dictData[i["title"]]=randint(1,5)
#lastName = obj["Hall"]
#age = obj["age"]
