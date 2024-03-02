# pylint: disable=unused-variable
import sys

from database_functions import get_all_job_data_from_table
from database_functions import get_all_job_links_from_table
from database_functions import get_all_job_qualifications_from_table
import PySide6.QtWidgets
import gui.list_window


def display_job_list_data(cursor):
    qt_app = PySide6.QtWidgets.QApplication(sys.argv)  # sys.argv is the list of command line arguments
    job_data = get_job_data_for_gui(cursor)
    job_list_window = gui.list_window.JobsListWindow(job_data)
    sys.exit(qt_app.exec())


def get_job_links_for_gui(cursor, job_id):
    job_link_list = []
    link_data = get_all_job_links_from_table(cursor, job_id)
    for link_entry in link_data:
        job_link_list.append(link_entry[2])
    return job_link_list


def get_job_qualifications_for_gui(cursor, job_id):
    job_qualification_list = []
    qualification_data = get_all_job_qualifications_from_table(cursor, job_id)
    for qualification_entry in qualification_data:
        job_qualification_list.append(qualification_entry[2])
    return job_qualification_list


def get_job_data_for_gui(cursor):
    final_data_list = []
    job_data = get_all_job_data_from_table(cursor)
    for job_entry in job_data:
        job_id = job_entry[0]
        job_title = job_entry[1]
        company_name = job_entry[2]
        job_description = job_entry[3]
        job_location = job_entry[4]
        job_remote = job_entry[5]
        job_posted = job_entry[6]
        salary_min = job_entry[7]
        salary_max = job_entry[8]
        salary_rate = job_entry[9]
        job_links = get_job_links_for_gui(cursor, job_id)
        job_qualifications = get_job_qualifications_for_gui(cursor, job_id)
        if not job_links:
            job_links = "N/A"
        if not job_qualifications:
            job_qualifications = "N/A"
        record = {"job_id": job_id, "job_title": job_title, "company_name": company_name,
                  "job_description": job_description, "job_location": job_location, "job_remote": job_remote,
                  "job_posted": job_posted, "salary_min": salary_min, "salary_max": salary_max,
                  "salary_rate": salary_rate, "job_links": job_links, "job_qualifications": job_qualifications}
        final_data_list.append(record)
    return final_data_list
