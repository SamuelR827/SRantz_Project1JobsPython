import sys

from database_functions import get_all_job_data_from_table
import PySide6.QtWidgets
import gui.list_window


def display_job_list_data(cursor):
    qt_app = PySide6.QtWidgets.QApplication(sys.argv)  # sys.argv is the list of command line arguments
    job_data = get_job_data_for_gui(cursor)
    job_list_window = gui.list_window.JobsListWindow(job_data)
    sys.exit(qt_app.exec())


def get_job_data_for_gui(cursor):
    final_data_list = []
    job_data = get_all_job_data_from_table(cursor)
    for job_entry in job_data:
        job_id = job_entry[0]
        job_title = job_entry[1]  # Assuming the job title is the first element of the tuple
        record = {"job_id": job_id, "job_title": job_title}
        final_data_list.append(record)
    return final_data_list
