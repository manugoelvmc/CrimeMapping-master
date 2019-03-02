import sys
import requests
from math import *

from crimeReporting.models import *


# Reference: https://stackoverflow.com/questions/20231258/minimum-distance-between-a-point-and-a-line-in-latitude-longitude
def calculate_distance_from_line(latA, lonA, latB, lonB, latC, lonC):
    y = sin(lonC - lonA) * cos(latC)
    x = cos(latA) * sin(latC) - sin(latA) * cos(latC) * cos(latC - latA)
    bearing1 = degrees(atan2(y, x))
    bearing1 = 360 - ((bearing1 + 360) % 360)

    y2 = sin(lonB - lonA) * cos(latB)
    x2 = cos(latA) * sin(latB) - sin(latA) * cos(latB) * cos(latB - latA)
    bearing2 = degrees(atan2(y2, x2))
    bearing2 = 360 - ((bearing2 + 360) % 360)

    latARads = radians(latA)
    latCRads = radians(latC)
    dLon = radians(lonC - lonA)

    distanceAC = acos(sin(latARads) * sin(latCRads)+cos(latARads)*cos(latCRads)*cos(dLon)) * 6371
    min_distance = fabs(asin(sin(distanceAC/6371)*sin(radians(bearing1)-radians(bearing2))) * 6371)
    return min_distance


def calculate_score_for_route(steps):
    crimetype_score = {"theft": 0.5, "kidnap": 1.5, "rape": 2.5, "murder": 3}
    fir_reports = FIR_REPORT.objects.all()
    total_score = 0
    for report in fir_reports:
        min_dist = sys.float_info.max
        for step in steps:
            dist = calculate_distance_from_line(step["start_location"]["lat"], step["start_location"]["lng"],
                            step["end_location"]["lat"], step["end_location"]["lng"],
                            report.LAT, report.LNG)
            if min_dist > dist:
                min_dist = dist
        report_safesty_score = min_dist * min_dist / crimetype_score[report.CRIME_TYPE]
        total_score += report_safesty_score
    return total_score



import pandas as pd
import numpy as np
import urllib.request, json
from sklearn.neighbors import RadiusNeighborsRegressor
import sys

def get_route(origin, destination):
    murder = 5
    rape = 4
    eve_tease = 2
    theft = 3
    kidnapping = 4
    accidents = 3
    camera = 1

    dataset = pd.read_csv(r"file3.csv")
    dataset['rate'] = murder * dataset['Murder'] + rape * dataset['Rape'] + eve_tease * dataset['Eve tease'] + theft * dataset['Theft'] + kidnapping * dataset['Kidnapping'] + accidents * dataset['Accidents'] - dataset['Camera']

    # Google MapsDdirections API endpoint
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    api_key = 'AIzaSyD08BN7gmi_FNMNszEWYoe6y4hzHs570VY'

    # origin1 = input('Where are you?: ')
    # destination1 = input('Where do you want to go?: ')
    origin = origin.replace(' ','+')
    destination = destination.replace(' ','+')

    # Building the URL for the request
    nav_request = 'origin={}&destination={}&key={}&alternatives={}'.format(origin,destination,api_key,'true')
    request = endpoint + nav_request

    # Sends the request and reads the response.
    response = urllib.request.urlopen(request).read()
    
    # Loads response as JSON
    directions = json.loads(response)

    nroutes = len(directions['routes'])

    routes = []
    dataroutes = []
    
    for i in range(nroutes):
        nsteps = len(directions['routes'][i]['legs'][0]['steps'])
        waypoints = []
        waydata = []

        for j in range(nsteps):   
            point = []
            datapoint = []
            point.append(directions['routes'][i]['legs'][0]['steps'][j]['start_location']['lat'])
            point.append(directions['routes'][i]['legs'][0]['steps'][j]['start_location']['lng'])
            datapoint.append([directions['routes'][i]['legs'][0]['steps'][j]['start_location']['lat'],directions['routes'][i]['legs'][0]['steps'][j]['start_location']['lng']])
            waypoints.append(point)
            waydata.append(datapoint)
        routes.append(waypoints)
        dataroutes.append(waydata)
        
     
    X = dataset[['Latitude','Longitude']]
    Y = dataset['rate']

    clf = RadiusNeighborsRegressor(radius=0.05, weights='distance', p=2)
    clf.fit(X,Y)

    
    bestyet = sys.maxsize
    choice = 0

    for i in range(nroutes):
        sum = 0
        for j in range(len(routes[i])):
            sum = sum+clf.predict(dataroutes[i][j])
        newrate = sum/len(routes[i])
        if newrate <= bestyet:
            bestyet = newrate
    choice = i

    return directions['routes'][choice]

# def get_route(origin, destination):
#     payload = {'origin': origin, 'destination': destination, 'key':'AIzaSyD62lqHOOFvXUfXW9Itrd-f30pSzi_Db3Q', 'alternatives': 'true'}
#     request = requests.get('https://maps.googleapis.com/maps/api/directions/json', params=payload)
#     route_response = request.json()
#     routes = route_response['routes']
#     for route in routes:
#         steps_in_route = route["legs"][0]["steps"]
#         score = calculate_score_for_route(steps_in_route)
#         route["score"] = score
#     return route_response
