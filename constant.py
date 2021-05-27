url = "https://openartbrowser.org/api/en/_search"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
count = 100
image_processing_limit = 200000000
tweet_max_size = 3072000
filepath = "home/vpradhan"

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
