from bs4 import BeautifulSoup
import csv
from datetime import datetime
from playsound3 import playsound
import random

# import requests
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from cards import owned_cards


def extract_price_by_label(html, label):
    soup = BeautifulSoup(html, "html.parser")

    # Find the <td> with the specific label
    label_td = soup.find("td", string=label)

    if label_td:
        # Get the next <td> sibling (the price)
        price_td = label_td.find_next_sibling("td")
        if price_td:
            return price_td.text.replace(",", "").replace("$", "").strip()


date_time = datetime.today().strftime("%Y-%m-%d")

options = webdriver.ChromeOptions()

# Hopefully bypasses Cloudflare
# https://github.com/jiwan-gharti/selenium-cloudflare-bypass-chapcha/blob/main/main.py
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")
options.add_argument("--auto-open-devtools-for-tabs")
options.add_argument(
    f"--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
)
driver = webdriver.Chrome(options=options)

with open(f"cards_report_{date_time}.txt", "w", encoding="utf-8") as file, open(
    f"cards_report_{date_time}.csv", "w", newline="", encoding="utf-8"
) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(
        ["No", "Pokemon Set", "Pokemon ID", "Grade", "Purchase Price", "Current Price"]
    )
    header = "{:<5} {:<50} {:<40} {:<10} {:<15} {:<15}".format(
        "No", "Pokemon Set", "Pokemon ID", "Grade", "Purchase Price", "Current Price"
    )
    print(header)
    file.write(header + "\n")

    separator = "-" * 135
    print(separator)
    file.write(separator + "\n")

    total_value = 0

    # Deal with Cloudflare
    driver.get("https://www.pricecharting.com/")
    time.sleep(5)

    for index, card in enumerate(owned_cards, start=1):
        try:
            url = f"https://www.pricecharting.com/game/{card['set']}/{card['id']}"
            driver.get(url)
            time.sleep(random.random() * 3)
            text = driver.page_source
            if "<title>Just a moment...</title>" in text:
                playsound("tuturu.mp3", block=False)
                time.sleep(10)
                text = driver.page_source
            try:
                extracted_price = extract_price_by_label(text, card["grade"])
                current_price = round(float(extracted_price) * 1.3, 2)
                total_value += current_price
            except AttributeError as e:
                print(e)
                current_price = e
            line = "{:<5} {:<50} {:<40} {:<10} {:<15} {:<15}".format(
                index,
                card["set"],
                card["id"],
                card["grade"],
                card["purchase_price"],
                current_price,
            )
            writer.writerow(
                [
                    index,
                    card["set"],
                    card["id"],
                    card["grade"],
                    card["purchase_price"],
                    current_price,
                ]
            )
            print(line)
            file.write(line + "\n")
        except Exception as e:
            print(e)

    separator = "-" * 135
    print(separator)
    file.write(separator + "\n")

    total_line = "$" + str(round(total_value, 2))
    print(total_line)
    file.write(total_line + "\n")
