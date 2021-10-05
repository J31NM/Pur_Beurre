from django.test import LiveServerTestCase
from selenium import webdriver
import time


class SimpleTest(LiveServerTestCase):

    def test_simple(self):
        driver = webdriver.Chrome(r'C:\Users\jeanm\Desktop\Bureau\OC\8_Plateform_Nutella\Pur_Beurre\chromedriver')
        driver.get('http://127.0.0.1:8000/')

        # time.sleep(5)

        assert "Pur Beurre" in driver.title

