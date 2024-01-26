""" This module handles utility functions used in the project for easier modification.
    These functions include prompting the user and writing data to a file.
    Many of the functions defined in this file may be modified depending on how the
    data generated will be used in this project, or new functions may be created instead.
"""

import json

# line seperator global variable to use in write_page_to_file function
line_seperator = "\n" + ("-" * 256) + "\n"


def get_user_input():
    """ This function handles prompting user for input. Asking the user
        to enter there desired job and location and simultaneous return
        the query and location. """
    # debug print for additional information/ indication for user
    print("Please perform a Google job search...\n")
    # prompt user for location and query
    query = input("Please enter a job you would like to search for: ")
    location = input("Please enter your desired location for this job: ")
    # return query and location as string
    return query, location


def write_file_header(query, location, file):
    """ This function writes a header description to the top of the
        output file. The header includes the users entered query and location. """
    page_header = f"Generated output for {query} in {location}.\n"
    file.write(page_header)


def write_page_to_file(json_data, page, file):
    """ This function writes an individual page to the output file passed as a parameter.
        Each page will be seperated by a separation string at the end of the output
        and the output will start with the page # for the user. Depending on how we use
        the data, this will likely be changed in the future. The json data is passed as a
        parameter and converted into a string using the json dumps method."""
    # define page number string
    page_number_to_write = "Page " + str(page) + "\n"
    # dump json object into string using json dumps.
    lines_to_write = json.dumps(json_data, indent=4)
    # write page #, json data as a string, and line seperator to file
    file.write(page_number_to_write)
    file.write(lines_to_write)
    file.write(line_seperator)
