""" This module handles automated unit tests. We have two automated tests.
    One test retrieves the data from the web and assure that it gets at least 50 data items.
    The second test should create a new empty database, run the table creation function,
    then run the save data to database function to check to see
    that the database contains the test jobs."""
from sqlite3 import Connection, Cursor
from typing import Generator, Any

import pytest

from database_functions import create_db_connection
from database_functions import create_table_job_links
from database_functions import create_table_job_list
from database_functions import create_table_job_qualifications
from database_functions import save_data_to_database
from serpAPI import secrets_handling
from serpAPI import serpapi_search


@pytest.fixture(scope="module")
def mock_db_connection():
    """ This function creates a mock database for testing the function
    that saves data to the database."""
    # create a mock db_file
    db_file = 'test_results.db'
    # create a mock connection and cursor
    test_connection, test_cursor = create_db_connection(db_file)

    # create mock tables by calling database create tables function
    create_table_job_qualifications(test_cursor)
    create_table_job_links(test_cursor)
    create_table_job_list(test_cursor)

    # teardown/cleanup of connection and cursor
    yield test_connection, test_cursor
    # commit and close
    test_cursor.close()
    test_connection.commit()
    test_connection.close()


def test_save_data_to_database(mock_db_connection: Generator[tuple[Connection, Cursor], Any, None]) -> None:
    """ This function tests the save_data_to_database function. Making
    sure that the database is created properly and inserted with jobs data."""
    # call mock_db_connection to create test cursor and connection
    test_connection, test_cursor = mock_db_connection
    # sample data in json format
    test_json_job_data = [
        {"title": "Some Job Title",
         "company_name": "Some Company Name",
         "location": "Some Location",
         "via": "Some Via",
         "description": "Some Description",
         "job_highlights":
             [
                 {
                     "title": "Qualifications",
                     "items": [
                         "Qualification 1", "Qualification 2"
                     ]
                 },
                 {
                     "title": "Responsibilities",
                     "items": [
                         "Responsibility 1", "Responsibility 2"
                     ]
                 },
                 {
                     "title": "Benefits",
                     "items": [
                         "Salary $0 - 100"
                     ]
                 }
             ],
         "related_links": [
             {
                 "link": "https://example.com",
                 "text": "Link Title"
             }],
         "thumbnail": "https://examplethumb.com",
         "extensions":
             [
                 "some time ago",
                 "some information"
             ],
         "detected_extensions": {
             "posted_at": "some time ago"},
         "job_id": "some job id"
         },
    ]
    # call function to test saving data
    save_data_to_database(test_cursor, test_json_job_data)
    # Check if the test data exists in the database
    test_cursor.execute('''SELECT * FROM jobs WHERE title = "Some Job Title"''')
    # fetch the single result and create a variable
    result = test_cursor.fetchone()
    # assert the result is not null
    assert result is not None


def test_search_results_count() -> None:
    """ This function tests to make sure 50 search results are generated with
    serpapi_search when 5 pages are given. Test is a mock form of perform_search
    function in main module. """
    # variable to count the results
    result_count = 0
    # sample query and location
    query = "computer programmer"
    location = "new york"
    # get api key with secret handling
    api_key = secrets_handling()
    # keep track of pages
    page_offset = 0
    # variable to generate 5 pages - 50 results
    num_pages = 5
    # loop based on the amount of pages specified
    for page in range(1, num_pages + 1):
        # call serpapi search with sample query and return jobs_results as json
        search_results_as_json = serpapi_search(query, location, api_key, page, page_offset)
        # count each item in the list jobs_results
        result_count += len(search_results_as_json)
        # increment page offset
        page_offset += 10
    # make sure the result count is greater or equal to 50, print failing message otherwise
    assert result_count >= 50, f"Expected at least 50 data items, but got {result_count}"
