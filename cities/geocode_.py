from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys   # Enter Shift bla bla
import time
import json
from dotenv import load_dotenv
import os

load_dotenv()

email = os.getenv("GEOMAIL")
password = os.getenv("GEOPASSWORD")


with open("cities.txt", "r") as f:
    all_cities = f.read().split("\n")

to_json = {}


class Geocode:
    def __init__(self):
        self.URL = "https://www.latlong.net/"
        self.city_list = all_cities

        driver_path = "./geckodriver"
        options = webdriver.FirefoxOptions()
        s = Service(executable_path=driver_path)
        self.driver = webdriver.Firefox(options=options, service=s)

    def open(self):
        self.driver.get(f"{self.URL}/user/login")
        time.sleep(2)
        self.driver.maximize_window()
        self.driver.find_element(By.ID, "email").send_keys(email,
                                                           Keys.TAB,
                                                           password,
                                                           Keys.TAB,
                                                           Keys.ENTER)
        time.sleep(1)
        self.driver.get(self.URL)
        time.sleep(2)

    def fetch(self):
        self.open()
        place_input = self.driver.find_element(By.ID, "place")
        find_button = self.driver.find_element(By.ID, "btnfind")
        lat_input = self.driver.find_element(By.ID, "lat")
        lng_input = self.driver.find_element(By.ID, "lng")
        for city in self.city_list:
            place_input.send_keys(city)
            find_button.click()
            time.sleep(1)
            lat = lat_input.get_property("value")
            lng = lng_input.get_property("value")
            to_json[city] = {"lat": lat,
                             "lng": lng}
        return to_json




if __name__ == "__main__":
    geo = Geocode()
    cities = geo.fetch() # dict

    with open("../cities.json", "w", encoding='utf8') as fp:
        json.dump(cities, fp, ensure_ascii=False)
