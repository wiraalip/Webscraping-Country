from bs4 import BeautifulSoup
import requests
import csv

def scrape_country(url):
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch the webpage")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def extract_country_data(soup):
    countries = []

    for country in soup.find_all('div', class_ ='col-md-4 country'):
        country_name_element = country.find('h3', class_='country-name')
        country_capital_element = country.find('span', class_='country-capital')
        country_population_element =  country.find('span', class_='country-population')
        country_area_element = country.find('span', class_='country-area')
        
        if country_name_element:
            country_name = country_name_element.text.strip()
            country_capital = country_capital_element.text.strip()
            country_population = country_population_element.text.strip()
            country_area = country_area_element.text.strip()
        
            countries.append({'Country': country_name, 'Capital': country_capital, 'Population': country_population, 'Area (Km2)': country_area})

    return countries



if __name__ == "__main__":
    url = 'https://www.scrapethissite.com/pages/simple/'
    soup = scrape_country(url)

    if soup:
        country_data = extract_country_data(soup)
        print(country_data)

        csv_filename = 'country_data.csv'
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Country', 'Capital', 'Population', 'Area (Km2)']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(country_data)
    else:
        print("Webpage scraping failed.")