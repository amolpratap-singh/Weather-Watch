import logging

from handler.air_quality import AirQualityIndex
from handler.weather_data import WeatherData
from handler.forecast_news import ForeCastNews
from handler.geo_location import GeoLocation

class WeatherEngine(object):
    
    def __init__(self) -> None:
        self.logger = logging.getLogger("WeatherApp")
        self.geo_location = GeoLocation()
        
    def start(self) -> None:
        try:
            self.logger.info("Weather Engine Initiated")
            if self.geo_location.update_geolocation():
                self.launch_threads()
            else:
                self.logger.info("Threads Not launched due to issue \
                                 in update of location in Opensearch")
        except Exception as ex:
            self.logger.error(f"Error occurred during Weather Engine Thread Initiated: {ex}")
            
    def launch_threads(self) -> None:
        self.logger.info("Inititalizing of thread")
        weather_data_thread = WeatherData("WeatherData", 1)
        aqi_thread = AirQualityIndex("AirQualityIndex", 2)
        forecast_news_thread = ForeCastNews("ForeCastNews", 3)
        
        self.logger.info("Starting of Threads")
        aqi_thread.start()
        weather_data_thread.start()
        forecast_news_thread.start()
        
        self.logger.info("Threads allocated to Main")
        aqi_thread.join()
        weather_data_thread.join()
        forecast_news_thread.join()
        
        self.logger.info("Main thread Process Completed")
        
        
        
        
        
        
        
        
        
    