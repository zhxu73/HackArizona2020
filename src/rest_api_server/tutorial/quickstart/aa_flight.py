import json
import requests
import random

def aa_flight_engine_url():
    url = "localhost:3030/flights"
    return url

def list_aa_flights():
    url = aa_flight_engine_url()
    resp = requests.get(url)

    try:
        resp.raise_for_status()
        json_obj = json.loads(resp.text)
        return json_obj
    except requests.exceptions.HTTPError:
        print(resp.text)
        return None
    except json.decoder.JSONDecodeError as e:
        print("Failed to parse response as json")
        return None

def search_aa_flight(date, airport):
    """
    date needs to be in "%Y-%m-%d" format
    date & airport refers to depature
    """
    url = aa_flight_engine_url() + "?date={}&origin={}".format(date, airport)
    resp = requests.get(url)

    try:
        resp.raise_for_status()
        json_obj = json.loads(resp.text)
        return json_obj
    except requests.exceptions.HTTPError:
        print(resp.text)
        return None
    except json.decoder.JSONDecodeError as e:
        print("Failed to parse response as json")
        return None

def random_pick(date, airport):
    results = search_aa_flight(date, airport)
    if not results:
        return None
    index = random.randrange(0, len(results) - 1)
    return results[index]

def print_json(json_obj):
    json_formatted_str = json.dumps(json_obj, indent=2)
    print(json_formatted_str)

