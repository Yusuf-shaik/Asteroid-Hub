import pandas as pd
from pandas import DataFrame
import requests
from requests import *
import json
from datetime import *
import numpy as np
from astropy import units as u
import matplotlib.pyplot as plt
from poliastro.bodies import Earth, Mars, Sun
from poliastro.twobody import Orbit
from flask import Flask, render_template, request



startDate=date.today()
endDate=date.today() + timedelta(days=1)

apiKey="Zdwdmu3XeuOMOrMUHI2bm7auZcWW5fN1V0pCFZBr"


url="https://www.neowsapp.com/rest/v1/feed?start_date=2020-09-12&end_date=2020-09-12&detailed=true&api_key={}".format(apiKey)


response=get(url)
response=response.json()

result=response["near_earth_objects"]



asteroids=dict()
for date in result:
    for neo in result[date]:
        name = neo["name"]
        fileName = "static/image/"+name+".png"
        a = float(neo["orbital_data"]["semi_major_axis"]) * u.AU
        ecc = float(neo["orbital_data"]["eccentricity"]) * u.one
        inc = float(neo["orbital_data"]["inclination"]) * u.deg
        raan = float(neo["orbital_data"]["ascending_node_longitude"]) * u.deg
        argp = float(neo["orbital_data"]["perihelion_argument"]) * u.deg
        nu = float(neo["orbital_data"]["mean_anomaly"]) * u.deg
        print(a, ecc, inc, raan, argp, nu)


        orb = Orbit.from_classical(Earth, a, ecc, inc, raan, argp, nu)
        orb.plot()
        figure=plt.gcf()
        plt.axis('off')

        


        plt.savefig(fileName, dpi=100)
        print(fileName)
        
        




