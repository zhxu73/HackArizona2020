#!/usr/bin/env python3


import requests
from graphqlclient import GraphQLClient
import json

def read_token_from_file(filename):
    with open(filename, "r") as infile:
        content = infile.read()
        json_obj = json.loads(content)
        token = json_obj["bearerToken"]
        return token

def gql_request(token):
    session = requests.Session()
    headers = dict()
    headers["Authorization"] = "Bearer {}".format(token)
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"

    url = "https://dev.fly.me/api/graphql"

    cookies = dict()
    cookies["trustedClientToken"] = "Y621S/Usq1KuWhFQPbFD1uZd5AkyILcte8Rmxe8yaC2Ef5WH9xDovDjR38pFRKH9yhswc6YlhYnWOZXBNk18m1M4/57fhX0ZzUOzClg+UKlKVftXUI4XhABFrpSYnZZNzOaD7b+LYrUtGXvMJrY9BQ=="
    session.cookies["trustedClientToken"] = cookies["trustedClientToken"]

    data = dict()
    data["query"] = "{profile {accountDetails {id, accountEmail, displayName}companyMembership {companyId, companyName, memberId, companyAdmin}}}"
    data["operationName"] = None
    data["variables"] = dict()

    resp = session.post(url, headers=headers, json=data)
    resp.raise_for_status()

    try:
        json_obj = json.loads(resp.text)
        return json_obj
    except json.decoder.JSONDecodeError:
        print("Failed to parse response body as json")
        raise

def main():
    token = read_token_from_file("fly_me_token.json")
    try:
        result = gql_request(token)
        print(result)
    except Exception as e:
        print(e)

main()
