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
- A GUI will open that the user can filter through the list of data. View details for each data and map for all the filtered data
- To apply and filters in text fields you must hit the apply filter button

Requirements

- Git (only to clone the project)
- DBBrowserLite or Pycharm Professional to view database.
- Python 3.12(python --version) - I had to update to 3.12 to solve an issue with pyside6. If you have issues with older python versions try 3.12
- This project should handle standard python packages for you. If not see requirements.txt
- Run this command to instal all required packages
- Install pip in terminal
    - linux: python -m ensurepip --upgrade
    - mac: python -m ensurepip --upgrade
    - windows: py -m ensurepip --upgrade
- Install all required packages
  pip install -r requirements.txt

*** NOTE!!!! Past versions of the program used the file secrets.py
for secret handling, this was renamed to secrets_file.py to avoid issues with
an import error. If you are having issues with your secrets file this is why***

secrets_file.py

- The user must create a file named "secrets_file.py" in the project directory and type in a single line of code
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

A GUI will be created after a search is finished. From here the user can view all jobs in a list 
containing the job name and company name. The user can also view more information on a single job by clicking on a job 
from the list. The user can also filter out jobs by keyword, location, if the job is remote or not, and minimum salary.
The user can also view the data on a map that points to where the job is located. The map will only 
display the data that is on the list. So if the user filtered out data, only the filtered data will have markers. If you hit
the apply filter button with the map open, you will have to reopen the map.

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
job entry's extensions called work from home. It will show yes if the work from home key is found.

The posted column will look for key/value pair in the job entry's extensions
called posted_at. If that key/value pair is found it will show the value for that key.

The salary (min and max) is found using Professor Santore's function to find the salary in his
Sprint3Solution. The rate is found based on the value of the minimum salary. Hourly if less than
900, yearly if more than 900. N/A if 0.

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

I don't believe there is anything missing from the project. But this project cannot handle every
single odd case for where information is found in the json_data.

The map generates pretty slow if you have alot of data in the filter, for example if you don't filter everything.
I implemented caching to help with the performance, but I am not sure if it helps or if I did it correctly.
Some of the data will be skipped on the map if it's location isn't recognized by folium. (I.E to small of a city).
