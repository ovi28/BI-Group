import bs4
import requests
import csv
import os

def run():
    out_dir = './data/out'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    base_url = 'http://138.197.184.35/boliga/'
    urls = ['1050-1549_1.html', '1050-1549_2.html']
    urls = [os.path.join(base_url, url) for url in urls]

    fst_fourty_results = scrape(urls[0])
    snd_fourty_results = scrape(urls[1])
    fst_results = fst_fourty_results + snd_fourty_results

    save_to_file = os.path.join(out_dir, os.path.basename(urls[0]).split('.')[0] + '.csv')
    save_to_csv(fst_results, save_to_file)


def save_to_csv(data, path='./out/boliga.csv'):
    
    with open(path, 'w', encoding='utf-8') as output_file:
        output_writer = csv.writer(output_file)
        output_writer.writerow(['address','zip_code','price','sell_date',
                                'sell_type','price_per_sq_m','no_rooms',
                                'housing_type','size_in_sq_m','year_of_construction',
                                'price_change_in_pct'])

        for row in data:
            output_writer.writerow(row)

def scrape(url):
    data = []
    r = requests.get(url)
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.content.decode('utf-8'), 'html5lib')
    soup = str(soup).replace("<br/>", " ")
    soup = bs4.BeautifulSoup(soup, 'html5lib')
    table = soup.find('table')
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        
        # Decode address column
        address_str = cols[0].text.strip()
        address_str = address_str.replace("<br />"," ")
        zip_number = int(address_str.split(' ')[-3])
        
        # Decode price
        price_str = cols[1].text.strip()
        price_str = price_str.replace(".","")
        price = float(price_str)
        
        # Decode sales date
        sale_date_str = cols[2].text.strip()
        sale_date = sale_date_str.split(' ')[0]
        sale_type = sale_date_str.split(' ')[1]
        
         # Decode sales date
        price_per_sq_mr_str = cols[3].text.strip()
        price_per_sq_mr_str = price_per_sq_mr_str.replace(".","")
        price_per_sq_mr = int(price_per_sq_mr_str)
        
        # Decode number of rooms
        no_rooms_str = cols[4].text.strip()
        no_rooms = int(no_rooms_str)
        
        # Decode housing type
        housing_type = cols[5].text.strip()
        
        # Decode selling date and type
        size_in_sq_m_str = cols[6].text.strip()
        size_in_sq_m = int(size_in_sq_m_str)

        # Decode year of construction
        year_of_construction_str = cols[7].text.strip()
        year_of_construction = int(year_of_construction_str)
        
         # Price change in pct
        price_change_in_pct = cols[8].text.strip()
        

        decoded_row = (address_str, zip_number, price,sale_date,sale_type,price_per_sq_mr,
                        no_rooms, housing_type, size_in_sq_m,
                        year_of_construction,price_change_in_pct)
        data.append(decoded_row)
    
    return data