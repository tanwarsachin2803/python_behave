import json
import logging

class JSONReader:
    def __init__(self, file_path):
        """
        Initializes the JSONReader instance with the path to the JSON file.

        :param file_path: Path to the JSON file
        """
        self.file_path = file_path
        self.data = self.load_json()

    def load_json(self):
        """
        Loads the JSON data from the file path.

        :return: The parsed JSON data
        """
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                logging.info(f"Successfully loaded JSON file from {self.file_path}")
                return data
        except FileNotFoundError:
            logging.error(f"File not found: {self.file_path}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON in file {self.file_path}: {e}")
            raise

    def get_value(self, key):
        """
        Fetches the value associated with the specified key from the loaded JSON data.

        :param key: The key to fetch the value for
        :return: The value associated with the key
        """
        try:
            value = self.data.get(key)
            if value is None:
                logging.warning(f"Key '{key}' not found in the JSON file.")
            return value
        except KeyError:
            logging.error(f"Key '{key}' not found in the JSON data.")
            raise

    def get_nested_value(self, *keys):
        """
        Fetches a nested value from the JSON data based on the provided keys.
        
        Example:
            json_data = { "local": { "platformName": "Android" } }
            json_reader.get_nested_value("local", "platformName")

        :param keys: Keys in the JSON data, provided as a sequence of arguments
        :return: The value corresponding to the nested keys
        """
        value = self.data
        for key in keys:
            value = value.get(key)
            if value is None:
                logging.warning(f"Key '{key}' not found in the nested JSON structure.")
                return None
        return value
