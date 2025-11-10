#! /usr/bin/env python3

# a command-line program to search and edit tags of entries
# in a jellyfin database.
# just a mangling of the roulette code to different endpoints,
# and into a more modern language
#
# tags must match exactly
# currently failing on multiple tags
# multiple tags is an AND (not an OR)

import os
import sys
import argparse
import requests

# control

verbose = True
server = 'http://192.168.10.11:8096'

# get command line arguments
### TODO

# get api key
api_key = os.getenv("JELLYFIN")
if not api_key:
    print("Required environment variable JELLYFIN not found.")
    sys.exit(1)

# set the requests headers
headers = {
    "Accept": "application/json",
    "X-Emby-Token": api_key
}

# get tags (if not supplied in command line)            ### TODO
print("Please enter the tags (comma-seperated):")
tags = list(input().split(","))
tags_str = (",").join(tags)
### DEBUG
#print(tags)
#print(tags_str)


endpoint = f"/Items?tags={tags_str}&Recursive=true&Fields=Tags,Name,Type"

### FIXME 
# url encode the endpoint

### TODO
# add to the end point'&IncludeItemTypes={library}' if library specified in command line args

#print(endpoint)

# poll the server

url = f"{server}{endpoint}"

try:
    response = requests.get(url, headers=headers)
except requests.RequestException as e:
    print(f"Request failed: {e}")
    sys.exit(1)

if response.status_code == 200:
    data = response.json()
elif response.status_code == 401:
    print("Authorisation issue!")
    sys.exit(1)
else:
    print("Bad response from server.")
    sys.exit(1)

# process the data

if data and "Items" in data:
    items = data["Items"]
    for item in items:
        for key in ["Name", "Type", "Tags"]:
            if key in item:
                if key == "Tags":
                    tags = item[key]
                    print("TAG:")
                    for tag in tags:
                        print(f"'{tag}'", end="")
                    print()
                else:
                    print(f"{key}: {item[key]}")
        print("===================")






### TODO
# a main function