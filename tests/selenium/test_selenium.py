import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class BasicFlaskAppTests(unittest.TestCase):
    def setUp(self):
        """
        Set up the Chrome WebDriver with options to run in headless mode and
        disable unnecessary features for faster execution.
        """
        options = Options()
        options.headless = True  # Run in headless mode (no UI)
        options.add_argument("--disable-gpu")  # Disable GPU acceleration
        options.add_argument("--disable-extensions")  # Disable extensions
        options.add_argument("--no-sandbox")  # Bypass OS security model
        options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        options.add_argument("--disable-infobars")  # Disable infobars
        options.add_argument("--disable-browser-side-navigation")  # Disable browser side navigation
        options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation controlled info bar
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("http://127.0.0.1:5000/")  # Open the web application

    def tearDown(self):
        """
        Quit the WebDriver session to clean up after each test.
        """
        self.driver.quit()

    def test_homepage_loads(self):
        """
        Test if the homepage loads by checking the title of the page.
        """
        driver = self.driver
        # Check if the title of the homepage contains the expected text
        self.assertIn("Welcome to CSSE DevConnect", driver.title)

    def test_sign_up_link_present(self):
        """
        Test if the 'Sign Up' link is present on the homepage.
        """
        driver = self.driver
        # Find the 'Sign Up' link element by link text and check if it's displayed
        sign_up_link = driver.find_element(By.LINK_TEXT, "Sign Up")
        self.assertTrue(sign_up_link.is_displayed())

    def test_login_link_present(self):
        """
        Test if the 'Login' link is present on the homepage.
        """
        driver = self.driver
        # Find the 'Login' link element by link text and check if it's displayed
        login_link = driver.find_element(By.LINK_TEXT, "Login")
        self.assertTrue(login_link.is_displayed())

    def test_registration_form_elements(self):
        """
        Test if all the registration form elements are present and displayed correctly.
        """
        driver = self.driver
        # Click the 'Sign Up' link to open the registration form
        driver.find_element(By.LINK_TEXT, "Sign Up").click()
        # Wait until the registration form is present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "register")))

        # Find each form field by CSS selector and check if it's displayed
        first_name_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter First Name"]')
        last_name_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter Last Name"]')
        uwa_id_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter UWA ID"]')
        email_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter Email"]')
        major_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter Major"]')
        password_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter Password"]')
        confirm_password_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Confirm Password"]')
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

        # Assert that each field is displayed
        self.assertTrue(first_name_field.is_displayed())
        self.assertTrue(last_name_field.is_displayed())
        self.assertTrue(uwa_id_field.is_displayed())
        self.assertTrue(email_field.is_displayed())
        self.assertTrue(major_field.is_displayed())
        self.assertTrue(password_field.is_displayed())
        self.assertTrue(confirm_password_field.is_displayed())
        self.assertTrue(submit_button.is_displayed())

if __name__ == "__main__":
    unittest.main()
