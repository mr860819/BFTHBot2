import json
def load_car_keys():
            """
            Load the car keys from the JSON file.

            Returns:
            - dict: A dictionary containing the car keys.
            """
            with open('car_keys.json', 'r') as file:
                car_keys = json.load(file)
                print(str(car_keys))
            return car_keys