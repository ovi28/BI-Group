import bs4
import requests
import csv
import os

def scrape_the_index():
    data = []
    r = requests.get("http://138.197.184.35/boliga/")
    soup = bs4.BeautifulSoup(r.content.decode('utf-8'), 'html5lib')
    for link in soup.find_all('a', href=True)[5:]:
      if link.has_attr('href'):
            data.append(link['href'])
    return data

def save_to_csv(data, path='./out/boliga.csv'):
    print(path)
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
        if address_str.split(' ')[-3].isdigit():
            zip_number = int(address_str.split(' ')[-3])
        else:
            zip_number = 0
       
        
        # Decode price
        price_str = cols[1].text.strip()
        price_str = price_str.replace(".","")
        
        if price_str.isdigit():
            price = float(price_str)
        else: 
            price = 0
        
        # Decode sales date
        sale_date_str = cols[2].text.strip()
        sale_date = sale_date_str.split(' ')[0]
        sale_type = sale_date_str.split(' ')[1]
        
         # Decode sales date
        price_per_sq_mr_str = cols[3].text.strip()
        price_per_sq_mr_str = price_per_sq_mr_str.replace(".","")
        if price_per_sq_mr_str.isdigit():
            price_per_sq_mr = int(price_per_sq_mr_str)
        else: 
            price_per_sq_mr = 0
        
        # Decode number of rooms
        no_rooms_str = cols[4].text.strip()
        if no_rooms_str.isdigit():
            no_rooms = int(no_rooms_str)
        else: 
            no_rooms = 0
        
        # Decode housing type
        housing_type = cols[5].text.strip()
        
        # Decode selling date and type
        size_in_sq_m_str = cols[6].text.strip()
        if size_in_sq_m_str.isdigit():
            size_in_sq_m = int(size_in_sq_m_str)
        else: 
            size_in_sq_m = 0
       

        # Decode year of construction
        year_of_construction_str = cols[7].text.strip()
        if year_of_construction_str.isdigit():
            year_of_construction = int(year_of_construction_str)
        else: 
            year_of_construction = 0
        
         # Price change in pct
        price_change_in_pct = cols[8].text.strip()
        

        decoded_row = (address_str, zip_number, price,sale_date,sale_type,price_per_sq_mr,
                        no_rooms, housing_type, size_in_sq_m,
                        year_of_construction,price_change_in_pct)
        data.append(decoded_row)
    
    return data
    
    
    
def run():
    out_dir = './data/out'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    base_url = 'http://138.197.184.35/boliga/'
    urls = scrape_the_index()
    urls = [os.path.join(base_url, url) for url in urls]
    info = []
    x = 0
    link_zip = ""
    for link in urls:
        print(link)
        if link.split("_")[1] == "1.html":
        
            print("getting here")
            if len(info)>0:
                 if len(link_zip) < 1:
                      link_zip = link
                 save_to_file = os.path.join(out_dir, os.path.basename(link_zip.split('_')[0] + '.csv'))
                 save_to_csv(info, save_to_file)
                 link_zip = link
                 info = []
        info = info + scrape(link)
    save_to_file = os.path.join(out_dir, os.path.basename(link_zip.split('_')[0] + '.csv'))
    save_to_csv(info, save_to_file)
   