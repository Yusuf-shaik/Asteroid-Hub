import pandas as pd
from pandas import DataFrame
import requests
from requests import *
import json
from datetime import *
import numpy as np
from astropy import units as u
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from poliastro.bodies import Earth, Mars, Sun
from poliastro.twobody import Orbit, angles as angles
from poliastro.twobody.angles import M_to_E, E_to_nu

from flask import Flask, render_template, request
import os
import glob

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=['POST'])
def getImages():
    startDate = request.form['startDate']
    endDate = request.form['endDate']

    files=glob.glob('static\image\*')
    for f in files:
        os.remove(f)

    apiKey = ""
    url = "https://www.neowsapp.com/rest/v1/feed?start_date={}&end_date={}&detailed=true&api_key={}".format(startDate, endDate, apiKey)
    response = get(url)
    response = response.json()
    result = response["near_earth_objects"]
    for date in result:
        for neo in result[date]:
            name = neo["name"]
            fileName = "static/image/"+name+".png"
            resource=neo["nasa_jpl_url"]

            a = float(neo["orbital_data"]["semi_major_axis"]) * u.AU
            ecc = float(neo["orbital_data"]["eccentricity"]) * u.one
            inc = float(neo["orbital_data"]["inclination"]) * u.deg
            raan = float(neo["orbital_data"]
                            ["ascending_node_longitude"]) * u.deg
            argp = float(neo["orbital_data"]
                            ["perihelion_argument"]) * u.deg
            nu = float(neo["orbital_data"]["mean_anomaly"]) * u.deg

            # E=M_to_E(M, ecc) * u.deg
            # nu=E_to_nu(E,ecc) * u.deg
                       
            

            orb = Orbit.from_classical(Earth, a, ecc, inc, raan, argp, nu)
            orb.plot()
            figure = plt.gcf()
            plt.axis('off')

            plt.savefig(fileName, dpi=100)
            #print(fileName)

    images = []
    for picture in os.listdir('static/image'):
        images.append('static/image/'+ picture)

    return render_template("index.html", done=True, graphs=images, asteroidName=name, link=resource)


    # def eccentricAnomalyToTrueAnomaly(E, ecc):
    #     x=np.sqrt((1+ecc)/(1-ecc))
    #     nu=2 * np.arctan(x*np.tan(E/2))
    #     return nu

    # def meanAnomalyToEccentricAnomaly(M, ecc)