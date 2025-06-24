import requests
from bs4 import BeautifulSoup
import csv

def get_wikipedia_li_elements(URL):
    resp = requests.get(URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    group = soup.find_all("div", class_='mw-content-ltr')[2]
    
    return group.find_all("li")

def get_count_letter_in_web(items, counts, russians_alphabet='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'):
    for item in items:
        letter = item.text[0]

        if letter not in russians_alphabet:
            return counts
        
        if letter not in counts:
            counts[letter] = 0
        counts[letter] += 1

    return counts

def fetch_counts_per_letter():
    russians_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    URL_START = r"https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту&from=<b>А<%2Fb>"
    URL = URL_START
    counts = {}
    while True:
            items = get_wikipedia_li_elements(URL)
            if len(items) == 0:
                break

            counts = get_count_letter_in_web(items, counts)
            if items[-1].text[0] not in russians_alphabet:
                break

            if URL != URL_START:
                counts[items[0].text[0]] -= 1
            
            URL = fr"https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту&pagefrom={str(items[-1].text).replace(' ','+')}&subcatfrom=<b>А<%2Fb>&filefrom=<b>А<%2Fb>#mw-pages"

    return counts

def save_to_csv(counts, filename="beasts.csv"):
    letters = sorted(counts.keys(), key=lambda x: x)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # writer.writerow(["Letter", "Count"])
        for letter in letters:
            writer.writerow([letter, counts[letter]])

def main():
    counts = fetch_counts_per_letter()
    save_to_csv(counts)
    print("Saved beasts.csv with", len(counts), "letters.")

