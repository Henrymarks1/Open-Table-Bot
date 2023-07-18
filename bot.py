import requests
import json
from dotenv import load_dotenv
import os


class OpenTable:
    def __init__(self, open_table_token, resturant_id, date, time, party_size, firstName, lastName, email):
        self.open_table_token = open_table_token
        self.resturant_id = resturant_id
        self.date = date
        self.time = time
        self.party_size = party_size
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.url_head = "https://www.opentable.com/dapi"
        self.headers = {
            'content-type': 'application/json',
            'origin': 'https://www.opentable.com',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'x-csrf-token': self.open_table_token,
        }

        times = self.find_resturant_times()
        print("Found times!")
        slot_availability_token, slot_hash = self.find_slot(times)
        print("Found slot!")
        self.booking_reservation(slot_availability_token, slot_hash)

    def find_resturant_times(self):
        url = self.url_head + "/fe/gql?optype=query&opname=RestaurantsAvailability"

        print("finding open reservations:")
        payload = json.dumps({
            "operationName": "RestaurantsAvailability",
            "variables": {
                "restaurantIds": [
                    self.resturant_id
                ],
                "date": self.date,
                "time": self.time,
                "partySize": self.party_size,
                "databaseRegion": "NA",
            },
            "extensions": {
                "persistedQuery": {
                    "sha256Hash": "e6b87021ed6e865a7778aa39d35d09864c1be29c683c707602dd3de43c854d86"
                }
            }
        })

        response = requests.post(url, headers=self.headers, data=payload)

        return response.json()

    def find_slot(self, times_object):
        # print(times_object)
        times_list = times_object["data"]["availability"][0]["availabilityDays"][0]["slots"]
        # print(days)
        available_slots = [slot for slot in times_list if slot['isAvailable']]
        closest_slot = min(available_slots, key=lambda x: abs(
            x['timeOffsetMinutes'])) if available_slots else None
        return closest_slot["slotAvailabilityToken"], closest_slot["slotHash"]

    def booking_reservation(self, slot_availability_token, slot_hash):
        url = self.url_head + "/booking/make-reservation"

        payload = json.dumps({
            "restaurantId": self.resturant_id,
            "slotAvailabilityToken": slot_availability_token,
            "slotHash":  slot_hash,
            "isModify": False,
            "reservationDateTime": self.date + "T" + self.time,
            "partySize": 2,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "country": "US",
            "reservationType": "Standard",
            "reservationAttribute": "default",
            "additionalServiceFees": [],
            "tipAmount": 0,
            "tipPercent": 0,
            "pointsType": "Standard",
            "points": 100,
            "diningAreaId": 1,
            "fbp": "fb.1.1685721920137.7677309689611231",
            "phoneNumber": "7185010213",
            "phoneNumberCountryId": "US",
            "optInEmailRestaurant": False
        })

        response = requests.request(
            "POST", url, headers=self.headers, data=payload)

        print(response.text)


load_dotenv()

date = "2023-07-25"
time = "18:00"
party_size = 2
open_table_token = os.environ.get('OPEN_TABLE_TOKEN')
bad_roman_id = 1268701
firstName = "Henry"
lastName = "Marks"
email = "henryesmarks@gmail.com"

OpenTable(open_table_token=open_table_token, resturant_id=bad_roman_id,
          date=date, time=time, party_size=party_size, firstName=firstName, lastName=lastName, email=email)
