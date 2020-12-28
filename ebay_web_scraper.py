# Todo
# 1. Make a request to ebay.ca and get a page
# 2. Collect data frrom each detail page
# 3. Collect all links to detail pages of each product
# 4. Write scraped data to a csv file

import requests
from bs4 import BeautifulSoup
import re
import csv
import itertools
import threading
import time
import sys


def get_page(url):
    response = requests.get(url)

    if not response.ok:
        print('Server responded:', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_detail_data(soup):
    # Title
    try:
        # find_All finds all elements
        h1 = soup.find('h1', id='itemTitle').find(text=True, recursive=False)
    except:
        h1 = '[✖] Title not found'
    # Price
    try:
        try:
            price = soup.find('span', id="prcIsum").text
        except:
            price = '[✖] Item is a bid'
    except:
        price = '[✖] Price not found'

    # Shipping
    try:
        shipping = soup.find('span', id="fshippingCost").text
        shipping = re.sub(r'\s', '', shipping)
    except:
        shipping = '[✖] Shipping price not found'

    # Import charge
    try:
        import_charge = soup.find('span', id='impchCost').text

        if import_charge == '':
            import_charge = '[✓] No Import charge'
    except:
        import_charge = '[✖] Import charge not found'

    data = {
        'Title': h1,
        'Price': price,
        'Shipping Cost': shipping,
        'Import Charge': import_charge
    }

    return data


def get_index_data(soup):
    try:
        links = soup.find_all(
            'a', class_="s-item__link")
    except:
        links = []

    urls = [item.get('href') for item in links]

    return urls


def write_csv(data, url):
    with open('scraper_data.csv', 'a', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        row = [data['Title'], data['Price'],
               data['Shipping Cost'], data['Import Charge'], url]

        writer.writerow(row)


def main():
    url = 'https://www.ebay.ca/sch/i.html?&_nkw=apple+iphone+cracked+screen&_pgn=1'

    products = get_index_data(get_page(url))

    for link in products:
        data = get_detail_data(get_page(link))
        write_csv(data, link)
        print(data)


done = False


def startup():
    time.sleep(0.5)
    print('[#] Starting scripts...\n')
    time.sleep(0.5)
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rPrepping Scraper ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r[#] Starting Scraper     ')


t = threading.Thread(target=startup)
t.daemon = True
t.start()

# long process here
time.sleep(10)
done = True

if __name__ == '__main__':
    main()
    startup()
