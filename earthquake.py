import json
import requests
from bs4 import BeautifulSoup
from numpy import sin, cos, arccos, pi, round
import requests
from bs4 import BeautifulSoup
import os
import json

current_path = os.getcwd()
with open(f"{current_path}/cities.json", "r") as f:
    cities = json.load(f)

class Earthquake:


    headers = {
        "Host": "www.koeri.boun.edu.tr",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    }
    res = requests.get(
        "http://www.koeri.boun.edu.tr/scripts/lst9.asp", headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")

    @staticmethod
    def earthquakes() -> list:

        fetch_earthquakes = Earthquake.soup.pre.text.splitlines()[7:]
        to_json = []

        for count,fetched in enumerate(fetch_earthquakes, start=1):
            earthquake = fetched.split()
            if earthquake:
                if "İlksel" in earthquake:
                        to_json.append({
                    "id": count,
                    "time": {
                        "date": earthquake[0],
                        "hour": earthquake[1]},
                    "coordinate": {"latitude": float(earthquake[2]),
                                "longitude": float(earthquake[3])},
                    "depth": float(earthquake[4]),
                    "intensity": {
                        "MD": earthquake[5],
                        "ML": earthquake[6],
                        "MW": earthquake[7]},
                    "location": " ".join(earthquake[8:-1]),
                    "control": earthquake[-1]
                })
                else:
                    to_json.append({
                    "id": count,
                    "time": {
                        "date": earthquake[0],
                        "hour": earthquake[1]},
                    "coordinate": {"latitude": float(earthquake[2]),
                                "longitude": float(earthquake[3])},
                    "depth": float(earthquake[4]),
                    "intensity": {
                        "MD": earthquake[5],
                        "ML": earthquake[6],
                        "MW": earthquake[7]},
                    "location": " ".join(earthquake[8:-3]),
                    "control": earthquake[-3:]
                })
        return to_json

    def city_response(self, city):
        new_resp = []
        for eq in Earthquake.earthquakes():
            if city.upper() in eq["location"]:
                new_resp.append(eq)
        if new_resp:
            return new_resp
        else:
            return {"succes":"succes","description":"Earthquake not found"}, 400
    
    def distance_response(self, city, distance_control):
        new_resp = []
        for eq in Earthquake.earthquakes():
            distance = getDistanceBetweenPointsNew(latitude1=eq["coordinate"]["latitude"],
                                                   longitude1=eq["coordinate"]["longitude"],
                                                   city=city.capitalize())
            if distance < distance_control:
                eq["distance"] = distance
                new_resp.append(eq)
        if new_resp:
            return new_resp
        else:
            return {"succes":"succes","description":"Earthquake not found"}, 400

    def filter_by_intensity(self, min:float, max:float, type="ML"):
        if min and max:
            return list(filter(lambda eq: min< float(eq["intensity"][type]) < max, Earthquake.earthquakes()))
        if min:
            return list(filter(lambda eq: min< float(eq["intensity"][type]), Earthquake.earthquakes()))
        if max:
            return list(filter(lambda eq: float(eq["intensity"][type]) < max, Earthquake.earthquakes()))
        else:
            return {"succes":"succes","description":"Earthquake not found"}
    
    def filter_by_control(self, control):
        if control.lower() == "ilksel":
            return list(filter(lambda eq: eq["control"] == "İlksel", Earthquake.earthquakes()))
        elif control.lover() == "revize":
            return list(filter(lambda eq: eq["control"] == "REVIZE01", Earthquake.earthquakes()))
        
    
        

    def order_by_depth(self, ls, order="ascending"):

        if order.lower() == "ascending":
            return sorted(ls, key=lambda i: i["depth"])
        elif order.lower() == "descanding":
            return sorted(ls, key=lambda i: i["depth"], reverse=True)
        else:
            return {"succes": "fail", "description": "An error was encountered while accessing depth information."}

    def order_by_intensity(self, ls, order="ascending", type="ML"):
        if order.lower() == "ascending":
            return sorted(ls, key=lambda i: i["intensity"][type])
        elif order.lower() == "descanding":
            return sorted(ls, key=lambda i: i["intensity"][type], reverse=True)
        else:
            return {"succes": "fail", "description": "An error was encountered while accessing intensity information."}

    def order_by_distance(self, city, distance_control, order="ascending"):
        if order.lower() == "ascending":
            return sorted(Earthquake.distance_response(city, distance_control), key=lambda d: d['distance'])
        elif order.lower() == "descanding":
            return sorted(Earthquake.distance_response(city, distance_control), key=lambda d: d['distance'], reverse=True)
        else:
            return {"succes": "fail", "description": "An error was encountered while accessing distance information."}


""" Distance & Distance Utils """


def rad2deg(radians):
    degrees = radians * 180 / pi
    return degrees


def deg2rad(degrees):
    radians = degrees * pi / 180
    return radians


def getDistanceBetweenPointsNew(latitude1, longitude1, city, unit='kilometers'):

    try:
        latitude2 = float(cities[city]["lat"])  # from cities.json
        longitude2 = float(cities[city]["lng"])  # from cities.json
    except KeyError:
        return False
    theta = longitude1 - longitude2

    distance = 60 * 1.1515 * rad2deg(
        arccos(
            (sin(deg2rad(latitude1)) * sin(deg2rad(latitude2))) +
            (cos(deg2rad(latitude1)) * cos(deg2rad(latitude2)) * cos(deg2rad(theta)))
        )
    )

    if unit == 'miles':
        return round(distance, 2)
    if unit == 'kilometers':
        return round(distance * 1.609344, 2)


if __name__ == "__main__":
    eq = Earthquake()
    print(eq.filter_by_intensity(4, 5))
