import json
import folium
from folium import plugins
import os
from typing import List, Tuple

class MapDrawer:
    def __init__(self):
        self.coordinates = []
        self.map = None
        
    """def load_coordinates(self, filepath: str) -> List[Tuple[float, float]]:
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)["GPSData"]
            cords = []
            for key in data:
                value = data[key]
                lat = value["lat"]
                lon = value["lon"]
                cords.append((lat, lon))
            return cords
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")
            return []   
            
            #desktop
    
    """
    def load_coordinates(self, GPSdata) -> List[Tuple[float, float]]:
        data = GPSdata["GPSData"]
        cords = []
        for key in data:
            value = data[key]
            lat = value["lat"]
            lon = value["lon"]
            cords.append((lat, lon))
        return cords
    
    def calculate_map_center(self, coordinates: List[Tuple[float, float]]) -> Tuple[float, float]:
        if not coordinates:
            return (55.7558, 37.6173)
        avg_lat = sum(coord[0] for coord in coordinates) / len(coordinates)
        avg_lon = sum(coord[1] for coord in coordinates) / len(coordinates)
        return (avg_lat, avg_lon)
    
    def create_map(self, coordinates: List[Tuple[float, float]], output_file: str = "real_route_map.html"):
        if len(coordinates) < 2:
            print("Недостаточно точек для построения маршрута")
            return
        center = self.calculate_map_center(coordinates)
        self.map = folium.Map(location = center, zoom_start = 12, tiles = 'OpenStreetMap', control_scale = True)
        folium.TileLayer('Stamen Terrain', attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.').add_to(self.map)
        folium.TileLayer('CartoDB positron',attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>').add_to(self.map)
        folium.PolyLine(coordinates, weight = 6, color = '#3388ff', opacity = 0.8, popup="Маршрут по точкам").add_to(self.map)
        
        for i, (lat, lon) in enumerate(coordinates):
            if i == 0:
                icon_html = '''
                <div style="font-size: 12px; background-color: green; color: white; 
                           border-radius: 50%; width: 20px; height: 20px; 
                           text-align: center; line-height: 20px;">
                    ▶
                </div>
                '''
                icon = folium.DivIcon(html=icon_html, icon_size=(20, 20), icon_anchor=(10, 10))
                folium.Marker(location=[lat, lon], icon=icon).add_to(self.map)
            elif i == len(coordinates) - 1:
                icon_html = '''
                <div style="font-size: 12px; background-color: red; color: white; 
                           border-radius: 50%; width: 20px; height: 20px; 
                           text-align: center; line-height: 20px;">
                    ■
                </div>
                '''
                icon = folium.DivIcon(html=icon_html, icon_size=(20, 20), icon_anchor=(10, 10))
                folium.Marker(location=[lat, lon], icon=icon).add_to(self.map)
        plugins.MeasureControl(position='topright', primary_length_unit='kilometers').add_to(self.map)
        plugins.MiniMap().add_to(self.map)
        folium.LayerControl().add_to(self.map)
        self.map.save(output_file)
        print(f"Карта с маршрутом сохранена в {output_file}")

    def plot_route(self, filepath: str, output_file: str):
        cords = self.load_coordinates(filepath)
        if not cords:
            print("Произошло нагумление")
            return
        self.create_map(cords, output_file)

###########################################################################3
"""
def main():
    kartograf = MapDrawer()
    json_file = input("путь к JSON-файлу: ").strip()
    if not json_file:
        json_file = 'sample_coordinates.json'        
    output_file = input("имя выходного файла: ").strip()
    if not output_file:
        output_file = 'route_map.html'
    kartograf.plot_route(json_file, output_file)

main()"""