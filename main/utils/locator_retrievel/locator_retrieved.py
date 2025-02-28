import csv
from main.utils.locator_retrievel.locator_utility import LocatorUtil

class LocatorRetrieved:
    def __init__(self, driver, page_name, platform):
        """
        Initializes the LocatorRetrieved object with the page name and platform.
        :param page_name: The name of the page (e.g., 'landing_page')
        :param platform: The platform ('web', 'android', 'ios')
        """
        self.driver = driver
        self.page_name = page_name
        self.platform = platform.lower()  # Convert platform to lowercase for consistency
        self.locators = self.load_locators()

    def load_locators(self):
        """
        Loads locators from a CSV file based on the page_name.
        The CSV file should have the format:
        Locator_Name, Web_Locator, Android_Locator, iOS_Locator
        """
        locators = {}
        correct_page_name = self.page_name.replace('"', '')
        file_path = f"main/locators/{correct_page_name}.csv"  # Dynamic file path

        try:
            with open(file_path, mode='r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip header row
                for row in csv_reader:
                    locator_name = row[0]
                    android_locator = row[1].strip() if len(row) > 1 else None
                    ios_locator = row[2].strip() if len(row) > 2 else None
                    web_locator = row[3].strip() if len(row) > 3 else None

                    # Add locators to the dictionary
                    locators[locator_name] = {
                        "website": web_locator,
                        "android": android_locator,
                        "ios": ios_locator
                    }

        except FileNotFoundError:
            raise FileNotFoundError(f"Locator file '{file_path}' not found!")

        return locators

    def get_element(self, locator_name):
        """
        Returns the element for the specified locator_name based on the platform.
        If locator not found, raises an exception.
        """
        # Fetch the locator info for the given locator_name
        locator_name = locator_name.strip('"')
        locator_info = self.locators.get(locator_name)
        
        if not locator_info:
            raise ValueError(f"Locator '{locator_name}' not found on the {self.page_name} page!")

        # Fetch the correct locator based on the platform
        locator_value = locator_info.get(self.platform)
        
        if not locator_value:
            raise ValueError(f"Locator '{locator_name}' not found for platform '{self.platform}'")

        # Split the locator into type and value (e.g., 'id=APjFqb' becomes 'id' and 'APjFqb')
        locator_type, locator_value = locator_value.split("=", 1)
        print('locator_name',locator_name,'locator_type',locator_type,'locator_value',locator_value)
        # Return the element using LocatorUtil.get_element method
        return LocatorUtil.get_element(self.driver,locator_type, locator_value)
