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
- Find your job_results.db file in project directory
- View the database in either db_browser or IDE built in database viewer

Requirements

- Git (only to clone the project)
- DBBrowserLite or Pycharm Professional to view database.
- Python 3.9 or 3.10 (python --version)
- This project should handle standard python packages for you. If not see requirements.txt
- The project relies on a library known as serpAPI to fetch google results.
- If you have issues with the project running. You are likely missing the serpAPI package, and python is not detecting
  any serpAPI packages. Run these commands to install the package
- Install pip in terminal
    - linux: python -m ensurepip --upgrade
    - mac: python -m ensurepip --upgrade
    - windows: py -m ensurepip --upgrade
- Install serpAPI in your project directory
    - pip install google-search-results
- Install openpyxl in your project directory
  - pip install openpyxl

secrets.py

- The user must create a file named "secrets.py" in the project directory and type in a single line of code
- api_key = "insert your api key here"
- Otherwise, the project will not run

This project prompts the user to search for a job. The user doesn't have to enter there api key everytime they perform
a search. However, they must have there secrets.py file configured properly in the project directory.
The user must type in a job they would like to search for and press enter. Optionally it will ask the user
to specify a location for that job. The user may type in a location and
press enter or leave the location blank to skip. This program will then use serpAPI to perform a Google search
of the user's entered job and generate json results into a database. The program will also
fetch data from an Excel spreadsheet provided in the project. Some of this spreadsheet has missing
data, so for that missing data in the database it will be set to N/A.

The database is named job_results.db and in the project directory that was cloned.
Three tables are generated jobs, job_links, job_qualifications.

The jobs table contains columns for job_id as a primary key.
The job title, the company name, the description of the job, the job
location, if the job is remote or not, the job posted date, and the job salary(min, max and rate).
Most of these columns simply find a corresponding key/value pair in the job entry. Each
job is its own row. Some job may have some values that are not specified in will show
up in the database as not specified. All of this data is found from the job_entries
json entry and give the user information about the job_entry.

The remote column will first look if the job location is set to 'Anywhere'
it will show yes if that is the case. Otherwise, it will look for a key/value pair in
job entry's extensions called work from home. It will show yes if that value is true
in the results.

The posted column will look for key/value pair in the job entry's extensions
called posted_at. If that key/value pair is found it will show the value for that key.

The salary (min and max) is found using Professor Santore's function to find the salary in his
Sprint3Solution. The rate is found based on the min salary.

There is two other tables for job_qualifications and job_links. Which are
separate tables but use the job_id as foreign key to correspond to each database.

Job Qualifications is found by searching through the list of job highlights.
There will be a dictionary named Qualifications with the has a key named items.
These items are list of strings. Each string will show as a separate row with their own unique
id. But it will also show the job_id it corresponds to.

Job Links is found by searching through a list named related_links in the job entry.
This is a list of dictionary's. Each dictionary has the key named link with the value
of the link as string. Each job link will show as a separate row in the table with the own unique
id. But it will also show the job_id it corresponds to.

By default, 5 pages of results will be generated (50 job entries).
This can be changed in the main.py file with any python compatible text editor.

I don't believe there is anything missing from the project. There are some columns such as
salary which may have information in the description. But this project cannot handle every
single odd case for where information is found in the json_data.
