""" This is the main module for executing the problem. One main function is included in this
module for executing the program. """

from serpAPI import perform_search


def main():
    """ The main function for running the program. Opens a file based on a hard-coded filename
        and calls the perform_search function from the serpapi module with the created file as well as
        hard-coded number of pages to generate. """
    # hardcoded variable for filename for now
    # you may change this if desired
    filename = "results.txt"
    # hardcoded variable for desired amount of pages for now
    # you may change this if desired
    num_pages = 5
    # open file using with open to properly close file in case of exceptions
    with open(filename, "w") as file:
        # call perform_search function with created file and desired page count
        perform_search(num_pages, file)


if __name__ == "__main__":
    main()
