import os
import time
from datetime import date
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from testapp.models import Book


@override_settings(DEBUG=True)
class AdminAutocompleteE2ETest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Initialize the Chrome WebDriver
        cls.selenium = webdriver.Chrome(options=chrome_options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        # Create superuser
        User = get_user_model()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )

        # Create test books
        self.books = []
        test_data = [
            {
                "title": "The Great Adventure",
                "author": "John Smith",
                "published_date": date(2020, 1, 1),
                "isbn": "1234567890123"
            },
            {
                "title": "Mystery of the Lost Key",
                "author": "Jane Doe",
                "published_date": date(2021, 2, 15),
                "isbn": "2345678901234"
            },
            {
                "title": "Python Programming 101",
                "author": "David Wilson",
                "published_date": date(2022, 3, 20),
                "isbn": "3456789012345"
            },
            {
                "title": "Django for Beginners",
                "author": "Sarah Johnson",
                "published_date": date(2023, 4, 10),
                "isbn": "4567890123456"
            },
            {
                "title": "The Art of Testing",
                "author": "Michael Brown",
                "published_date": date(2023, 5, 5),
                "isbn": "5678901234567"
            }
        ]

        for book_data in test_data:
            self.books.append(Book.objects.create(**book_data))

    def test_admin_autocomplete(self):
        """Test the autocomplete functionality in the admin interface."""
        # Log in to admin
        self.selenium.get(f'{self.live_server_url}/admin/')
        username_input = self.selenium.find_element(By.NAME, 'username')
        password_input = self.selenium.find_element(By.NAME, 'password')
        username_input.send_keys('admin')
        password_input.send_keys('adminpass123')
        password_input.send_keys(Keys.RETURN)

        # Navigate to the Book changelist
        self.selenium.get(f'{self.live_server_url}/admin/testapp/book/')

        # Wait for the search bar to be present
        search_input = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "searchbar"))
        )

        # Test searching for "Python"
        search_input.send_keys("Python")
        
        # Wait for autocomplete results
        results_container = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "admin-autocomplete-results"))
        )

        # Wait for results to be visible
        time.sleep(1)  # Small delay to ensure results are populated

        # Check if results are displayed
        result_items = results_container.find_elements(By.CLASS_NAME, "autocomplete-item")
        self.assertTrue(len(result_items) > 0, "No autocomplete results found")

        # Verify the correct book is in results
        python_book_found = False
        for item in result_items:
            if "Python Programming 101" in item.text:
                python_book_found = True
                break
        self.assertTrue(python_book_found, "Python Programming book not found in results")

        # Test clicking a result
        for item in result_items:
            if "Python Programming 101" in item.text:
                item.click()
                break

        # Wait for the change form page to load
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "book_form"))
        )

        # Verify we're on the correct page
        self.assertTrue("/admin/testapp/book/" in self.selenium.current_url)

    def test_keyboard_navigation(self):
        """Test keyboard navigation in autocomplete results."""
        # Log in to admin
        self.selenium.get(f'{self.live_server_url}/admin/')
        username_input = self.selenium.find_element(By.NAME, 'username')
        password_input = self.selenium.find_element(By.NAME, 'password')
        username_input.send_keys('admin')
        password_input.send_keys('adminpass123')
        password_input.send_keys(Keys.RETURN)

        # Navigate to the Book changelist
        self.selenium.get(f'{self.live_server_url}/admin/testapp/book/')

        # Wait for the search bar
        search_input = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "searchbar"))
        )

        # Test searching for "the"
        search_input.send_keys("the")
        
        # Wait for autocomplete results
        results_container = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "admin-autocomplete-results"))
        )

        # Wait for results to be visible
        time.sleep(1)

        # Use keyboard to navigate
        search_input.send_keys(Keys.DOWN)  # First item
        search_input.send_keys(Keys.DOWN)  # Second item
        search_input.send_keys(Keys.UP)    # Back to first item
        search_input.send_keys(Keys.RETURN) # Select item

        # Wait for the change form page to load
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "book_form"))
        )

        # Verify we're on a book change page
        self.assertTrue("/admin/testapp/book/" in self.selenium.current_url)

    def test_minimum_chars_requirement(self):
        """Test that autocomplete only shows after minimum characters."""
        # Log in to admin
        self.selenium.get(f'{self.live_server_url}/admin/')
        username_input = self.selenium.find_element(By.NAME, 'username')
        password_input = self.selenium.find_element(By.NAME, 'password')
        username_input.send_keys('admin')
        password_input.send_keys('adminpass123')
        password_input.send_keys(Keys.RETURN)

        # Navigate to the Book changelist
        self.selenium.get(f'{self.live_server_url}/admin/testapp/book/')

        # Wait for the search bar
        search_input = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "searchbar"))
        )

        # Type single character
        search_input.send_keys("a")
        time.sleep(1)

        # Check that no results are shown
        results = self.selenium.find_elements(By.CLASS_NAME, "autocomplete-item")
        self.assertEqual(len(results), 0, "Results shown with insufficient characters")

        # Type second character
        search_input.send_keys("r")
        time.sleep(1)

        # Check that results are now shown
        results = self.selenium.find_elements(By.CLASS_NAME, "autocomplete-item")
        self.assertTrue(len(results) > 0, "No results shown with sufficient characters")
