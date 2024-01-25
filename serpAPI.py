from serpapi import GoogleSearch

from secrets import secret_api_key
from util_functions import write_page_header
from util_functions import write_page_to_file
from util_functions import get_user_input


def create_search_parameters(query, location, api_key, page_offset):
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
    print(f"Generating Page {page_number} results for {query} positions in {location}...\n")
    search_parameters = create_search_parameters(query, location, api_key, page_offset)
    search = GoogleSearch(search_parameters)
    results = search.get_dict()
    return results


def perform_single_search(query, location, page, page_offset, file):
    search_results_as_json = serpapi_search(query, location, secret_api_key, page, page_offset)
    write_page_to_file(search_results_as_json, page, file)


def perform_search(num_pages, file):
    page_offset = 0
    try:
        query, location = get_user_input()
        write_page_header(query, location, file)

        for page in range(1, num_pages + 1):
            perform_single_search(query, location, page, page_offset, file)
            page_offset += 10

        print("Finished! Please check your results in the 'results.txt' file")
    except Exception as exception:
        print(f"Oh nos! An error occurred: {exception}")
