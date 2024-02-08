import os
import json
import logging

from handler import constant

current_dir = os.path.dirname(os.path.abspath(__file__))
relative_path = os.path.join(current_dir, "..", "resources", "test-pincodes.json")
absolute_path = os.path.abspath(relative_path)



class GeoLocation(object):
    
    def __init__(self):
        self.logger = logging.getLogger("WeatherApp")
        self.file_path = absolute_path
    
    def read_input_file(self):
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            self.logger.error(f"File is not present at {self.file_path}")
            return None
        except json.JSONDecodeError:
            self.logger.error(f"Error caused during decoding json {self.file_path} file")
    
    def update_geolocation(self):
        
        json_data = self.read_input_file()
        if json_data:
            #self.logger.info(f"Geo Location information from input file: {json_data}")
            
            for data in json_data:
                location_info = dict()
                location_info[constant.PINCODE] = data.get(constant.PINCODE)
                location_info[constant.TALUKA] = data.get("taluk")
                location_info[constant.DISTRICT] = data.get("districtName")
                location_info[constant.STATE] = data.get("stateName")
                location_info[constant.COUNTRY] = "India"
                location_info[constant.POST_OFFICE] = data.get("officeName")
                print(location_info)
             
            # create the body 
            # update the db
            
            return True
        
        
        return False
        