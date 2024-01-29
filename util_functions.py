""" This module handles utility functions used in the project for easier modification.
    These functions include prompting the user and writing data to a file.
    Many of the functions defined in this file may be modified depending on how the
    data generated will be used in this project, or new functions may be created instead.
"""

import json

# line seperator global variable to use in write_page_to_file function
line_seperator = "\n" + ("-" * 256) + "\n"


def get_user_input():
    """ This function handles prompting the user for input. Asking the user
        to enter their desired job and location and simultaneously return
        the query and location. """
    print("Please perform a Google job search...\n")
    # use a while loop to catch if user actually enters a query
    while True:
        # Prompt the user for a job query
        query = input("Please enter a job you would like to search for (Required): ")
        # Check if the job query is blank, re loop if left blank
        if not query.strip():
            print("Job query cannot be blank. Please enter a valid job.")
            continue
        # Prompt the user for a location
        location = input("Please enter your desired location for this job "
                         "(Optional: Leave blank for no specific location): ")

        # Return query and location as strings
        return query, location


def write_file_header(query, location, file):
    """ This function writes a header description to the top of the
        output file. The header includes the users entered query and location.
        If no location is specified, then it will print that no specific location
        was entered."""
    if not location.strip():
        page_header = f"Generated output for {query} in no specific location.\n"
    else:
        page_header = f"Generated output for {query} near {location}.\n"
    file.write(page_header)


def write_page_to_file(json_data, page, file):
    """ This function writes an individual page to the output file passed as a parameter.
        Each page will be seperated by a separation string at the end of the output
        and the output will start with the page # for the user. Depending on how we use
        the data, this will likely be changed in the future. The json data is passed as a
        parameter and converted into a string using the json dumps method."""
    # define page number string
    page_number_to_write = "Page " + str(page) + "\n"
    # call clean_data_from_json function to remove unnecessary keys from output
    # keep just actual job search_results
    json_data_no_metadata = clean_data_from_json(json_data)
    # dump json object into string using json dumps.
    lines_to_write = json.dumps(json_data_no_metadata, indent=4)
    # write page #, json data as a string, and line seperator to file
    file.write(page_number_to_write)
    file.write(lines_to_write)
    file.write(line_seperator)


def clean_data_from_json(json_data):
    """ This function removes all unnecessary keys from the json_data, since the
    data is read as a python dictionary. All the unnecessary keys(search_metadata, search_parameters,
    chips) are popped if found."""
    # pop search_metadata key if found
    if 'search_metadata' in json_data:
        json_data.pop('search_metadata')
    # pop search_parameters key if found
    if 'search_parameters' in json_data:
        json_data.pop('search_parameters')
    # pop chips key if found
    if 'chips' in json_data:
        json_data.pop('chips')
    # return new json data without unnecessary keys
    return json_data
