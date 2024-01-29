Name
-
Samuel Rantz

Install/Run directions


- Open your terminal in desired location
- Clone the repository: git clone https://github.com/SamuelR827/SRantz_Project1JobsPython.git
- Make sure requirements are configured properly (see below)
- Make sure to configure your secrets! (see below)
- Find the main.py file using your terminal
- Run the main python script by typing "python main.py" in your terminal
- Follow directions that print in the script
- Find your results.txt file in project directory

Requirements

- Git (only to clone the project)
- Python 3.9 or 3.10 (python --version)
- This project should handle standard python packages for you.
- The project relies on a library known as serpAPI to fetch google results.
- If you have issues with the project running. You are likely missing the serpAPI package, and python is not detecting any serpAPI packages. Run these commands to install the package
- Install pip in terminal
    - linux: python -m ensurepip --upgrade
    - mac: python -m ensurepip --upgrade
    - windows: py -m ensurepip --upgrade
- Install serpAPI in your project directory
    - pip install google-search-results

Secrets.py

- The user must create a secrets.py file in the project directory and type in a single line of code
- secret_api_key = "insert your api key here"

This project prompts the user to search for a job. The user doesn't have to enter there api key everytime they perform
a search.
However, they must have there secrets.py file configured properly in the project directory.
The user must type in a job they would like to search for and press enter. Optionally it will ask the user
to specify a location for that job. The user may type in a location and
press enter or leave the location blank to skip. This program will then use serpAPI to perform a Google search
of the user's entered job and generate json results in a text file.
This file will be named results.txt and in the project directory that was cloned.
By default, 5 pages of results will be generated with each page being clearly seperated.
This can be changed in the main.py file with any python compatible text editor.
Only json data is generated for now, no metadata will be included.

I don't believe there is anything missing from the project.