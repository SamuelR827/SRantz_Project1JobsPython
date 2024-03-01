from PySide6.QtWidgets import QWidget, QLabel, QLineEdit


class JobDetailWindow(QWidget):
    def __init__(self, job_data):
        super().__init__()
        self.data = job_data
        self.setup_window()

    def setup_window(self):
        self.setWindowTitle('Selected Job Detail Window')
        self.setGeometry(500, 100, 1000, 500)

        self.create_field("Job ID: ", self.data['job_id'], 50)
        self.create_field("Job Title: ", self.data['job_title'], 75)
        self.create_field("Company Name: ", self.data['company_name'], 100)
        self.create_field("Job Location: ", self.data['job_location'], 125)
        self.create_field("Job Remote: ", self.data['job_remote'], 150)
        self.create_field("Job Posted Date: ", self.data['job_posted'], 175)
        self.create_field("Salary Min: ", str(self.data['salary_min']), 200)
        self.create_field("Salary Max: ", str(self.data['salary_max']), 225)
        self.create_field("Salary Rate: ", self.data['salary_rate'], 250)
        y_position = 275
        y_position = self.create_field_links(y_position)
        y_position = self.create_field_qualifications(y_position)

    def create_field(self, label_text, data, y_pos):
        label = QLabel(self)
        label.setText(label_text)
        label.move(50, y_pos)

        line_edit = QLineEdit(str(data), self)
        line_edit.move(200, y_pos)
        line_edit.setReadOnly(True)  # Make the field read-only
        line_edit.setFixedWidth(300)  # Set the width of the field

    def create_field_links(self, y_pos):
        job_links = self.data['job_links']
        if job_links != 'N/A':
            link_count = 1
            for link in job_links:
                self.create_field(f"Job Link {link_count}: ", self.data['job_links'][link_count - 1], y_pos)
                link_count += 1
                y_pos += 25
            return y_pos

    def create_field_qualifications(self, y_pos):
        job_qualifications = self.data['job_qualifications']
        print(job_qualifications)
        if job_qualifications != 'N/A':
            qualification_count = 1
            for qualification in job_qualifications:
                self.create_field(f"Job Qualification {qualification_count}: ",
                                  self.data['job_qualifications'][qualification_count - 1], y_pos)
                qualification_count += 1
                y_pos += 25
            return y_pos
