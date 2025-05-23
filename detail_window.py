""" This module handles the creation and handling of the job detail window that opens for each job. """
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QScrollArea, QVBoxLayout


class JobDetailWindow(QWidget):
    def __init__(self, job_data):
        super().__init__()
        self.description_field = None
        self.data = job_data
        self.setup_window()

    def setup_window(self):
        """ Create the job list window"""
        self.setWindowTitle(f"{self.data['job_title']} Detail Window")

        # Create scroll area for job fields
        scroll_area = QScrollArea(self)
        scroll_area.setGeometry(50, 50, 500, 300)
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)

        # Create layout for job fields
        field_layout = QVBoxLayout(scroll_content)

        # Display job fields
        self.create_field("Job ID: ", self.data['job_id'], field_layout)
        self.create_field("Job Title: ", self.data['job_title'], field_layout)
        self.create_field("Company Name: ", self.data['company_name'], field_layout)
        self.create_field("Job Location: ", self.data['job_location'].strip(), field_layout)
        self.create_field("Job Remote: ", self.data['job_remote'], field_layout)
        self.create_field("Job Posted Date: ", self.data['job_posted'], field_layout)
        self.create_field("Salary Min: ", str(self.data['salary_min']), field_layout)
        self.create_field("Salary Max: ", str(self.data['salary_max']), field_layout)
        self.create_field("Salary Rate: ", self.data['salary_rate'], field_layout)
        self.create_field_links(field_layout)
        self.create_field_qualifications(field_layout)

        # Create scroll area for job description
        if self.data['job_description'] != 'N/A':
            description_label = QLabel("Job Description:", self)
            description_label.setAlignment(Qt.AlignTop)
            field_layout.addWidget(description_label)

            self.description_field = QTextEdit(self.data['job_description'], self)
            self.description_field.setReadOnly(True)
            field_layout.addWidget(self.description_field)

    def create_field(self, label_text, data, layout):
        """This function creates a field based on parameters for easier modularity and readability"""
        label = QLabel(label_text, self)
        layout.addWidget(label)

        line_edit = QLineEdit(str(data), self)
        line_edit.setReadOnly(True)
        layout.addWidget(line_edit)

    def create_field_links(self, layout):
        """ This function handles the creation of the links for the jobs that have links."""
        job_links = self.data['job_links']
        # don't create the field if the job has no links for simple gui
        if job_links != 'N/A':
            if job_links != 'No Related Links Specified':
                # get link count to print each link with a number
                link_count = 1
                # create a field for each link
                for _ in job_links:
                    self.create_field(f"Job Link {link_count}: ", self.data['job_links'][link_count - 1], layout)
                    link_count += 1

    def create_field_qualifications(self, layout):
        """ This function handles the creation of the qualifications for the jobs that have qualifications."""
        job_qualifications = self.data['job_qualifications']
        # don't create the field if the job has no qualifications for simple gui
        if isinstance(job_qualifications, list) and 'No Qualifications Specified' not in job_qualifications:
            # get qualification count to print each link with a number
            qualification_count = 1
            # create a field for each qualification
            for qualification in job_qualifications:
                self.create_field(f"Job Qualification {qualification_count}: ", qualification, layout)
                qualification_count += 1
