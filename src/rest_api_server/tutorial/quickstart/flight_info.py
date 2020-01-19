import json
import datetime
import dateutil
import dateutil.parser
import tutorial.quickstart.fly_me
import tutorial.quickstart.aa_flight
from django.db import models
from tutorial.quickstart.models import UserData

def parse_input(json_obj):
    try:
        result = dict()
        result["responseId"] = json_obj["responseId"]
        result["session"] = json_obj["session"]
        result["queryResult"] = json_obj["queryResult"]
        result["intent"] = json_obj["queryResult"]["intent"]["displayName"]

        return result
    except IndexError:
        raise RuntimeError("Missing Field in request")

def dispatch_intent(intent, result):
    """
    intent is str
    """
    sessionId = result["session"]

    # Obtain departure date
    if intent == "Find Mystery Flight":
        date = extract_date(result["queryResult"])
        print("date: {}".format(date))
        user_data = UserData.objects.get_or_create(sessionId=sessionId, departure_date=date)
        return ask_user_location_permission(result)
    # Get user location
    elif intent == "Get User Location":
        cty = result["originalDetectIntentRequest"]["payload"]["device"]["location"]["city"]
        sessionId = result["session"]
        user_data = UserData.objects.filter(sessionId=sessionId)
        if not user_data:
            raise RuntimeError("No record of user data")
        date = user_data.departure_date
        if not date:
            raise RuntimeError("No departure date present")
        virtual_flight, price, currency = find_flights(date, city)
        user_data.price = price
        user_data.currency = currency

        dump_str = json.deumps(virtual_flight)
        if len(dump_str) < 1000:
            user_data.flight_json = dump_str
        user_data.save()
        return user_location_obtained()
    #
    elif intent == "Flight Confirmation":
        user_data = UserData.objects.get(sessionId=sessionId)
        if not user_data:
            raise RuntimeError("No record of user data")
        if not user_data.complete():
            # fixme, delete record
            raise RuntimeError("Corrupted user data")
        #
        # fixme
        # send email
        #

        # voice output for basic info
        return voice_response("Flight number is {}, price is {} {}".format(user_data.flight_number, user_data.price), user_data.currency)
    else:
        return unknown_intent_response()

def extract_date(queryResult):
    for context in queryResult["outputContexts"]:
        date_time_str = context["parameters"]["date"]
        departure_date = dateutil.parser.parse(date_time_str)
        # use the 1st date
        #return departure_date.strftime("%Y-%m-%d")
        return departure_date
    return None


def ask_user_location_permission(result):
    json_obj = dict()
    json_obj["payload"] = {
            "google": {
            "expectUserResponse": True,
            "systemIntent": {
                "intent": "actions.intent.PERMISSION",
                "data": {
                "@type": "type.googleapis.com/google.actions.v2.PermissionValueSpec",
                "optContext": "To address you by name and know your location",
                "permissions": [
                    "NAME",
                    "DEVICE_PRECISE_LOCATION"
                ]
                }
            }
            }
        }
    return json_obj

def user_location_obtained():
    return voice_response("Location obtained")

def default_response():
    return voice_response("This is a default response")

def unknown_intent_response():
    return voice_response("Sorry, unknown request, can not help you")

def error_response():
    return voice_response("Can not process the request")

def voice_response(msg, json_obj=None):
    if not json_obj:
        json_obj = dict()
    json_obj["payload"] = { "google": {
                        "expectUserResponse": False,
                        "richResponse": {
                            "items": [ { "simpleResponse": { "textToSpeech": msg } } ]
                        }
                    }
                }
    return json_obj

def find_flights(date, city):
    """
    depature date and depature city
    """
    json_obj = fly_me.gpl_request(fly_me.token, fly_me.find_airport_query(city))

    # if found airport
    if json_obj["data"]["airports"]["edges"]:
        airport = json_obj["data"]["airports"]["edges"][0]["node"]["iataCode"]
        print("airport: {}".format(airport))
    else:
        return None

    for i in range(3):
        virtual_flight = aa_flight.random_pick(date, airport)
        print("aa_flight: {}".format(virtual_flight))

        if virtual_flight:
            depature_date = dateutil.parser.parse(departureTime["departureTime"])
            arrival_date = dateutil.parser.parse(departureTime["arrivalTime"])
            fly_me_flight = fly_me.gpl_request(fly_me.token, fly_me.flight_search_query(virtual_flight["origin"]["code"], depature_date, virtual_flight["destination"]["code"], arrival_date))
            if fly_me_flight:
                break
    if not fly_me_flight["data"]["simpleAirSearch"]["select"]["products"]["edges"]:
        return None
    price = fly_me_flight["data"]["simpleAirSearch"]["select"]["products"]["edges"][0]["node"]["fareInfo"]["totalPrice"]
    currency = fly_me_flight["data"]["simpleAirSearch"]["select"]["products"]["edges"][0]["node"]["fareInfo"]["currency"]

    return virtual_flight, price, currency
