import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime

try:
    load_dotenv()
except:
    print("Could not load the environement vairbales.")


API_key = os.getenv('API_KEY1')
API_secret = os.getenv('API_SECRET1')

API_key1 = os.getenv('API_KEY2')

API_secret1 = os.getenv('API_SECRET2')



#test.api.amadeus.com


def get_amadeus_token(client_id, client_secret):
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        return f"Error: {response.status_code}, {response.text}"

access_token = get_amadeus_token(API_key,API_secret)

def getAirportList(city):
    headers = {
    'Authorization': f'Bearer {access_token}'
    }
    req = requests.get(f"https://test.api.amadeus.com/v1/reference-data/locations?subType=CITY,AIRPORT&keyword={city}&countryCode=US", headers=headers)
    data = req.json().get("data")
    Iata =[]
    AirportList =[]
    for i in data:
        if i['subType'] == "AIRPORT":
            Iata.append(i['iataCode'])
            AirportList.append(f"{i['name']} AIRPORT")
       
    return Iata,AirportList

def getAirportName(code):
    try:
        url = f"https://test.api.amadeus.com/v1/reference-data/airlines?airlineCodes={code}" #currently using test api for this call because it saves the points in the acc

        headers = {
            'Authorization': f'Bearer {access_token}'
            }
        response = requests.get(url, headers=headers)
  
        data = response.json().get('data')

        return data[0]['businessName']
    except:
        print("Invalid Airline code.")
        return "ERROR"
    
def get_token():
    url = "https://api.amadeus.com/v1/security/oauth2/token"

    payload = f'client_id={API_key1}&client_secret={API_secret1}&grant_type=client_credentials'
    headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()['access_token']

def extract_flight_data(data):
        extracted = []

        for offer in data.get("data", []):
            itinerary = offer["itineraries"][0]
            segments = itinerary["segments"]

            route = [seg["departure"]["iataCode"] for seg in segments]
            route.append(segments[-1]["arrival"]["iataCode"])

            dep_time = datetime.fromisoformat(segments[0]["departure"]["at"]).strftime("%Y-%m-%d %H:%M")
            arr_time = datetime.fromisoformat(segments[-1]["arrival"]["at"]).strftime("%Y-%m-%d %H:%M")

            duration = itinerary["duration"].replace("PT", "").lower()
            airline_codes = list({seg["carrierCode"] for seg in segments})

            price = offer["price"]["grandTotal"]
            currency = offer["price"]["currency"]

            extracted.append({
                "airlines": airline_codes,
                "route": " → ".join(route),
                "departure": dep_time,
                "arrival": arr_time,
                "duration": duration,
                "price": f"{price} {currency}"
            })

        return extracted


def get_price(Depcode,DesCode,Depdate,RetDate,adult,children,infants):

    url = "https://api.amadeus.com/v2/shopping/flight-offers"
    headers = {
        "Authorization": f"Bearer {get_token()}"
    }
    params = {
        "originLocationCode": f"{Depcode}",
        "destinationLocationCode": f"{DesCode}",
        "departureDate": f"{Depdate}",
        "adults": adult,
        'children': children,
        'infants': infants,
        "travelClass": "ECONOMY",
        "currencyCode": "USD",
        "max": 7
    }

    if RetDate:
        params['returnDate'] = f'{RetDate}'
        

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    return data



def BeauitfyData(flight_data):
    response = (
        "✈️ **Flight Details**\n"
        f"🛫 **`Route`:** {flight_data['route']}\n"
        f"📅 **`Departure`:** {flight_data['departure']}\n"
        f"🛬 **`Arrival`:** {flight_data['arrival']}\n"
        f"⏱️ **`Duration`:** {flight_data['duration']}\n"
        f"🛩️ **`Airline`:** {getAirportName(flight_data['airlines'][0])}\n"
        f"💰 **`Price`:** {flight_data['price']}"
    )
    return response
# print(getAirportList("Cleveland")) (['CLE', 'BKL', 'CGF'], ['HOPKINS INT AIRPORT', 'BURKE LAKEFRONT AIRPORT', 'CUYAHOGA COUNTY AIRPORT'])


# print(getAirportList("Cleveland"))

# a = getAirportList("hello")

# print(a[0].__len__())

flights = extract_flight_data(get_price("CLE","PIT","2025-04-18","",1,0,0))
for flight in flights[:10]:
    print(flight)
# print(get_price("CLE","PIT","2025-04-17","",1,0,0))


