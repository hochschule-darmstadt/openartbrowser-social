import json
import tweepy
import requests
from config import *
from constant import *
import os
from PIL import Image
from resizeimage import resizeimage
from constant import defaultSize

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# All posted artwork IDs are written to a file. In this method, we will find the first artwork from the provided list "artworkIDList" (top-down) which has not yet been posted and return it.
def checkPostedArtworks(artworkQIDs):
  posted = False
  postedList = [""]

  with open("posted.txt", "r") as file:
    for line in file:
      postedList.append(line)

  for x in artworkQIDs:
    for y in postedList:
      if y.__contains__(x):
        posted = True

    if posted == False:
      file.close()
      return x
    else:
      posted = False


# This method will add the QID of an artwork to our persistent file so we do not post it again.
def addPostedArtwork(artworkQID):
  with open("posted.txt", "a") as file:
    file.write("\n" + artworkQID)
    file.close()

  print("Added artwork QID " + artworkQID + " to persistent file.")


#response = requests.get(url, data=json.dumps(artwork_query), headers=headers)
#body = response.json()

#Hole alle QIDs in eine Liste
artworkQIDs = [
    "When Brigid twisted her ankle and fell forward face down on the gravel, only she could see the tiny man tugging his right leg and only she could hear him calling out in his raspy voice, Help me get my foot out of this hole!",


    ]





tweet_text = f" {postArtistName} is the Artist von {artwork_titel} . To see more infos see {url_post}"


print(tweet_text)
api.update_with_media(imgpath, tweet_text)



# IF TWITTER POST SUCCESSFULL
addPostedArtwork(postQID)



'''
def get_num_pixels(filepath):
    width, height = Image.open(filepath).size
    return width*height

print(get_num_pixels(imgpath))
'''




'''
import requests as rq
import json
from config import *
import tweepy

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
# Number of artworks to get
count = 1000

# Elasticsearch API URL
url = 'https://openartbrowser.org/api/de/_search'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


def elasticQueryArtwork():
  # Query will get "count" no. of artworks, sort them by their relative rank in descending order.
  artwork_query = {
    'size': count,
    'sort': {
      'relativeRank': 'desc'
    },
    'query': {
      "match": {
        "type": "artwork"
      }
    }
  }

  return artwork_query


def elasticQueryArtist(ID):
  # Prepare query to find more details about artist using their QID "postArtistQID"
  artist_query = {
    'size': '1',
    'query': {
      "match": {
        "id": ID
      }
    }
  }

  return artist_query


# All posted artwork IDs are written to a file. In this method, we will find the first artwork from the provided list "artworkIDList" (top-down) which has not yet been posted and return it.
def checkPostedArtworks(artworkQIDList):
  posted = False
  postedList = [""]

  with open("posted.txt", "r") as file:
    for line in file:
      postedList.append(line)

  for x in artworkQIDList:
    for y in postedList:
      if y.__contains__(x):
        posted = True

    if posted == False:
      file.close()
      return x
    else:
      posted = False


# This method will add the QID of an artwork to our persistent file so we do not post it again.
def addPostedArtwork(artworkQID):
  with open("posted.txt", "a") as file:
    file.write("\n" + artworkQID)
    file.close()

  print("Added artwork QID " + artworkQID + " to persistent file.")


# ARTWORK QUERY
# The response will save the data retrieved for the artwork
response = rq.get(url, data=json.dumps(elasticQueryArtwork()), headers=headers)

# We save the json data from the body of the response for the artwork
body = response.json()

# List of all artwork QIDs retrieved in query
artworkQIDList = []

# Append each QID of an artwork from the body to the "artworkQIDList". The QID of an artwork can be found at the position "x" in the body structure.
for x in range(count):
  artworkQIDList.append(body["hits"]["hits"][x]["_source"]["id"])

# DATA FOR TWITTER POST
# Get the QID of the artwork we are going to post into "postQID"
postQID = checkPostedArtworks(artworkQIDList)

# Get the position of it in the response body for getting the following data
postQIDPos = artworkQIDList.index(postQID)

# Name of art
postName = body["hits"]["hits"][postQIDPos]["_source"]["label"]

# Link to artwork image
postImage = body["hits"]["hits"][postQIDPos]["_source"]["image"]

# QID of artist
postArtistQID = body["hits"]["hits"][postQIDPos]["_source"]["artists"][0]

# ARTIST QUERY
# The response will save the data retrieved for the artist
response = rq.get(url, data=json.dumps(elasticQueryArtist(postArtistQID)), headers=headers)

# We save the json data from the body of the response for the artist
body = response.json()

# Name of artist
postArtistName = body["hits"]["hits"][0]["_source"]["label"]

# ALL DATA FOR TWITTERP POST
print(postQID)
print(postName)
print(postImage)
print(postArtistQID)
print(postArtistName)

# INSERT TWITTER POST CODE HERE
def image_download(link):
  response = rq.get(link)
  file = open("image.jpg", "wb")
  file.write(response.content)
  file.close()


image_download(postImage)
imgpath = "/home/ahmad/PycharmProjects/pythonProject/image.jpg"
url_post = f"https://openartbrowser.org/en/artwork/{postQID}"
tweet_text = f" {postArtistName} is the Artist von {postName} . To see more infos see {url_post}"
print(tweet_text)
#api.update_with_media(imgpath, tweet_text)

# IF TWITTER POST SUCCESSFULL
addPostedArtwork(postQID)
'''