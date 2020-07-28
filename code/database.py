import csv
import json
class database():
    reader = csv.DictReader(open('ratings.csv'))
    movie=csv.DictReader(open('movies.csv'))
    result = {}
    dictData={}
    for row in reader:
        done=False
        key = row.pop('movieId')
        if key in result:
            result[key]=(int(round(float(result[key])))+int(round(float(row['rating']))))/2
            done=True
        if done==False:
            result[key] = row['rating']
    for i in movie:
        if i["movieId"] in result:
            result[i["title"]] = result[i["movieId"]]
            del result[i["movieId"]]
    
    with open('my.csv','w') as f:
        w = csv.writer(f)
        w.writerow(["title", "rating"])
        w.writerows(result.items())
