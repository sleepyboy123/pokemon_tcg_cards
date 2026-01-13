from bs4 import BeautifulSoup
import cloudscraper
from datetime import datetime
import requests

from cards import owned_cards

def extract_price_by_label(html, label):
    soup = BeautifulSoup(html, 'html.parser')

    # Find the <td> with the specific label
    label_td = soup.find('td', string=label)

    if label_td:
        # Get the next <td> sibling (the price)
        price_td = label_td.find_next_sibling('td')
        if price_td:
            return price_td.text.strip()

scraper = cloudscraper.create_scraper()

date_time = datetime.today().strftime('%Y-%m-%d')

with open(f"cards_report_{date_time}.txt", "w", encoding="utf-8") as file:
    header = "{:<5} {:<40} {:<40} {:<10} {:<15} {:<15}".format("No", "Pokemon Set", "Pokemon ID", "Grade", "Purchase Price", "Current Price")
    print(header) 
    file.write(header + "\n")

    separator = "-" * 135
    print(separator) 
    file.write(separator + "\n")

    total_value = 0

    for index, card in enumerate(owned_cards, start=1):
        url = f"https://www.pricecharting.com/game/{card['set']}/{card['id']}"
        response = scraper.get(url)
        print(response.status_code)
        try:
            current_price = float(extract_price_by_label(response.text, card["grade"]).replace(",","")) * 1.3
            total_value += current_price
        except AttributeError as e:
            current_price = url
        line = "{:<5} {:<40} {:<40} {:<10} {:<15} {:<15}".format(index, card["set"], card["id"], card["grade"], card["purchase_price"], current_price)
        print(line)
        file.write(line + "\n")

    separator = "-" * 135
    print(separator)
    file.write(separator + "\n")

    total_line = "$" + str(round(total_value, 2))
    print(total_line)
    file.write(total_line + "\n")