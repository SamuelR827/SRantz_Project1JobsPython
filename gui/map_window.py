import io
from PySide6.QtWidgets import QWidget, QVBoxLayout
import folium
from PySide6.QtWebEngineWidgets import QWebEngineView
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster


class JobMapWindow(QWidget):
    def __init__(self, job_data):
        super().__init__()
        self.layout = None
        self.webview = None
        self.data = job_data
        self.map = self.build_map()
        self.setup_window()

    def setup_window(self):
        self.layout = QVBoxLayout(self)
        self.webview = QWebEngineView()

        self.webview.setHtml(self.map.getvalue().decode("utf-8"))
        self.layout.addWidget(self.webview)
        self.setLayout(self.layout)
        self.resize(800, 800)
        self.show()

    def build_map(self):
        address = 'Brockton, MA'
        geolocator = Nominatim(user_agent="Rantz_Project1JobsPython")
        base_location = geolocator.geocode(address)
        job_map_menu = folium.Map(
            location=[base_location.latitude, base_location.longitude], zoom_start=13
        )
        in_memory_file = io.BytesIO()
        map_data_markers = MarkerCluster().add_to(job_map_menu)
        for entry in self.data:
            job_name = entry["job_title"]
            company_name = entry["company_name"]
            job_location = entry["job_location"]
            job_loc_geocoded = geolocator.geocode(job_location)  # this might need try/catch for small towns
            folium.Marker(
                location=[job_loc_geocoded.latitude, job_loc_geocoded.longitude],
                popup=f"{job_name}, {company_name} - {job_location}"
            ).add_to(map_data_markers)
        job_map_menu.save(in_memory_file, close_file=False)
        return in_memory_file
