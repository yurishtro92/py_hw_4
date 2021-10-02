import json
import requests
from bs4 import BeautifulSoup
import hashlib

class CountriesIterator:
    def __init__(self, file_path):
        self.file_path = file_path

    def __iter__(self):
        return self

    def __next__(self):
        countries_from_file = str()
        countries_from_wiki_dict = {}
        countries_for_recording = {}
        with open(self.file_path, encoding="utf-8") as f:
            countries = json.load(f)
            for country in countries:
                country_name = (country['name']['official']).lower()
                countries_from_file += country_name + ' '
        response = requests.get('https://en.wikipedia.org/wiki/List_of_country-name_etymologies')
        response.raise_for_status()
        text = response.text
        soup = BeautifulSoup(text, features='html.parser')
        country_names = soup.find_all('h3')
        for country_name in country_names:
            if len(country_name) == 2:
                country_name_ = country_name.find_all('span', class_='mw-headline')
                country_name_text = [country_name.text.lower() for country_name in country_name_]
                country_link = country_name.find('a').attrs.get('href')
                for country in country_name_text:
                    countries_from_wiki_dict[country] = 'https://en.wikipedia.org/' + country_link
        for country in countries_from_wiki_dict:
            if country in countries_from_file:
                countries_for_recording[country] = countries_from_wiki_dict[country]
        with open('out.txt', 'w', encoding="utf-8") as output:
            json.dump(countries_for_recording, output)
        raise StopIteration
        return self

for i in CountriesIterator('countries.json'):
    print(i)
#
class MD5Generator:
    def __init__(self, file_path):
        self.file_path = file_path

    def generator(self):
        with open(self.file_path, encoding="utf-8") as f:
            file = json.load(f)
            for string in file:
                print(hashlib.md5(str(string).encode('utf-8')).hexdigest())
        return self

gen = MD5Generator('countries.json')
print(gen)












