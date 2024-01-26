""" This is a testing module to test for how the output will write to the file. I will include
more unit tests as the project is expanded more."""
from io import StringIO

from util_functions import clean_data_from_json
from util_functions import write_file_header


def test_write_page_header():
    # Test case to make sure header prints
    file = StringIO()
    write_file_header('Software Engineer', 'New York', file)
    file.seek(0)
    content = file.read()
    assert 'Generated output for Software Engineer in New York.' in content


def test_clean_data_no_metadata():
    # Test case where search_metadata key is present
    json_data = {
        "results": [{"title": "Job Result 1"}, {"title": "Job Result 2"}],
        "search_metadata": {"some_key": "some_value"}
    }
    cleaned_data = clean_data_from_json(json_data)
    # Ensure search_metadata key is removed
    assert ('search_metadata' in cleaned_data) is False
