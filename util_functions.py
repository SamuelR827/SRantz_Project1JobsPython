""" This module handles utility functions used in the project for easier modification.
    These functions include prompting the user and finding certain values in the jobs dictionary
    and returning a certain value if a key/value is found in the job's dictionary.
    Many of the functions defined in this file may be modified depending on how the
    data generated will be used in this project, or new functions may be created instead.
"""
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
    # return no if no work_from_home key is in the job entry
    if work_from_home is None:
        return 'No'
    # return yes if the work_from_home value is True
    if work_from_home == 'True':
        return 'Yes'
    # return no if no other case was satisfied
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


def find_job_salary(job_entry: Dict[str, Any]) -> str:
    """ This function searches through a specified job's salary. It looks through the job_highlights
    key which it's value is a list of dictionary's. The function looks for a dictionary
    with the key/value pair. title:Benefits. If found it will look through the Benefits items which is a list
    of strings. It will look for any strings that contain the words, salary, pay or the $ and return this string."""
    # find job highlights list
    job_highlights: Optional[List[Dict[str, Any]]] = job_entry.get('job_highlights', None)
    # return no salary if there is no job highlights list
    if job_highlights is None:
        return 'No Salary Specified'
    # loop through each highlight in highlights list to find a dictionary with
    # the key value pair 'title: Benefits'
    for highlight in job_highlights:
        if highlight.get('title') == 'Benefits':
            # if found key/value pair match create a list of strings from benefits
            benefits = highlight.get('items', [])
            # loop through each benefit and check if each benefit contain keywords
            # if match return the benefit
            for benefit in benefits:
                if 'salary:' in benefit.lower() or 'pay:' in benefit.lower() or '$' in benefit:
                    return benefit.strip()
            # return no salary specified if no benefit containing keywords fond
            return 'No Salary Specified'
        # return no salary specified if no benefits key/value pair found
    return 'No Salary Specified'


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
