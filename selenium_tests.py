from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class SimpleTest(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(r'C:\Users\jeanm\Desktop\Bureau\OC\8_Plateform_Nutella\Pur_Beurre\chromedriver')
        self.driver.get('http://127.0.0.1:8000/')
        self.original_window = self.driver.current_window_handle

    def test_simple(self):
        assert len(self.driver.window_handles) == 1
        assert "Pur Beurre" in self.driver.title

    def test_input_fields_good_request(self):
        elem = self.driver.find_element_by_name("product")
        elem.send_keys("chocolat")
        elem.send_keys(Keys.RETURN)
        assert "Nous n'avons pas compris votre demande" not in self.driver.page_source

    def test_input_fields_bad_request(self):
        elem = self.driver.find_element_by_name("product")
        elem.send_keys("dgsgdvst")
        elem.send_keys(Keys.RETURN)
        assert "Nous n'avons trouvé aucun produit de substitution" in self.driver.page_source

    def test_input_fields_no_request(self):
        elem = self.driver.find_element_by_name("product")
        elem.send_keys("")
        elem.send_keys(Keys.RETURN)
        assert "Nous n'avons pas compris votre demande" in self.driver.page_source

    def test_legals_page(self):
        link = self.driver.find_element_by_id('legals')
        link.click()
        page_title =self.driver.find_element_by_tag_name('h1').text
        self.assertEqual(page_title, "MENTIONS LÉGALES")

    def tearDown(self):
        self.driver.quit()
