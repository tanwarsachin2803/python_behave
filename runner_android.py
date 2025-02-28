import os
from subprocess import run

def run_tests(tag):
    # Set the environment variable to pass the tag to the Behave environment
    os.environ["platform"] = "@android"  # This will set the platform as Android
    os.environ["environment"] = "virtual"  # This can be adjusted based on your environment needs
    feature_file = "features/feature_files/testing_app.feature"

    # Update the command to specify the tag that filters Android-related tests
    command = f"behave --tags={tag} {feature_file}"
    print(f"Running tests for tag: {tag}")
    
    # Run the command
    run(command, shell=True)

if __name__ == "__main__":
    # Run tests for @android tag
    run_tests("@android")