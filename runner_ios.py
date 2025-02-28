# runner.py
import os
from subprocess import run

platform_runner = '@ios'

def run_tests(tag):
    # Set the environment variable to pass the tag to the Behave environment
    os.environ["platform"] = platform_runner

    command = f"behave --tags={tag}"
    print(f"Running tests for tag: {tag}")
    run(command, shell=True)

if __name__ == "__main__":
    #Run tests for Website
     run_tests(platform_runner)
