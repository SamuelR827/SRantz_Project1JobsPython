from PySide6.QtWidgets import QWidget, QPushButton, QListWidget, QApplication, QListWidgetItem, QMessageBox


class JobsListWindow(QWidget):
    def __init__(self, job_data):
        super().__init__()
        self.data = job_data
        self.list_control = None
        self.setup_window()

    def setup_window(self):
        self.setWindowTitle("GUI Demo for Capstone")
        display_list = QListWidget(self)
        self.list_control = display_list
        self.put_data_in_list(self.data)
        display_list.resize(400, 350)
        display_list.currentItemChanged.connect(self.list_job_selected)
        self.setGeometry(300, 100, 400, 500)
        quit_button = QPushButton("Quit Now", self)
        quit_button.clicked.connect(QApplication.instance().quit)
        quit_button.resize(quit_button.sizeHint())
        quit_button.move(300, 400)
        map_button = QPushButton("Job Map", self)
        map_button.move(300, 400)
        map_button.clicked.connect(self.show_map_window)
        self.show()

    def put_data_in_list(self, job_data: list[dict]):
        for job_entry in job_data:
            display_text = f'{job_entry["job_title"]}'
            list_item = QListWidgetItem(display_text, listview=self.list_control)

    # TODO actual implementation of job map window
    def show_map_window(self):
        message_box = QMessageBox(self)
        message_box.setText("You just pushed the button - imagine database work here")
        message_box.setWindowTitle("Map Window")
        message_box.show()

# TODO actual implementation of job list window
    def list_job_selected(self, current: QListWidgetItem, previous: QListWidgetItem):
        message_box = QMessageBox(self)
        message_box.setText("You just selected a job - imagine database work here")
        message_box.setWindowTitle("Detail Window")
        message_box.show()


