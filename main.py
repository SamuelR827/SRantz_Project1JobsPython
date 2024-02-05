""" This is the main module for executing the problem. One main function is included in this
module for executing the program. """
from serpAPI import secrets_handling
from serpAPI import serpapi_search
from util_functions import get_user_input


def perform_search(num_pages):
    """ This function performs multiple searches based on the number of pages passed as a parameter
    and writes to the desired file. The function keeps track of a page offset variable to print
    the next page of the Google results. This function uses a loop to execute multiple
    searches and is wrapped inside a try except statement to catch any exceptions that occur. """
    secret_api_key = secrets_handling()
    # page offset variable to keep track of the current page, starts at 0 for page 1 in serpapi results
    page_offset = 0
    # try except block to handle any exceptions likely caused by user-input error.
    try:
        # simultaneous assignment of query and location based on user input function call.
        query, location = get_user_input()
        # loops based on the page amount, for each page perform a search, everytime a loop occurs
        # the page offset increases to generate multiple pages of results
        for page in range(1, num_pages + 1):
            search_results_as_json = serpapi_search(query, location, secret_api_key)

            # increment page offset by 10, which means one page
            page_offset += 10
    # catch any exceptions and print error message
    except Exception as exception:
        print(f"Oh nos! An error occurred: {exception}")
        print("Did you create a secrets.py file?")


def main():
    """ The main function for running the program. Opens a file based on a hard-coded filename
    and calls the perform_search function from the serpapi module with the created file as well as
    hard-coded number of pages to generate. """
    # hardcoded variable for desired amount of pages for now
    # you may change this if desired
    num_pages = 5
    # call perform_search function with desired page count
    perform_search(num_pages)


if __name__ == "__main__":
    main()
