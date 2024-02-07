from typing import Dict, Any, List

from serpapi import GoogleSearch

""" This module handles functions related to the serpapi library. These functions
allow the user to perform a search of google job listings using searchapi parameters,
creating a search query, and running the search. """


def secrets_handling() -> str:
    """ This function imports secrets but with error handling
    if the user hasn't created a secrets.py file."""
    try:
        # try to import secrets
        import secrets
        return secrets.api_key
    except ImportError:
        # if import error exception occurs print error message and return no secrets
        return 'No secrets'


def create_search_parameters(query: str, location: str, api_key: str, page_offset: int) -> dict:
    """ This function creates a python dictionary based on passed query and location
        that will be entered by the user. A serpapi key is passed as a parameter for the use
        of the API. A page offset is passed as a parameter to print other pages of the api output.
        This function is called in the serpapi_search function. """
    # python dictionary of the parameters
    search_parameters = {
        'engine': 'google_jobs',
        'q': query,
        'location': location,
        'hl': 'en',
        'google_domain': 'google.com',
        'api_key': api_key,
        'start': page_offset
    }
    return search_parameters


def serpapi_search(query: str, location: str, api_key: str, page_number: int, page_offset: int) -> List[Dict[str, Any]]:
    """ This function generates a search query based on parameters.
        This function calls the search_parameters function to get the parameters dictionary
        and then calls the serpapi google search with the parameters
        and returns the json_data results as a list of dictionary's/json."""
    if not location.strip():
        print(f'Generating Page {page_number} results for {query} positions in no specific location')
    else:
        print(f'Generating Page {page_number} results for {query} positions near {location}...\n')
    # function call to generate parameter dictionary
    search_parameters = create_search_parameters(query, location, api_key, page_offset)
    # serpapi call
    search = GoogleSearch(search_parameters)
    # get results as dictionary
    results = search.get_dict()
    # keep just actual job search_results key and return it
    return results.get('jobs_results')
