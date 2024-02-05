import logging

from handler.air_quality import AirQualityIndex
from handler.weather_data import WeatherData
from handler.forecast_news import ForeCastNews

class WeatherEngine(object):
    
    def __init__(self) -> None:
        self.logger = logging.getLogger("WeatherApp")
        
    def start(self) -> None:
        try:
            self.logger.info("Weather Engine Initiated")
            self.launch_threads()
        except Exception as ex:
            self.logger.error(f"Error occurred during Weather Engine Thread Initiated: {ex}")
            
    def launch_threads(self) -> None:
        self.logger.info("Inititalizing of thread")
        aqi_thread = AirQualityIndex("AirQualityIndex", 1)
        weather_data_thread = WeatherData("WeatherData", 2)
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
        
        
        
        
        
        
        
        
        
    