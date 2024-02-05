""" This module handles utility functions used in the project for easier modification.
    These functions include prompting the user and writing data to a file.
    Many of the functions defined in this file may be modified depending on how the
    data generated will be used in this project, or new functions may be created instead.
"""


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
