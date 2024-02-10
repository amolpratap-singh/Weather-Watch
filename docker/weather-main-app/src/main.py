import os
import logging

from weatherapp.handler.weather_engine import WeatherEngine

# Logging Configuration
log_level = os.getenv("LOG_LEVEL", "INFO")
logger = logging.getLogger("WeatherApp")
format = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(module)s %(funcName)s %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(format)
logger.addHandler(handler)
logger.setLevel(log_level)
logger.propagate = False


process_interval = os.getenv("PROCESS_INTRVAL", 30)

weather_engine = WeatherEngine()

if __name__ == "__main__":
    logger.info("Start of Weather Main App")
    weather_engine.start()
    logger.info("Execution of Main Thread Completed")
    