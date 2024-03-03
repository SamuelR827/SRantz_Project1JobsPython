from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QPushButton, QListWidget, QApplication, QListWidgetItem, QLabel,
                               QVBoxLayout, QLineEdit, QCheckBox)

import gui.detail_window as detail_window
import gui.map_window as map_window


class JobsListWindow(QWidget):
    def __init__(self, job_data):
        super().__init__()
        self.map_window = None
        self.data_window = None
        self.data = job_data
        self.list_control = None
        self.keyword_filter = QLineEdit(self)
        self.location_filter = QLineEdit(self)
        self.remote_filter = QCheckBox("Remote Jobs", self)
        self.salary_filter = QLineEdit(self)
        self.setup_window()

    def setup_window(self):
        self.setWindowTitle("Job Data for Capstone Project 1")
        layout = QVBoxLayout(self)
        title_label = QLabel("Job List", self)
        layout.addWidget(title_label)

        # Add filter widgets
        layout.addWidget(self.keyword_filter)
        self.keyword_filter.setPlaceholderText("Enter keyword to filter")

        layout.addWidget(self.location_filter)
        self.location_filter.setPlaceholderText("Select or type city to filter")

        layout.addWidget(self.remote_filter)

        layout.addWidget(self.salary_filter)
        self.salary_filter.setPlaceholderText("Enter a minimum salary range to filter")

        display_list = QListWidget(self)
        self.list_control = display_list
        self.put_data_in_list(self.data)
        display_list.resize(400, 350)
        display_list.currentItemChanged.connect(self.list_job_selected)
        layout.addWidget(display_list)

        map_button = QPushButton("Job Map", self)
        map_button.clicked.connect(self.show_map_window)
        layout.addWidget(map_button)

        quit_button = QPushButton("Quit Now", self)
        quit_button.clicked.connect(QApplication.instance().quit)
        layout.addWidget(quit_button)

        apply_filters_button = QPushButton("Apply Filters", self)
        apply_filters_button.clicked.connect(self.filter_jobs)
        layout.addWidget(apply_filters_button)

        self.show()

    def put_data_in_list(self, job_data: list[dict]):
        for job_entry in job_data:
            display_text = f'{job_entry["job_title"]}, {job_entry["company_name"]}'
            list_item = QListWidgetItem(display_text, listview=self.list_control)
            list_item.setData(Qt.UserRole, job_entry["job_id"])  # Set job ID as user data

    def show_map_window(self):
        filtered_data = self.filter_jobs()  # Apply filters to get filtered data
        self.map_window = map_window.JobMapWindow(filtered_data)  # Pass filtered data
        self.map_window.show()

    def find_full_job_record(self, job_id):
        for job_record in self.data:
            if job_record["job_id"] == job_id:
                return job_record

    def list_job_selected(self, current: QListWidgetItem):
        if current is not None:
            job_id = current.data(Qt.UserRole)
            full_record = self.find_full_job_record(job_id)
            print(full_record)
            self.data_window = detail_window.JobDetailWindow(full_record)
            self.data_window.show()

    def filter_jobs(self):
        keyword = self.keyword_filter.text()
        location = self.location_filter.text()
        remote = self.remote_filter.isChecked()
        salary = self.salary_filter.text()

        filtered_jobs = self.data

        if keyword:
            filtered_jobs = self.filter_jobs_by_keyword(filtered_jobs, keyword)
        if location:
            filtered_jobs = self.filter_jobs_by_location(filtered_jobs, location)
        if remote:
            filtered_jobs = self.filter_remote_jobs(filtered_jobs)
        if salary:
            filtered_jobs = self.filter_jobs_by_salary(filtered_jobs, salary)

        self.list_control.clear()
        self.put_data_in_list(filtered_jobs)

        # Close the detail window if it's open
        if self.data_window:
            self.data_window.close()
        return filtered_jobs

    @staticmethod
    def filter_jobs_by_keyword(jobs, keyword):
        filtered_jobs = []
        for job in jobs:
            if (keyword.lower() in job['job_description'].lower() or
                    keyword.lower() in job['job_title'].lower() or
                    any(keyword.lower() in qualification.lower() for qualification in
                        job.get('job_qualifications', []))):
                filtered_jobs.append(job)
        return filtered_jobs

    @staticmethod
    def filter_jobs_by_location(jobs, location):
        filtered_jobs = []
        for job in jobs:
            if location.lower() in job['job_location'].lower():
                filtered_jobs.append(job)
        return filtered_jobs

    @staticmethod
    def filter_remote_jobs(jobs):
        filtered_jobs = []
        for job in jobs:
            if job['job_remote'] == "Yes":
                filtered_jobs.append(job)
        return filtered_jobs

    @staticmethod
    def filter_jobs_by_salary(jobs, min_salary):
        filtered_jobs = []
        for job in jobs:
            if job['salary_min'] >= float(min_salary):
                filtered_jobs.append(job)
        return filtered_jobs
