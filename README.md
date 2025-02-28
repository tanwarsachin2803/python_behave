# 🐍 Python Behave Automation Framework

A powerful, scalable BDD automation testing framework built with Python and Behave, designed for cross-platform testing across Web, Android, and iOS, with LambdaTest integration for cloud testing.

## ✨ Key Features
- 🌐 Cross-platform testing support (Web, Android, iOS)
- ☁️ Cloud testing with LambdaTest integration
- 📱 Mobile-first approach with Appium integration
- 🧩 Modular and maintainable architecture using Page Object Model
- 📊 Comprehensive reporting with Allure
- 🔄 Reusable step definitions
- 🎯 Tag-based test execution
- 📝 Detailed logging capabilities

## 🚀 Getting Started

### Prerequisites

1. 📥 Install Python3
   ```bash
   # For Ubuntu/Debian
   sudo apt-get install python3
   
   # For MacOS
   brew install python3
   ```

2. 🔮 Create & Activate Virtual Environment
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment     
   source venv/bin/activate  # For Unix/MacOS
   .\venv\Scripts\activate   # For Windows
   ```

3. 📦 Install Dependencies
   ```bash
   pip3 install -r requirements.txt
   ```

### 🏃‍♂️ Running Tests

Choose your preferred execution method:

1. 🎯 Using Behave CLI
   ```bash
   behave                           # Run all features
   behave features/login.feature    # Run specific feature
   behave -t @smoke                 # Run tests with specific tags
   ```

2. 🔄 Using Python Runner
   ```bash
   python3 -m behave features/login.feature
   ```

3. 🌐 Platform-Specific Runners
   ```bash
   python3 runner_android.py    # For Android tests
   python3 runner_ios.py        # For iOS tests
   python3 runner_web.py        # For Web tests
   ```

4. ☁️ Running Tests on LambdaTest
   ```bash
   # Set LambdaTest credentials
   export LT_USERNAME="your_username"
   export LT_ACCESS_KEY="your_access_key"
   
   # Run tests on LambdaTest
   python3 runner_lambdatest.py
   ```

## 📝 How to Add New Test Cases

### 1. 🎯 Locator Management
- Store locators in CSV files under `locators/` directory
- Create separate CSV files for each feature/page
- CSV Format: `locator,android_locator,ios_locator,web_locator`
- Locator Types:
  ```
  xpath   → "xpath= your_xpath"
  id      → "id= your_id"
  class   → "class= your_class"
  text    → "text= your_text"
  index   → "index= your_index"
  ```

### 2. 🔄 Step Definitions
- Utilize `common_steps.py` for reusable actions:
  - Element interactions (clicks, inputs)
  - Verification steps
  - Navigation actions
- Create feature-specific step files for unique scenarios

### 3. 📱 Page Objects
- Implement page classes in `pages/` directory
- Each page = One class with related methods
- Follow Page Object Model (POM) for:
  - Better maintenance
  - Reduced code duplication
  - Enhanced readability

### 4. 📋 Feature Files
- Store `.feature` files in `features/` directory
- Write scenarios in Gherkin syntax:
  ```gherkin
  Feature: Login Functionality
    
    Scenario: Successful Login
      Given the user clicks on "locator" on "page_name_of_csv_file"
  ```
- Organize tests with tags (@smoke, @regression, @critical)

### 5. 🎣 Environment Hooks (environment.py)
- Behave hooks for test lifecycle management:
  ```python
  def before_all(context):
      # Setup logging, configurations
      context.config.setup_logging()
      
  def before_feature(context, feature):
      # Feature level setup
      
  def before_scenario(context, scenario):
      # Initialize drivers, setup test data
      
  def after_scenario(context, scenario):
      # Cleanup, close drivers
      
  def after_feature(context, feature):
      # Feature level cleanup
      
  def after_all(context):
      # Final cleanup, generate reports
  ```

### 6. 📊 Reporting
- Allure Reporting Integration:
  ```bash
  # Install Allure
  pip install allure-behave
  
  # Run tests with Allure
  behave -f allure_behave.formatter:AllureFormatter -o allure-results ./features
  
  # Generate HTML report
  allure serve allure-results
  ```

### 7. 📝 Logging
- Comprehensive logging setup:
  ```python
  # In utils/logger.py
  import logging
  
  def setup_logging():
      logging.basicConfig(
          level=logging.INFO,
          format='%(asctime)s - %(levelname)s - %(message)s',
          handlers=[
              logging.FileHandler('test_execution.log'),
              logging.StreamHandler()
          ]
      )
  ```

## 📂 Project Structure
