import json
import time
import random

import tweepy
import requests
from config import *
from constant import *
from constant import defaultSize
import re
from resize_img import *
from PIL import Image



# Loading credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


class TwitterBot:
    def __init__(self, artworkQIDs):
        self.artworkQIDs = artworkQIDs

        # DATA FOR TWITTER POST
        # Get the QID of the artwork we are going to post into "postQID"
        postQID = self.checkPostedArtworks(self.artworkQIDs)

        postQIDPos = artworkQIDs.index(postQID)
        # print("artworkQIDs: ", artworkQIDs)
        print("postQID:", postQID)
        print("----------------------------------------------------------------------")

        # Name des Kustwerks
        artwork_title = body["hits"]["hits"][postQIDPos]["_source"]["label"]
        print("artwork_title: ", artwork_title)

        # TODO:alle artist soll extrahiert werden
        # QID von Kunstler
        artistQID = body["hits"]["hits"][postQIDPos]["_source"]["artists"][0]
        print("artistQID", artistQID)

        artist_query = {
            'size': '1',
            'query': {
                "match": {
                    "id": artistQID
                }
            }
        }

        response_artist = requests.get(url, data=json.dumps(artist_query), headers=headers)
        body_artist = response_artist.json()

        # Name of artist
        postArtistName = body_artist["hits"]["hits"][0]["_source"]["label"]
        print("artist_name:", postArtistName)

        # Link des image
        image_link = body["hits"]["hits"][postQIDPos]["_source"]["image"]
        print("Image_Link: ", image_link)

        filename = postQID + ".png"
        self.image_download(image_link, filename)

        imgSizeByte = os.path.getsize(filename)
        print("imgSizeByte is: ", imgSizeByte)

        if imgSizeByte > image_limit:
            self.addPostedArtwork(postQID)
            TwitterBot(self.artworkQIDs)

        else:
            if imgSizeByte > defaultSize:
                limit_img_size(
                    filename,  # input file
                    filename,  # target file
                    3000000,  # bytes
                    tolerance=5  # percent of what the file may be bigger than target_filesize
                )
                imgSizeBytenew = os.path.getsize(filename)
                print("new imagesize: ", imgSizeBytenew)

            url_post = f"https://openartbrowser.org/en/artwork/{postQID}"
            tweet_text = self.generateTweetText(postArtistName, artwork_title, url_post)

            print(tweet_text)
            api.update_with_media(filename, tweet_text)

            # IF TWITTER POST SUCCESSFULL
            self.addPostedArtwork(postQID)

    # All posted artwork IDs are written to a file. In this method, we will find the first artwork from the provided list "artworkIDList" (top-down) which has not yet been posted and return it.
    def checkPostedArtworks(self, artworkQIDs):
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

    def image_download(self, link, filename):
        imgResponse = requests.get(link)

        file = open(filename, "wb")
        file.write(imgResponse.content)
        file.close()

    def sanitize(self, text: str):
        """
        This function removes linebreaks, carriage returns, duplicated spaces and all leading
        and trailing spaces from the passed string and returns the sanitized one. This function should be used
        for fields which contain longer strings like 'label' or 'term'.
        """
        remove_chars = ["-", "—", "(", ")", ";", "&", "?", "/", ",", "\"", "."]
        replace_chars = [" "]
        for c in remove_chars:
            text = text.replace(c, "")

        # remove newline and carriage return
        sanitized_text = text.replace('\n', ' ').replace('\r', '')

        # remove duplicated spaces and remove leading and trailing spaces
        sanitized_text = re.sub(' +', ' ', sanitized_text)
        sanitized_text = sanitized_text.strip()

        return sanitized_text

    # This method will add the QID of an artwork to our persistent file so we do not post it again.
    def addPostedArtwork(self, artworkQID):
        with open("posted.txt", "a") as file:
            file.write("\n" + artworkQID)
            file.close()

        print("Added artwork QID " + artworkQID + " to persistent file.")

    def generateTweetText(self, artistName, artworkTitle, artworkURL):
        tweetTexts = [
            f" {artistName} is the artist of \"{self.sanitize(artworkTitle)}\". More infos can be found here: {artworkURL}",
            f" {artistName} created \"{self.sanitize(artworkTitle)}\". Curious? Further details at: {artworkURL}",
            f" \"{self.sanitize(artworkTitle)}\" is a masterpiece made by {artistName}. Find out more: {artworkURL}",
            f" Can you guess who made this? Created by {artistName} and titled \"{self.sanitize(artworkTitle)}\". Link: {artworkURL}",
            f" Who created \"{self.sanitize(artworkTitle)}\"? Find the answer at {artworkURL}",
            f" What is the name of this masterpiece made by {artistName}? The answer can bd found at {artworkURL}",
            f" \"{self.sanitize(artworkTitle)}\" by {artistName}. Link: {artworkURL}",
            f" {artistName} made \"{self.sanitize(artworkTitle)}\". Link: {artworkURL}",
            f" Like it? \"{self.sanitize(artworkTitle)}\". Find out more: {artworkURL}",
            f" Artwork of the week: \"{self.sanitize(artworkTitle)}\". More details here: {artworkURL}"
        ]

        return random.choice(tweetTexts)


# Main body of program

response = requests.get(url, data=json.dumps(artwork_query), headers=headers)
body = response.json()

# Hole alle QIDs in eine Liste
artworkQIDs = []
for x in range(count):
    # QID von Kunstwerk
    postQID = body["hits"]["hits"][x]["_source"]["id"]
    artworkQIDs.append(postQID)

TwitterBot(artworkQIDs)