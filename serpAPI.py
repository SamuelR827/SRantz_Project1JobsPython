from serpapi import GoogleSearch
from secrets import secret_api_key


def create_search_parameters(query, location, api_key):
    search_parameters = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": api_key
    }
    return search_parameters


def serpapi_search(query, location, api_key):
    print("Searching for ")
    search_parameters = create_search_parameters(query, location, api_key)
    search = GoogleSearch(search_parameters)
    results = search.get_dict()
    return results


def perform_search():
    print("Performing search... \n")
    query = input("Please enter a job you would like to search for: ")
    location = input("Please enter your desired location for this job: ")
    search_results = serpapi_search(query, location, secret_api_key)
    return search_results
