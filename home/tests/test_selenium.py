from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import FirefoxOptions

from home.models import Category, Aliment

class SeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        cls.selenium = WebDriver(firefox_options=opts)
        cls.selenium.implicitly_wait(10)

        cls.cat_test = Category.objects.create(name='cat_test')
        cls.cat_test.save()
        cls.original_test = Aliment.objects.create(
            name="original test au jambon",
            nutriscore='f',
            ingredients='ingredients test',
            cat_name=cls.cat_test,
            link="https://fr.openfoodfacts.org/",
            image="https://static.openfoodfacts.org/images/products/544/900/000/0996/front_fr.547.400.jpg")
        cls.original_test.save()
        cls.substitut_test = Aliment.objects.create(
            name="substitut test",
            nutriscore='a',
            ingredients='ingredients test',
            cat_name=cls.cat_test,
            link="https://fr.openfoodfacts.org/",
            image="https://static.openfoodfacts.org/images/products/544/900/000/0996/front_fr.547.400.jpg")
        cls.substitut_test.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_selenium(self):
        # Go to home page
        self.selenium.get(f'{self.live_server_url}')
        # Click on login button
        self.selenium.find_element_by_id('login').click()
        # Click on register button
        self.selenium.find_element_by_id('inscription').click()

        # Fill register form and register
        username = self.selenium.find_element_by_name('username')
        username.clear()
        username.send_keys('user_test')

        email = self.selenium.find_element_by_name('email')
        email.clear()
        email.send_keys('email_test@email.fr')

        password = self.selenium.find_element_by_name('password')
        password.clear()
        password.send_keys('password_test')

        self.selenium.find_element_by_id('submit').click()
        # Verify that account page is shown and logout
        print(self.selenium.current_url)
        assert 'account' in self.selenium.current_url
        self.selenium.find_element_by_id('login').click()

        # Login again
        self.selenium.find_element_by_id('login').click()

        username = self.selenium.find_element_by_name('username')
        username.clear()
        username.send_keys('user_test')

        password = self.selenium.find_element_by_name('password')
        password.clear()
        password.send_keys('password_test')

        self.selenium.find_element_by_id('submit').click()

        # Go make a new search
        self.selenium.get(f'{self.live_server_url}')
        search = self.selenium.find_element_by_id('search')
        search.clear()
        search.send_keys('original test')
        self.selenium.find_element_by_id('submit').click()

        # Register a product
        self.selenium.find_element_by_class_name('select-submit').click()
        # Verify that the product registered is on the favorite view
        self.selenium.get(f'{self.live_server_url}/favorites')
        substitute = self.selenium.find_element_by_class_name('card-img-top')
        assert substitute.get_attribute('alt') == str(self.substitut_test.name)
