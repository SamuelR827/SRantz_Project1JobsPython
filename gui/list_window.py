from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QPushButton, QListWidget, QApplication, QListWidgetItem, QMessageBox, QLabel,
                               QVBoxLayout)

import gui.detail_window as detail_window
import gui.map_window as map_window


class JobsListWindow(QWidget):
    def __init__(self, job_data):
        super().__init__()
        self.data_window = None
        self.data = job_data
        self.list_control = None
        self.setup_window()

    def setup_window(self):
        self.setWindowTitle("GUI Demo for Capstone")
        layout = QVBoxLayout(self)
        title_label = QLabel("Job List", self)
        layout.addWidget(title_label)
        display_list = QListWidget(self)
        self.list_control = display_list
        self.put_data_in_list(self.data)
        display_list.resize(400, 350)
        display_list.currentItemChanged.connect(self.list_job_selected)
        layout.addWidget(display_list)
        self.setGeometry(200, 100, 300, 500)
        map_button = QPushButton("Job Map", self)
        map_button.move(300, 400)
        map_button.clicked.connect(self.show_map_window)
        layout.addWidget(map_button)
        quit_button = QPushButton("Quit Now", self)
        quit_button.clicked.connect(QApplication.instance().quit)
        quit_button.resize(quit_button.sizeHint())
        layout.addWidget(quit_button)
        self.show()

    def put_data_in_list(self, job_data: list[dict]):
        for job_entry in job_data:
            display_text = f'{job_entry["job_title"]}, {job_entry["company_name"]}'
            list_item = QListWidgetItem(display_text, listview=self.list_control)
            list_item.setData(Qt.UserRole, job_entry["job_id"])  # Set job ID as user data

    # TODO actual implementation of job map window
    def show_map_window(self):
        self.map_window = map_window.JobMapWindow(self.data)
        self.map_window.show()

    def find_full_job_record(self, job_id):
        for job_record in self.data:
            if job_record["job_id"] == job_id:
                return job_record

    def list_job_selected(self, current: QListWidgetItem, previous: QListWidgetItem):
        job_id = current.data(Qt.UserRole)
        full_record = self.find_full_job_record(job_id)
        print(full_record)
        self.data_window = detail_window.JobDetailWindow(full_record)
        self.data_window.show()
