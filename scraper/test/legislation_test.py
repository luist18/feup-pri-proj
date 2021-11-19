import unittest

from dre_scraper import scrap
from dre_scraper.exporter import export_to_csv


class LegislationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dre = scrap()

    def test_get_legislation(self):
        self.assertEqual(0, 0)
        export_to_csv(self.dre)
