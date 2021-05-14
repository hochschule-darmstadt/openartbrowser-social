url = "https://openartbrowser.org/api/en/_search"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
count = 20
defaultSize = 3072000
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

