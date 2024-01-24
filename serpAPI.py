from serpapi import GoogleSearch

def serpapi_search(query, location, api_key):
    search_result = GoogleSearch({
        "q": query,
        "location": location,
        "api_key": api_key
    })