def main():
    """ The main function for running the program. Opens a file based on a hard-coded filename
        and calls the perform_search function from the serpapi module with the created file as well as
        hard-coded number of pages to generate. """
    try:
        # hardcoded variable for filename for now
        # you may change this if desired
        filename = "results.txt"
        # hardcoded variable for desired amount of pages for now
        # you may change this if desired
        num_pages = 5
        # open file using with open to properly close file in case of exceptions
        with open(filename, "w") as file:
            try:
                # Import inside the try block to catch ImportError
                from secrets import perform
            except ImportError as import_error:
                print("Oh nos! An ImportError has occurred. Did you create a secrets.py file?")
                print(import_error)
                return  # Return or handle the exception as needed
            # Now that the import is successful, call perform_search function
            from serpAPI import perform_search
            perform_search(num_pages, file)
    except Exception as exception:
        print("Oh nos! An error has occurred.")
        print(exception)


if __name__ == "__main__":
    main()
