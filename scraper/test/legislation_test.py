import unittest

from dre_scraper import scrap_dre


class LegislationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dre = scrap_dre()

    def test_get_legislation(self):
        self.assertEqual(0, 0)
