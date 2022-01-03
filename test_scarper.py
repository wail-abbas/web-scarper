import os
import unittest
from web_scarper import web_scraper, save_to_json

html_path = 'input/Kempinski Hotel Bristol Berlin, Germany - Booking.com.html'

class TestMethods(unittest.TestCase):

    def test_file_exists(self):
        """checks if the file exist"""
        assert os.path.isfile(html_path)

    def test_tag_exists(self):
        """checks if the html file is not empty"""
        html = open(html_path).read()
        self.assertTrue(html)
    
    def test_web_scraper(self):
        """checks if the function will return a string"""
        hotel_name = web_scraper(html_path, 'hp_hotel_name', 'id', 'span')
        assert (type(hotel_name) == str)

if __name__ == '__main__':
    unittest.main()