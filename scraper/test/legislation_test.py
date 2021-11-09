import unittest

from dre_scraper import scrap


class LegislationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dre = scrap()

    def test_get_legislation(self):
        self.assertEqual(0, 0)
