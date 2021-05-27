# Libraries required
import tweepy  # Tweets creation and posting
import json  # Using JSON data
import random  # Random selection
import requests  # HTTP Request
import re  # Regex
import os  # OS operations

# Loading data from local files
from config import *  # Config includes authentication data
from constant import *  # Load all constant parameters for application
from resize_img import *  # Importing function for resizing image


class twitterBot:
    def __init__(self, artworkQIDs, body):

        # INITIALIZE AUTH & DATA
        # Loading credentials for tweeting
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  # API Key and Secret
        auth.set_access_token(access_token, access_token_secret)  # Access Token and Secret
        api = tweepy.API(auth)

        # Loading artwork QIDs we are going to process to find an artwork to post and response body
        self.artworkQIDs = artworkQIDs
        self.body = body

        # PREPARE DATA FOR TWITTER POST
        # Get the QID of the artwork we are going to post into "postQID"
        postQID = self.checkPostedArtworks(self.artworkQIDs)

        # Get the position of the postQID in our list artworkQIDs
        postQIDPos = artworkQIDs.index(postQID)

        # Print the PostQID we are processing for log
        print("postQID:", postQID)
        print("----------------------------------------------------------------------")

        # ARTWORK NAME
        # Name of artwork can be loaded from response body using postQID position
        artwork_title = body["hits"]["hits"][postQIDPos]["_source"]["label"]
        # Print artwork name to log
        print("artwork_title: ", artwork_title)

        # ARTIST NAME
        # QID of artist can be loaded from response body using postQID position
        # For MVP only first artist is loaded
        artistQID = body["hits"]["hits"][postQIDPos]["_source"]["artists"][0]
        # Print artist QID to log
        print("artistQID", artistQID)

        # Prepare query for getting artist details using the artist QID we have found
        artist_query = {
            'size': '1',
            'query': {
                "match": {
                    "id": artistQID
                }
            }
        }

        # Get data from ElasticSearch with prepared artist_query
        response_artist = requests.get(url, data=json.dumps(artist_query), headers=headers)
        body_artist = response_artist.json()

        # Name of artist can be retrieved from body of response
        postArtistName = body_artist["hits"]["hits"][0]["_source"]["label"]
        # Print artist name to log
        print("artist_name:", postArtistName)

        # Prepare URL Link and Tweet text
        url_post = f"https://openartbrowser.org/en/artwork/{postQID}"
        tweet_text = self.generateTweetText(postArtistName, artwork_title, url_post)
        # Print tweet text to log
        print("tweet text: " + tweet_text)

        # IMAGE PREPARATION
        # Get link of image using postQID position
        image_link = body["hits"]["hits"][postQIDPos]["_source"]["image"]
        # Print image link to log
        print("Image_Link: ", image_link)

        # Prepare file name to download image and save it
        filename = postQID + ".png"
        # Download image with method image_download
        self.image_download(image_link, filename)

        # Get size of image file (bytes)
        imgSizeByte = os.path.getsize(filename)
        # Print image size to log
        print("imgSizeByte is: ", imgSizeByte)

        # Check if image size is greater than constant image limit
        # If yes,
        while imgSizeByte > image_limit:
            limit_img_size(
                filename,  # input file
                filename,  # target file
                3000000,  # bytes
                tolerance=5  # percent of what the file may be bigger than target_filesize
            )

            imgSizeByte = os.path.getsize(filename)
            print("new imagesize: ", imgSizeByte)

        #Send Twitter post with file and tweet text
        api.update_with_media(filename, tweet_text)
        #After twitter post, add QID to persistent file
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
