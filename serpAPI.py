from serpapi import GoogleSearch


""" This module handles functions related to the serpapi library. These functions
allow the user to perform a search of google job listings using searchapi parameters,
creating a search query, and running the search. """

from util_functions import write_file_header
from util_functions import write_page_to_file
from util_functions import get_user_input


def secrets_handling():
    """ This function imports secrets but with error handling
    if the user hasn't created a secrets.py file."""
    try:
        # try to import secrets
        import secrets
        return secrets.secret_api_key
    except ImportError:
        # if import error exception occurs print error message and return no secrets
        return "No secrets"


def create_search_parameters(query, location, api_key, page_offset):
    """ This function creates a python dictionary based on passed query and location
        that will be entered by the user. A serpapi key is passed as a parameter for the use
        of the API. A page offset is passed as a parameter to print other pages of the api output.
        This function is called in the serpapi_search function. """
    # python dictionary of the parameters
    search_parameters = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "hl": "en",
        "google_domain": "google.com",
        "api_key": api_key,
        "start": page_offset
    }
    return search_parameters


def serpapi_search(query, location, api_key, page_number, page_offset):
    """ This function generates a search query based on parameters.
        This function calls the search_parameters function to get the parameters dictionary
        and then calls the serpapi google search with the parameters
        and returns the json_data results as a dictionary."""
    if not location.strip():
        print(f"Generating Page {page_number} results for {query} positions in no specific location")
    else:
        print(f"Generating Page {page_number} results for {query} positions near {location}...\n")
    # function call to generate parameter dictionary
    search_parameters = create_search_parameters(query, location, api_key, page_offset)
    # serpapi call
    search = GoogleSearch(search_parameters)
    # get results as dictionary
    results = search.get_dict()
    return results


def perform_single_search(query, location, page, page_offset, file):
    """ This function performs a single search based on the generated query. It writes the json results
    to a file by calling the write_page_to_file function. This function passed the desired file
    and page as a parameter. A secret api key is fetched from a secret file for security."""
    # call secret handling function to make sure exceptions are handled if no secret found
    secret_api_key = secrets_handling()
    search_results_as_json = serpapi_search(query, location, secret_api_key, page, page_offset)
    write_page_to_file(search_results_as_json, page, file)


def perform_search(num_pages, file):
    """ This function performs multiple searches based on the number of pages passed as a parameter
    and writes to the desired file. The function keeps track of a page offset variable to print
    the next page of the Google results. This function uses a loop to execute multiple
    searches and is wrapped inside a try except statement to catch any exceptions that occur. """
    # page offset variable to keep track of the current page, starts at 0 for page 1 in serpapi results
    page_offset = 0
    # try except block to handle any exceptions likely caused by user-input error.
    try:
        # simultaneous assignment of query and location based on user input function call.
        query, location = get_user_input()
        # write header to desire file by calling function with query, location, and desired file
        write_file_header(query, location, file)
        # loops based on the page amount, for each page perform a search, everytime a loop occurs
        # the page offset increases to generate multiple pages of results
        for page in range(1, num_pages + 1):
            perform_single_search(query, location, page, page_offset, file)
            # increment page offset by 10, which means one page
            page_offset += 10
        # debug message for the user
        print("Finished! Please check your results in the 'results.txt' file")
    # catch any exceptions and print error message
    except Exception as exception:
        print(f"Oh nos! An error occurred: {exception}")
        print("Did you create a secrets.py file?")
