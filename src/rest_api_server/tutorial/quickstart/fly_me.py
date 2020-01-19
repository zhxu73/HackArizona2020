#!/usr/bin/env python3


import requests
from graphqlclient import GraphQLClient
import json

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlcyI6W10sImlzcyI6Im1lLmZseSIsImRlZmF1bHRUcmF2ZWxlclBlcnNvbklkIjoiMTE2IiwidXNlcklkIjoiMzI4NDgzNmUtNTdkZC00ODVhLWFhOTMtOTU5MWE4Zjg4NTZhIiwicHVibGljX2V4cGlyZXNfZW0iOiIxNTc5NDE4NDgwNzE4IiwidXNlckNvbXBhbnlKc29uIjoie1wiY29tcGFueUlkXCI6MzksXCJtZW1iZXJJZFwiOjE3MixcImVuYWJsZWRNZW1iZXJcIjp0cnVlLFwiYWRtaW5pc3RyYXRvclwiOmZhbHNlLFwiZW5hYmxlZENvbXBhbnlcIjp0cnVlLFwiY29udHJhY3RTaWduZWRcIjp0cnVlfSIsImF1dGgwSWQiOiJnb29nbGUtb2F1dGgyfDEwMDE5NjI1NDI5NDUzMzE1MzE1OSIsInByb2ZpbGVJZCI6Ijk3Iiwic2NvcGUiOiJmbHltZWFwaWRldiIsImRiSWQiOiI5NyIsImV4cCI6MTU4MTkyNDA4MCwiaWF0IjoxNTc5MzMyMDgwLCJlbWFpbCI6InpoeHU3M0BlbWFpbC5hcml6b25hLmVkdSJ9.y1s_RqxmD5j5-AOmLg3PKUie3GOeU2ePY2SCI3JO0ds"

def read_token_from_file(filename):
    with open(filename, "r") as infile:
        content = infile.read()
        json_obj = json.loads(content)
        token = json_obj["bearerToken"]
        return token

def gql_request(token, query):
    session_id = requests.session_id()
    headers = dict()
    headers["Authorization"] = "Bearer {}".format(token)
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"

    url = "https://dev.fly.me/api/graphql"

    cookies = dict()
    cookies["trustedClientToken"] = "Y621S/Usq1KuWhFQPbFD1uZd5AkyILcte8Rmxe8yaC2Ef5WH9xDovDjR38pFRKH9yhswc6YlhYnWOZXBNk18m1M4/57fhX0ZzUOzClg+UKlKVftXUI4XhABFrpSYnZZNzOaD7b+LYrUtGXvMJrY9BQ=="
    session_id.cookies["trustedClientToken"] = cookies["trustedClientToken"]

    data = dict()
    #data["query"] = "{profile {accountDetails {id, accountEmail, displayName}companyMembership {companyId, companyName, memberId, companyAdmin}}}"
    data["query"] = query
    data["operationName"] = None
    data["variables"] = dict()

    resp = session_id.post(url, headers=headers, json=data)
    resp.raise_for_status()

    try:
        json_obj = json.loads(resp.text)
        return json_obj
    except json.decoder.JSONDecodeError:
        print("Failed to parse response body as json")
        raise

def find_airport_query(city):
    query = """
        query FindAirports($query: String = "{}") {
        airports(query: $query) {
            edges {
            node {
                ...SuggestionFacts
                subSuggestions {
                ...SuggestionFacts
                }
            }
            }
        }
        }

        fragment SuggestionFacts on AirportSuggestion {
        iataCode
        title
        subTitle
        selectedText
        location {
            ...LocationDetails
        }
        }

        fragment LocationDetails on Location {
        ltv { type, code }
        }
        """
    return query.format(city)

def flight_search_query(departure_airport, departure_date, arrival_airport, arrival_date):
    query = """
        {
        simpleAirSearch(input: {
            stops: [
            { portCode: "{}", earliestDate: "{}"} 
            { portCode: "{}", earliestDate: "{}"}
            ]
            returnsToOrigin: true
        }) {
            select {
            products(first: 3) {
                edges {
                node {
                    type
                    productId
                    fareInfo { validatingCarrier, totalPrice, currency }
                    ods {
                    id
                    segments {
                        departurePort, departureTime, marketingCarrier
                        flightNumber, arrivalPort, arrivalTime
                    }
                    }
                }
                }
            }
            }
        }
        }
        """
    return query.format(departure_airport, departure_date, arrival_airport, arrival_date)
