import sys
import requests
from math import *

from crimeReporting.models import *

import pandas as pd
import numpy as np
import math
import urllib.request, json
import gmaps
import pandas as pd

data = pd.read_csv('final_data.csv')

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

# def getRouteSafety(waypoints,dist, size, data, plot_crime_points):
#     rating = 0.0
    
#     for i in range(len(waypoints)):
#         rating+=getPointSafety(waypoints[i], size, data, plot_crime_points)      
    
#     return rating/len(waypoints)


# def distance(lat1,lng1,lat2,lng2):
#     b = abs(lat1-lat2)
#     c = abs(lng1-lng2)
#     a = b**2 + c**2
    
#     return math.sqrt(a)


# def isnearby_police(lat,lng):
#     endpoint = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
#     api_key = 'AIzaSyD08BN7gmi_FNMNszEWYoe6y4hzHs570VY'

#     location = str(lat)+','+str(lng)
#     radius=800
#     typ="police"  


#     nav_request = 'location={}&radius={}&type={}&key={}'.format(location,radius,typ,api_key)
#     request = endpoint + nav_request

#     response = urllib.request.urlopen(request).read()
#     police = json.loads(response)
    
#     if len(police['results'])==0:
#         return False
    
#     return True


# def findStartIndex(lng,size, data):
#     low = 0
#     high =size-1
#     mid=0
#     val = lng
#     #print("new root")
#     while low<=high:
#         mid=int((low+high)/2)
        
#         if data[data.columns[1]][mid]<val:
       
#             low=mid+1
#         else:
#             high=high-1

#     return mid


# def getPointSafety(point, size, data, plot_crime_points):
#     radius=0.05
#     rating = 0.0
#     lat = point[0]
#     lng = point[1]    
    
#     iloc = findStartIndex(lng-radius, size, data)
#     #print(iloc)
    
#     crime_points = []
    
#     while iloc<=size-1 and data[data.columns[1]][iloc]< lng+radius:
#         lat2 = data[data.columns[0]][iloc]
#         lng2 = data[data.columns[1]][iloc]
#         points=[]
#         points.append(lat2)
#         points.append(lng2)
#         plot_crime_points.append(point)
        
#         if(abs(lat2-lat)<radius):
#             d = distance(lat,lng,lat2,lng2) 
#             crime = data[data.columns[9]][iloc]
#             rating += crime/d
#         iloc=iloc+1
    
#     nearby_police = isnearby_police(lat,lng)
    
#     if nearby_police:
#         rating = (rating*8)/10
    
#     return rating





# # gmaps.configure(api_key='AIzaSyD08BN7gmi_FNMNszEWYoe6y4hzHs570VY')
# # coordinates = (28.664402, 77.124928)
# # gmaps.figure(center=coordinates, zoom_level=20)

# # fig = gmaps.figure()


# # #size = data[data.columns[0]].size
# # fig.add_layer(gmaps.traffic_layer())
# # fig.add_layer(gmaps.transit_layer())


# # layer1 = gmaps.directions.Directions(origin2, destination2,mode='car',waypoints=routes[0],stroke_color='Red')

# # fig.add_layer(layer1)
# # layer2 = gmaps.directions.Directions(origin2, destination2,mode='car',waypoints=routes[choice],stroke_color='blue')

# # fig.add_layer(layer2)

# # marker_layer = gmaps.symbol_layer(plot_crime_points,fill_color='green')
# # fig.add_layer(marker_layer)
# # fig


# def get_route(origin, destination):
#     global data
#     size = data[data.columns[0]].size
#     plot_crime_points=[]
#     endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
#     api_key = 'AIzaSyD08BN7gmi_FNMNszEWYoe6y4hzHs570VY'


#     origin=origin.replace(' ','+')
#     destination=destination.replace(' ','+')

#     nav_request = 'origin={}&destination={}&key={}&alternatives={}'.format(origin,destination,api_key,'true')
#     request = endpoint + nav_request

#     response = urllib.request.urlopen(request).read()
#     directions = json.loads(response)

#     origin2 = origin.strip().split(",")
#     origin2=[float(x.strip().strip("+")) for x in origin2]
#     destination2 = destination.strip().split(",")
#     destination2=[float(x.strip().strip("+")) for x in destination2]


#     nroutes = len(directions['routes'])

#     routes=[]
#     bestrate=sys.maxsize+1
#     choice=0
#     for i in range(nroutes):
        
#         nsteps = len(directions['routes'][i]['legs'][0]['steps'])
#         waypoints=[]

#         for j in range(nsteps):
#             point=[]
#             point.append(directions['routes'][i]['legs'][0]['steps'][j]['start_location']['lat'])
#             point.append(directions['routes'][i]['legs'][0]['steps'][j]['start_location']['lng'])
#             waypoints.append(point)
#         Rdistance = directions['routes'][i]['legs'][0]['distance']['value']
#         rating = getRouteSafety(waypoints,Rdistance, size, data, plot_crime_points)
#         if(rating<bestrate):
#             bestrate=rating
#             choice=i
#     return routes[choice];


import urllib.request, json
import sys
import pandas as pd
import numpy as np
import datetime
import math

def getRouteSafety(waypoints, Rdistance, size, plot_crime_points, live_events):
    global data
    rating = 0.0
    
    for i in range(len(waypoints)):
        rating += getPointSafety(waypoints[i], size, plot_crime_points, live_events)       
    
    return rating/len(waypoints)


def distance(lat1,lng1,lat2,lng2):
    b = abs(lat1-lat2)
    c = abs(lng1-lng2)
    a = b**2 + c**2
    
    return math.sqrt(a)


def isnearby_police(lat,lng):
    endpoint = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    api_key = 'AIzaSyD08BN7gmi_FNMNszEWYoe6y4hzHs570VY'

    location = str(lat)+','+str(lng)
    radius=800
    typ="police"  


    nav_request = 'location={}&radius={}&type={}&key={}'.format(location,radius,typ,api_key)
    request = endpoint + nav_request

    response = urllib.request.urlopen(request).read()
    police = json.loads(response)
    
    if len(police['results'])==0:
        return False
    
    return True
    

def getPointSafety(point, size, plot_crime_points, live_events):
    global data
    radius=0.05
    rating = 0.0
    lat = point[0]
    lng = point[1]    
    
    iloc = findStartIndex(lng-radius,data,size,plot_crime_points,live_events)
    
    #print(iloc)
    
    crime_points = []
    
    while iloc<=size-1 and data[data.columns[1]][iloc]< lng+radius:
        lat2 = data[data.columns[0]][iloc]
        lng2 = data[data.columns[1]][iloc]
        
        points=[]
        points.append(lat2)
        points.append(lng2)
        plot_crime_points.append(point)
        now = datetime.datetime.now()
        
        if(abs(lat2-lat)<radius):
            d = distance(lat,lng,lat2,lng2) 
            #t=(now.year-y)*365+(now.month-m)*30+(now.day-day)
            t=1
            crime = data[data.columns[9]][iloc]            
            
            rating += crime/d
            rating += crime/(d*t)
        iloc=iloc+1
    
    nearby_police = isnearby_police(lat,lng)
    
    if nearby_police:
        rating = (rating*8)/10
    
    return rating

def getLivePoint(point,data,size,plot_crime_points,live_events):
    radius=0.023
    rating = 0.0
    lat = point[0]
    lng = point[1]    
    
    iloc = findLiveIndex(lng-radius,data,size,plot_crime_points,live_events)  
    
    while iloc<=size-1 and live_events[iloc]< lng+radius:
        lat2 = live_events[iloc]
        lng2 = live_events[iloc]
        points=[]
        points.append(lat2)
        points.append(lng2)
        
        
        if(abs(lat2-lat)<radius):
            return sys.maxsize+1
        iloc=iloc+1

    return 0

def findStartIndex(lng,data,size,plot_crime_points,live_events):
    low = 0
    high =size-1
    mid=0
    val = lng
    while low<=high:
        mid=int((low+high)/2)
        
        if data[data.columns[1]][mid]<val:
            low=mid+1
        else:
            high=mid-1

    return mid

def findLiveIndex(lng,data,size,plot_crime_points,live_events):
    low = 0
    high =size-1
    mid=0
    val = lng    
    while low<=high:
        mid=int((low+high)/2)
        
        if live_events[mid]<val:
            low=mid+1
        else:
            high=mid-1

    return mid

    

def get_route(origin, destination):
    global data
    size = data[data.columns[0]].size
    plot_crime_points=[]
    live_events=[]

    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    api_key = 'AIzaSyD08BN7gmi_FNMNszEWYoe6y4hzHs570VY'

    origin = origin.replace(' ','+')
    destination = destination.replace(' ','+')

    nav_request = 'origin={}&destination={}&key={}&alternatives={}'.format(origin,destination,api_key,'true')
    request = endpoint + nav_request
    response = urllib.request.urlopen(request).read()
    directions = json.loads(response)


    nroutes = len(directions['routes'])

    routes=[]
    bestrate=sys.maxsize+1
    choice=0
    for i in range(nroutes):    
        nsteps = len(directions['routes'][i]['legs'][0]['steps'])
        waypoints = []
        
        for j in range(nsteps):
            point = []
            point.append(directions['routes'][i]['legs'][0]['steps'][j]['start_location']['lat'])
            point.append(directions['routes'][i]['legs'][0]['steps'][j]['start_location']['lng'])
            waypoints.append(point)

        Rdistance = directions['routes'][i]['legs'][0]['distance']['value']
        rating = getRouteSafety(waypoints, Rdistance, size, plot_crime_points, live_events)
        print(rating, bestrate)

        if(rating<bestrate):
            bestrate=rating
            choice=i
        routes.append(waypoints)
    return directions['routes'][choice]
