""" This module handles automated unit tests. We have two automated tests.
    One test retrieves the data from the web and assure that it gets at least 50 data items.
    The second test should create a new empty database, run the table creation function,
    then run the save data to database function to check to see
    that the database contains the test jobs."""

import pytest

from ..database_functions import create_db_connection
from ..database_functions import create_table_job_links
from ..database_functions import create_table_job_list
from ..database_functions import create_table_job_qualifications
from ..database_functions import save_data_to_database
from ..serpAPI import secrets_handling
from ..serpAPI import serpapi_search


@pytest.fixture(scope="module")
def mock_db_connection():
    db_file = 'test_results.db'
    test_connection, test_cursor = create_db_connection(db_file)

    create_table_job_qualifications(test_cursor)
    create_table_job_links(test_cursor)
    create_table_job_list(test_cursor)

    yield test_connection, test_cursor
    test_cursor.close()
    test_connection.commit()
    test_connection.close()


def test_save_data_to_database(mock_db_connection):
    test_connection, test_cursor = mock_db_connection

    # sample data
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
    save_data_to_database(test_cursor, test_json_job_data)
    # Check if the test data exists in the database
    test_cursor.execute('''SELECT * FROM jobs WHERE title = "Some Job Title"''')
    result = test_cursor.fetchone()
    assert result is not None


def test_search_results_count():
    result_count = 0
    query = "computer programmer"
    location = "new york"
    api_key = secrets_handling()
    page_offset = 0
    num_pages = 5
    for page in range(1, num_pages + 1):
        search_results_as_json = serpapi_search(query, location, api_key, page, page_offset)
        result_count += len(search_results_as_json)
        page_offset += 10
    assert result_count >= 50, f"Expected at least 50 data items, but got {result_count}"
