import requests
import json
import os
from bs4 import BeautifulSoup

class President:
    def __init__(self, name="", date_start="", date_end="", political_party=""):
        self.name = name
        self.date_start = date_start
        self.date_end = date_end
        self.political_party = political_party

    def __repr__(self):
        return f"{self.name} ({self.date_start} - {self.date_end}) {self.political_party}"

# makes the request to the wikipedia api
def get_wiki_data():
    # the url to the wikipedia api
    url = 'https://en.wikipedia.org/w/api.php'
    # the parameters to be sent to the api
    params = {
        'action': 'parse',
        'format': 'json',
        'page': 'List_of_presidents_of_Portugal',
        'prop': 'text',
        'section': '4'
    }
    # makes the request
    response = requests.get(url, params=params)
    # returns the response
    html = response.json().get('parse').get('text').get('*')

    # gets the table inside the html
    table = '<table' + \
        html.split('<table')[1].split('</table>')[0] + '</table>'
    return table

def send_to_json(presidents, file_name):
    # creates parent directories if they don't exist
    if not os.path.exists(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name))

    with open(file_name, 'w') as f:
        json.dump(presidents, f, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)

def main():
    presidents_table_html = get_wiki_data()

    # transforms it into a beautiful soup object
    elements = BeautifulSoup(presidents_table_html, 'html.parser')

    # gets the table rows (including headers and all)
    elements = elements.tbody.find_all('tr')

    # gets only the rows with useful data
    elements = [element for element in elements if 'bgcolor' in element.attrs]
    elements = elements[1:]

    # for each row builds a president object
    presidents = []
    for element in elements:        
        president = President()
        
        # gets the name
        name_element = element.find('td').find('b')
        first_row = name_element is not None
        if first_row:
            president.name = name_element.find('a').text

            # gets the dates
            president.date_start = element.find_all('td')[3].text.replace('[R]', '').strip()
            president.date_end = element.find_all('td')[4].text.replace('[R]', '').strip()
            
            # gets the political party
            referenced_party = element.find_all('td')[5].find('a')
            if referenced_party is not None:
                president.political_party = referenced_party.text.strip()
            else:
                president.political_party = element.find_all('td')[5].text.strip()

            # appends the president to the list
            presidents.append(president)
        else:
            # gets the last element of the list as the current president
            president = presidents[-1]

            # gets the ending date
            president.date_end = element.find_all(
                'td')[2].text.replace('[R]', '').strip()

    send_to_json(presidents, "data/presidents/presidents.json")

main()
