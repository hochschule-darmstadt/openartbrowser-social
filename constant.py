# ElasticSearch Search URL
url = "https://openartbrowser.org/api/en/_search"

# Headers for request
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

# Number of max elements to retrieve from ElasticSearch
count = 100

# Library PIL has a limit for processing images up to this size (in Bytes)
image_processing_limit = 200000000

# Tweets can contain images up to this size (in Bytes)
tweet_max_size = 3072000

# Local file_path on staging server
file_path = "home/vpradhan"

# Artwork query needed for getting artworks to post on Twitter
artwork_query = {
  "sort": [
    {
      "relativeRank": {
        "order": "desc"
      }
    }
  ],
  "size": count,
  "query": {
    "match": {
      "type": "artwork"
    }
  }
}
