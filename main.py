""" This is the main module for executing the problem. One main function is included in this
module for executing the program. """
from serpAPI import secrets_handling
from serpAPI import serpapi_search
from util_functions import get_user_input
from database_functions import insert_data_to_table
from database_functions import create_db_connection
from database_functions import setup_db
from database_functions import db_close


def perform_search(cursor, num_pages):
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
            search_results_as_json = serpapi_search(query, location, secret_api_key, page, page_offset)
            insert_data_to_table(cursor, search_results_as_json)
            # increment page offset by 10, which means one page
            page_offset += 10
    # catch any exceptions and print error message
    except Exception as exception:
        print(f"Oh nos! An error occurred: {exception}")


def main():
    """ The main function for running the program. Opens a file based on a hard-coded filename
    and calls the perform_search function from the serpapi module with the created file as well as
    hard-coded number of pages to generate. """
    # hardcoded variable for desired amount of pages for now
    # you may change this if desired
    num_pages = 1
    connection, cursor = create_db_connection("job_results.db")
    setup_db(cursor)
    # call perform_search function with desired page count
    perform_search(cursor, num_pages)
    db_close(connection)


if __name__ == "__main__":
    main()
