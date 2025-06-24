import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup
import os
import csv

# Импортируем из вашего модуля
from solution import (
    get_count_letter_in_web,
    save_to_csv,
    fetch_counts_per_letter,
)

class TestBeastsProgram(unittest.TestCase):

    def test_get_count_letter_in_web_single_letter(self):
        html = """
        <ul>
            <li>Аист</li>
            <li>Антилопа</li>
            <li>Акула</li>
        </ul>
        """
        soup = BeautifulSoup(html, "html.parser")
        items = soup.find_all("li")
        counts = {}
        counts = get_count_letter_in_web(items, counts)
        self.assertEqual(counts["А"], 3)

    def test_get_count_letter_in_web_multiple_letters(self):
        html = """
        <ul>
            <li>Аист</li>
            <li>Белка</li>
            <li>Волк</li>
        </ul>
        """
        soup = BeautifulSoup(html, "html.parser")
        items = soup.find_all("li")
        counts = {}
        counts = get_count_letter_in_web(items, counts)
        self.assertEqual(counts["А"], 1)
        self.assertEqual(counts["Б"], 1)
        self.assertEqual(counts["В"], 1)

    def test_save_to_csv(self):
        counts = {"А": 3, "Б": 2}
        filename = "test_output.csv"
        save_to_csv(counts, filename)

        self.assertTrue(os.path.exists(filename))

        with open(filename, newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            self.assertIn(["А", "3"], rows)
            self.assertIn(["Б", "2"], rows)

        os.remove(filename)

    @patch("solution.get_wikipedia_li_elements")
    def test_fetch_counts_per_letter_mocked(self, mock_get_elements):
        html_1 = """
        <ul>
            <li>Акула</li>
            <li>Аист</li>
        </ul>
        """
        html_2 = """
        <ul>
            <li>Аист</li>
            <li>Белка</li>
            <li>Бобр</li>
        </ul>
        """

        soup1 = BeautifulSoup(html_1, "html.parser").find_all("li")
        soup2 = BeautifulSoup(html_2, "html.parser").find_all("li")

        mock_get_elements.side_effect = [soup1, soup2, []]  

        counts = fetch_counts_per_letter()
        self.assertEqual(counts["А"], 2)
        self.assertEqual(counts["Б"], 2)  

if __name__ == "__main__":
    unittest.main()