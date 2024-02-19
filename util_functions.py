""" This module handles utility functions used in the project for easier modification.
    These functions include prompting the user and finding certain values in the jobs dictionary
    and returning a certain value if a key/value is found in the job's dictionary.
    Many of the functions defined in this file may be modified depending on how the
    data generated will be used in this project, or new functions may be created instead.
"""
import re
from typing import Tuple, Optional, List, Dict, Any, Union


def get_user_input() -> Tuple[str, str]:
    """ This function handles prompting the user for input. Asking the user
        to enter their desired job and location and simultaneously return
        the query and location. """
    print('Please perform a Google job search...\n')
    # use a while loop to catch if user actually enters a query
    while True:
        # Prompt the user for a job query
        query = input('Please enter a job you would like to search for (Required): ')
        # Check if the job query is blank, re loop if left blank
        if not query.strip():
            print('Job query cannot be blank. Please enter a valid job.')
            continue
        # Prompt the user for a location
        location = input('Please enter your desired location for this job '
                         '(Optional: Leave blank for no specific location): ')

        # Return query and location as strings
        return query, location


def find_remote_in_job(job_entry: Dict[str, Any]) -> str:
    """ This function searches through a specified job's dictionary
    and looks for the work_from_home key in the job_extensions dictionary.
    If the key is present in the job_extensions dictionary and is true
    it will return yes. Otherwise, it will return no. The function will also return yes
     if the job's location is Anywhere."""
    # get the job_extensions dictionary and the work_from_home key
    job_extensions = job_entry.get('detected_extensions')
    work_from_home = job_extensions.get('work_from_home', None)
    # return yes if job location is anywhere as that means remote work is possible
    if job_entry.get('location').strip() == 'Anywhere':
        return 'Yes'
    # return yes if work_from_home value is found/not none
    elif work_from_home:
        return 'Yes'
    else:
        return 'No'


def find_job_age(job_entry: Dict[str, Any]) -> str:
    """ This function searches through a specified job's posted date. It looks
    through the list of keys in the detected_extensions dictionary. Looking
    for a key named posted_at returning it if found. And returning text
    to specify the user it wasn't found if the posted_at key does not exist."""
    # find job_extensions dictionary
    job_extensions = job_entry.get('detected_extensions')
    # find posted_at key in extensions dictionary and get its value
    posted_at = job_extensions.get('posted_at', None)
    # if key doesn't exist print generic message
    if posted_at is None:
        return 'No Job Posted Date Specified'
    # if found key/value pair return the posted_at date stripped
    if posted_at is not None:
        return posted_at.strip()


# flake8: noqa: C901
def find_job_salary(job_entry: Dict[str, Any]) -> Tuple[int, int]:
    """This code is taken from Professor Santore's GitHub solution from sprint 2.
    It was slightly modified to work with my program."""
    # create empty benefits dictionary
    benefits_section = {}
    # get job highlights
    job_highlights = job_entry.get('job_highlights')
    # loop through each highlight dictionary, if it has a key named title and value
    # benefits, the benefits section dictionary becomes the current dictionary
    for highlight in job_highlights:
        if highlight.get('title') == 'Benefits':
            benefits_section = highlight
    # base values for min and max salary
    min_salary = 0
    max_salary = 0
    if benefits_section:  # if we got a dictionary with stuff in it
        for benefit_item in benefits_section['items']:
            if 'range' in benefit_item.lower():
                # from https://stackoverflow.com/questions/63714217/how-can-i-extract-numbers-containing-commas-from
                # -strings-in-python
                numbers = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?!\d)', benefit_item)
                if numbers:  # if we found salary data, return it
                    return int(numbers[0].replace(',', '')), int(numbers[1].replace(',', ''))
            numbers = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?!\d)', benefit_item)
            if len(numbers) == 2 and int(float(
                    numbers[0].replace(',', ''))) > 30:  # some jobs just put the numbers in one item
                # and the description in another
                return int(numbers[0].replace(',', '')), int(numbers[1].replace(',', ''))
            else:
                return min_salary, max_salary
    # find description entry
    job_description = job_entry.get('description')
    # variable to keep track of pay range location job description
    location = job_description.find('salary range')
    # look for pay range in job description and update location if found
    if location < 0:
        location = job_description.find('pay range')
    if location < 0:
        return min_salary, max_salary
    numbers = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?!\d)', job_description[location:location + 50])
    if numbers:
        return int(numbers[0].replace(',', '')), int(numbers[1].replace(',', ''))
    return min_salary, max_salary


def find_job_rate(min_salary: int) -> str:
    """ This function gets the salary rate either hourly or yearly based on the
    value of the minimum salary passed as a parameter. A min salary 900 or less
    will result in hourly. """
    # default to NA
    salary_time_period = 'N/A'
    # If between 0 and 900 it's an hourly salary
    if 0 < min_salary < 900:
        salary_time_period = 'Hourly'
    # Otherwise, if greater than 0 it's a yearly salary
    elif min_salary > 0:
        salary_time_period = 'Yearly'
    return salary_time_period


def find_job_qualifications(job_entry: Dict[str, Any]) -> List[str]:
    """ This function searches through a specified job's qualifications. It looks through the job_highlights
      key which it's value is a list of dictionary's. The function will
      look for a dictionary key/value pair named 'qualification'
       and return the items of the dictionary which is a list of strings."""
    # find job highlights list
    job_highlights: Optional[List[Dict[str, Any]]] = job_entry.get('job_highlights', None)
    # return a single item in a list to specify no qualifications found if no job highlights
    if job_highlights is None:
        return ['No Qualifications Specified']
    # loop through each highlight in highlights list to find a dictionary with
    # the key value pair 'title: Qualifications'
    for highlight in job_highlights:
        # if matching key/value pair found return the value of
        # the key items which is a list of strings
        if highlight.get('title') == 'Qualifications':
            return highlight.get('items')
    # return a single item in a list to specify no qualifications
    # found if no qualifications key/value pair
    return ['No Qualifications Specified']


def find_job_links(job_entry: Dict[str, Any]) -> Union[List[str], List[Dict[str, Any]]]:
    """ This function searches through a specified job's related links. It finds
    the related links key/value pair which is a list of dictionaries. It will return that dictionary
    unless there was no key found for related links"""
    # find related links list
    related_links: Optional[List[Dict[str, Any]]] = job_entry.get('related_links')
    # if no related links list value found return single item list
    # to specify the user no links found
    if related_links is None:
        return ['No Related Links Specified']
    # otherwise return the related_links dictionary
    return related_links
