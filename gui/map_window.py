import io

import folium
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget, QVBoxLayout
from folium.plugins import MarkerCluster
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim


class JobMapWindow(QWidget):
    def __init__(self, filtered_data):
        super().__init__()
        self.layout = None
        self.webview = None
        self.filtered_data = filtered_data  # Store filtered data
        self.geocode_cache = {}
        self.setup_window()

    def setup_window(self):
        self.layout = QVBoxLayout(self)
        self.webview = QWebEngineView()

        self.layout.addWidget(self.webview)
        self.setLayout(self.layout)
        self.resize(800, 800)
        self.show()
        self.update_map()

    def update_map(self):
        address = 'Brockton, MA'
        geolocator = Nominatim(user_agent="Rantz_Project1JobsPython")
        base_location = geolocator.geocode(address)

        # Convert dictionaries to tuples in filtered_data
        filtered_data_tuples = (entry.items() for entry in self.filtered_data)

        # Check if the map data is already cached
        if filtered_data_tuples in self.geocode_cache:
            print("Cache hit")
            map_data = self.geocode_cache[filtered_data_tuples]
        else:
            print("Cache miss")
            job_map_menu = folium.Map(
                location=[base_location.latitude, base_location.longitude], zoom_start=13
            )
            in_memory_file = io.BytesIO()
            map_data_markers = MarkerCluster().add_to(job_map_menu)
            for entry in self.filtered_data:
                job_name = entry["job_title"]
                company_name = entry["company_name"]
                job_location = entry["job_location"]

                try:
                    job_loc_geocoded = geolocator.geocode(job_location, timeout=10)  # Geocode the location with timeout
                    if job_loc_geocoded:
                        latitude, longitude = job_loc_geocoded.latitude, job_loc_geocoded.longitude
                        folium.Marker(
                            location=[latitude, longitude],
                            popup=f"{job_name}, {company_name} - {job_location}"
                        ).add_to(map_data_markers)
                except GeocoderTimedOut:
                    print(f"Timeout error processing location '{job_location}'. Skipping.")
                except Exception as e:
                    print(f"Error processing location '{job_location}': {e}")

            job_map_menu.save(in_memory_file, close_file=False)
            map_data = in_memory_file.getvalue().decode("utf-8")

            # Cache the map data using the tuple as the key
            self.geocode_cache[filtered_data_tuples] = map_data
            print("Cache updated")

        # Display the cached map data
        self.webview.setHtml(map_data)

    def filter_data(self, filtered_data):
        self.filtered_data = filtered_data
        self.update_map()  # Update the map with filtered data
