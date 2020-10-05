import requests
from requests import *
import json
from datetime import *
from twilio.rest import Client
# Your Account Sid and Auth Token from twilio.com/console
# REPLACE WITH YOUR OWN KEYS
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)
def sendSMS(SMSbody):
    message = client.messages \
                .create(
                    body=SMSbody,
                    from_=' +19285890813',
                    to='+19054491786'
                )
    print(message.sid)




apiKey = ""

startDate=date.today()
endDate=date.today() + timedelta(days=7)

url = "https://www.neowsapp.com/rest/v1/feed?start_date={}&end_date={}&detailed=true&api_key={}".format(startDate, endDate, apiKey)
response = get(url)
response = response.json()
result = response["near_earth_objects"]
for date in result:
    for neo in result[date]:
        name = neo["name"]
        reference=neo["nasa_jpl_url"]
        size=(neo["estimated_diameter"]["meters"]["estimated_diameter_min"]+neo["estimated_diameter"]["meters"]["estimated_diameter_max"])/2
        isHazardous=neo["is_potentially_hazardous_asteroid"]
        date=neo["close_approach_data"][0]["close_approach_date_full"]
        missDistance=neo["close_approach_data"][0]["miss_distance"]["kilometers"]
        if isHazardous:
            #print(name, reference, size, isHazardous, date, missDistance)
            str="Asteroid {} has been declared Hazardous by NASA. It will pass by on {} missing the earth by approximately {} kilometers. It is approximately {} m. Please see the official NASA reference: {}".format(name, date, missDistance, size, reference)
            sendSMS(str)
