""" This is the main module for executing the problem. One main function is included in this
module for executing the program. """
import sqlite3
import sys

from database_functions import create_db_connection
from database_functions import db_close
from database_functions import save_searched_data_to_database
from database_functions import setup_db
from excel_functions import add_excel_job_data
from excel_functions import load_job_workbook
from serpAPI import secrets_handling
from serpAPI import serpapi_search
from util_functions import get_user_input


def perform_search(cursor: sqlite3.Cursor, num_pages: int) -> None:
    """ This function performs multiple searches based on the number of pages passed as a parameter
    and saves the data to a database. The function keeps track of a page offset variable to print
    the next page of the Google results. This function uses a loop to execute multiple
    searches and is wrapped inside a try except statement to catch any exceptions that occur. """
    # call secrets handling function to cancel if no secret.py file is found
    secret_api_key = secrets_handling()
    # if secret_api_key returns no secrets and return to prevent rest of the function from running
    if secret_api_key == 'No secrets':
        sys.exit('Oh nos! An error occurred: Missing API key. Did you create a secrets.py file?')
    # page offset variable to keep track of the current page, starts at 0 for page 1 in serpapi results
    page_offset = 0
    # try except block to handle any exceptions likely caused by user-input error.
    try:
        # simultaneous assignment of query and location based on user input function call.
        query, location = get_user_input()
        # loops based on the page amount, for each page perform a search, everytime a loop occurs
        # the page offset increases to generate multiple pages of results
        for page in range(1, num_pages + 1):
            # call serpapi search to get the json results
            search_results_as_json = serpapi_search(query, location, secret_api_key, page, page_offset)
            # if search results is None, raise a ValueError
            if search_results_as_json is None:
                raise ValueError("Search returned no results.")
            # add json results to the database by calling the save database function
            save_searched_data_to_database(cursor, search_results_as_json)
            # increment page offset by 10, which means one page
            page_offset += 10
        # finish print message for the user
        print("Finished! Please check your database in the project directory...")
    # catch any exceptions and print error message
    except Exception as exception:
        sys.exit(f'Oh nos! An error occurred: {exception}')


def main() -> None:
    """ The main function for running the program. Creates a connection to sqlite to handle generated data
    and calls the perform_search function to generate that data with the created database as well as
    hard-coded number of pages to generate. A workbook is created for the job data in the Excel sheet
    and all the data from the Excel sheet is added to the database. """
    # hardcoded variable for desired amount of pages for now
    # you may change this if desired
    num_pages = 1
    # call load_job_workbook function to initialize workbook
    job_workbook = load_job_workbook()
    # create database connection by calling the connection function
    connection, cursor = create_db_connection('job_results.db')
    # call the database function
    setup_db(cursor)
    # call perform_search function with desired page count
    perform_search(cursor, num_pages)
    # call add_excel_job_data function to add excel data to database
    add_excel_job_data(cursor, job_workbook)
    # close the database by calling the close database function
    db_close(connection)


if __name__ == '__main__':
    main()
