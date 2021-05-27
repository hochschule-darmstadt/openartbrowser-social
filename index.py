#!/usr/bin/ python3.8

# Loading data from local files
from twitterBot import *  # Get main class and use functionality for preparing post

# Get from ElasticSearch a certain no. of artworks - see constants file
response = requests.get(url, data=json.dumps(artwork_query), headers=headers)
body = response.json()

# Initialize artwork QIDs list
artworkQIDs = []
# Count is from constant file - no. artworks to retrieve from ElasticSearch.
# Load artwork QIDs into artworkQIDs array
for x in range(count):
    postQID = body["hits"]["hits"][x]["_source"]["id"]
    artworkQIDs.append(postQID)

# Run twitterBot with the list of artwork QIDs and response body which contains also other data
twitterBot(artworkQIDs, body)
