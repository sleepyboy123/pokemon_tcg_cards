import requests

from bs4 import BeautifulSoup
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

print("{:<5} {:<40} {:<40} {:<10} {:<15} {:<15}".format("No", "Pokemon Set", "Pokemon ID", "Grade", "Purchase Price", "Current Price"))
print("-" * 135)  

total_value = 0

for index, card in enumerate(owned_cards, start=1):
    url = f"https://www.pricecharting.com/game/{card['set']}/{card['id']}"
    response = requests.get(url)
    current_price = extract_price_by_label(response.text, card["grade"])
    total_value += float(current_price[1:])
    print("{:<5} {:<40} {:<40} {:<10} {:<15} {:<15}".format(index, card["set"], card["id"], card["grade"], card["purchase_price"], current_price))

print("-" * 135)  
print(round(total_value, 2))