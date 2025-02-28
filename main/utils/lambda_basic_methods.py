import json
import os
from datetime import datetime, timedelta
import logging

class LambdaBasicMethod:
    def __init__(self, is_jenkins=False, platform='', environment=''):
        # Get platform and environment from environment variables, or use provided arguments
        self.platform = os.environ.get("platform", platform).replace('@', '')
        self.environment = os.environ.get("environment", environment)
        self.is_jenkins = is_jenkins  # Flag to check if running in Jenkins or locally
        self.json_file = f"main/utils/device_capabilities/{self.platform}.json"  # Path to the platform-specific JSON file
        self.driver = None  # Add driver attribute
        
        # Only proceed if the environment is 'virtual'
        if self.environment == "virtual":
            self.capabilities = self.load_capabilities()  # Load capabilities from the JSON file
            self.build_name = self.generate_build_name()  # Set the build name
        else:
            logging.warning(f"Running in non-virtual environment ({self.environment}). Skipping setup for virtual environment.")
            self.capabilities = {}  # Empty capabilities if not running in a virtual environment
            self.build_name = None
        
        self.test_status = "pass"  # Default status is pass

    def load_capabilities(self):
        """Load capabilities from the platform-specific JSON file."""
        try:
            with open(self.json_file, 'r') as file:
                capabilities = json.load(file)
                return capabilities
        except Exception as e:
            logging.error(f"Error loading capabilities from {self.json_file}: {e}")
            raise
    
    def get_current_timestamp(self):
        current_time = datetime.now()
        if self.is_jenkins:
            # Adjust for Jenkins environment (e.g., IST)
            current_time += timedelta(hours=5, minutes=30)
        return current_time.strftime("%Y%m%d_%H%M%S")

    def generate_build_name(self):
        timestamp = self.get_current_timestamp()
        return f"Tez_Rummy_{timestamp}"

    def update_test_details(self, scenario_name):
        """Update the build name and test name (scenario name) in the capabilities."""
        if self.environment == "virtual":
            self.capabilities["build"] = self.build_name
            self.capabilities["name"] = scenario_name
            if "lambda:options" in self.capabilities:
                self.capabilities["lambda:options"]["build"] = self.build_name
                self.capabilities["lambda:options"]["name"] = scenario_name

    def mark_test_status(self, status):
        """Mark the test status (pass/fail)."""
        self.test_status = status

    def log_test_results(self):
        """Log the final test results."""
        if self.test_status == "pass":
            logging.info(f"Test passed for scenario: {self.capabilities.get('name', 'Unknown')}")
        elif self.test_status == "fail":
            logging.error(f"Test failed for scenario: {self.capabilities.get('name', 'Unknown')}")
        else:
            logging.warning(f"Test skipped for scenario: {self.capabilities.get('name', 'Unknown')}")

    def set_driver(self, driver):
        """Set the WebDriver instance"""
        self.driver = driver
        logging.info("WebDriver instance set in LambdaBasicMethod")

    def set_test_name(self, scenario_name):
        """Set the test name in LambdaTest dashboard"""
        if self.environment == "virtual" and self.driver:
            try:
                # Update capabilities
                self.update_test_details(scenario_name)
                
                # Update test name in LambdaTest
                script = f'lambda-name={scenario_name}'
                self.driver.execute_script(script)
                logging.info(f"Test name set to: {scenario_name}")
            except Exception as e:
                logging.error(f"Failed to set test name in LambdaTest: {e}")

    def update_test_status(self, status):
        """Update test status in LambdaTest dashboard"""
        if self.environment == "virtual" and self.driver:
            try:
                # Validate status
                status = status.lower()
                if status not in ['passed', 'failed', 'skipped']:
                    raise ValueError("Status must be 'passed', 'failed', or 'skipped'")

                # Update status in LambdaTest
                script = f'lambda-status={status}'
                self.driver.execute_script(script)
                
                # Update local status
                self.test_status = "pass" if status == "passed" else "fail"
                
                logging.info(f"Test status updated to: {status}")
                self.log_test_results()
            except Exception as e:
                logging.error(f"Failed to update test status in LambdaTest: {e}")

    def run(self, scenario_name):
        """Run the test for the given scenario."""
        try:
            if self.environment == "virtual":
                self.set_test_name(scenario_name)
                logging.info(f"Running test for scenario: {self.capabilities['name']}")
                self.mark_test_status("pass")
            else:
                logging.info(f"Skipping test execution for scenario: {scenario_name} (Non-virtual environment)")

        except Exception as e:
            logging.error(f"Test failed due to error: {e}")
            self.mark_test_status("fail")
        finally:
            self.log_test_results()
