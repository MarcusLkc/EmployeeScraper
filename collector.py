"""Web Scraper for the security licenses government websites

This module is uses two classes to scrape employee roster
data from the https://www.dos.ny.gov/ websites and generates 
cvs files of the data that was chosen based on the department or businessname

You can go here to visit the starting index for the websites and make your
own searchs: https://appext20.dos.ny.gov/lcns_public/chk_load

Or to navigate to a differnet department and chase the baseurl
of IdCollector

"""


import requests
from bs4 import BeautifulSoup
import json
import math
import datetime
import pandas as pd


class Scraper(object):
    """Default webscraper template for future Scraper classes to inherit from

    Arguments:
        base_url (str) -- BaseUrl for all of our future scrapers to start off 
                          with defaults to None
        headers (obj) -- Default Headers for when making any outgoing requests 
                         for generating html
    """

    base_url = None
    headers = {
        'cache-control': 'no-cache',
        'postman-token': '12adf88a-d1b9-0924-96ad-42808c2825eb'
    }

    def generate_soup(self, url, params=None):
        """Utility class for grabbing requesting url and parsing html with beautifulsoup

        Arguments:
            url {str} -- url of website to get html data from

        Keyword Arguments:
            params (dic of str) -- [description] (default: {None})

        Returns:
            soup -- returns a BeautifulSoup object with parsed html
                    for more info on handling these objects refer to
                    the bs4 docs
        """

        response = requests.request(
            "GET", url, headers=self.headers, params=params)
        return BeautifulSoup(response.text, "html.parser")

    def collect_data(self):
        pass

    def clean_data(self):
        pass

    def save(self):
        pass


class IdCollector(Scraper):
    """Collects all the Id links of different employees that can be used to
    generate dynamic urls later


    Arguments:
        Scraper (object) -- Inherits from the Scraper template class and makes
                            use of the generate soup utility function
        ids (list of ints) -- These are all the links IDs collected by the webscraper,
                              we use these to generate dynamic urls
        base_url (str) -- the starting url of our web scraper
        ids_total (int) -- total amount of link ids to be collected
        record_count (int) -- total amount of acquired records
        page_count (int) -- total amount of pages to scrape for a department
        ids_per_page -- links per page

    """

    def __init__(self, page_count=None, base_url=None):

        self.ids = []
        self.base_url = base_url or "https://appext20.dos.ny.gov/lcns_public/roster_cursor?p_record_id=11000080984&p_display_start="
        self.ids_total = None
        self.record_count = None
        self.page_count = page_count
        self.ids_per_page = 25
        self._calculate_site_records()

    def _calculate_site_records(self):
        """function for intiating our webscraper class with site statistics variables

        """

        first_page_url = self.base_url + '1&'
        soup = self.generate_soup(first_page_url)
        result = soup.find('font', class_='large_bold')
        self.ids_total = int(result.text.split(' ')[-2])
        if self.page_count == None:
            self.page_count = math.ceil(self.ids_total / self.ids_per_page)

    def collect_data(self):
        """Collects all of the employee id links from websites pages and 
        saves them in the ids list

        Returns:
        (list: ints) -- Returns the ids of our collected data within a list
        """

        for i in range(self.page_count + 1):
            url = self.base_url + '{}&'.format(i)
            soup = self.generate_soup(url)
            results_set = soup.find_all(headers='id')
            for data in results_set:
                for link in data.find_all('a'):
                    self.ids.append(link.get('href')[-9::])
        return self.ids

    def save(self, filename=None):
        """This function saves all of the link data we gathered from the web

        Keyword Arguments:
            filename (str) -- filename to save ids in if given otherwise will be saved as ids.txt (default: {None})

        Returns:
            (None) -- None
        """

        filename = filename or 'ids.txt'
        with open('ids.txt', 'w', encoding='utf-8') as f:
            json.dump(self.ids, f, ensure_ascii=False)

    def __len__(self):
        return len(self.ids)

    def __getitem__(self, index):
        return self.ids[index]


class EmployeeRecords(Scraper):
    """This class is used to gather employee data from html pages
    and save it to an excel file.

    Arguments:
        Scraper (Inherited) -- Scraper class that we inherited from for default methods

    Attributes:
        links (list: ints) -- employee links to search
        employees (list: obj) -- A List of dictionary items that represent our Employees


    """

    base_url = "https://appext20.dos.ny.gov/lcns_public/bus_name_inq_frm"

    def __init__(self, employee_links):

        self.links = employee_links
        self.employees = []

    def collect_data(self):
        """Appends the links receiver to our base_url then visits 
        every page to collect employee data


        Returns:
            (list: objects) -- Returns a list that contaisn all of our employee dict objects
        """

        for link in self.links:
            query_string = {"p_record_id": link}
            soup = self.generate_soup(self.base_url, query_string)
            self.employees.append(
                self.generate_employee(self.clean_data(soup)))
        return self.employees

    def clean_data(self, soup):
        """This function cleans and extracts the data from an individual employee html page

        Arguments:
            soup {object: BeautiFulSoup} -- A beautifulsoup parsed html object

        Returns:
            (list: str) -- List of strings from our table rows
        """

        self.data = []
        for tr in soup.find_all('tr'):
            if "Services" in tr.text:
                break
            if tr.text and "NOT" not in tr.text:
                table_row = tr.text.splitlines()
                for text in table_row:
                    if text:
                        self.data.append(text.strip())
        return self.data

    def generate_employee(self, data):
        """This function generates an employee objet by filtering our list elements and placing 
        adjacent list items into our employee object

        Arguments:
            data {list: str} -- the string of keywords found on our html page

        Returns:
            (dict) -- returns employee as a dictionary of keywords
        """

        dict_emp = {}
        i = 0
        l = len(data)
        while i < l-1:
            dict_emp[data[i]] = data[i+1]
            i += 2
            if i < l and validate_date(data[i]):
                dict_emp[data[i-2] + '2'] = data[i]
                i += 1

        return dict_emp

    def save(self, filename=None):
        """Saves our employee objects to an excel file
            Arguments:
                filename (str) -- filename to save file in, filename must end in xlsx or other excel endings
                                  Default -- employees.xlsx
        """
        filename = filename or 'employees.xlsx'
        with pd.ExcelWriter(filename) as writer:
            df = pd.DataFrame(self.employees)
            df = df.fillna(0)
            df.to_excel(writer)


def validate_date(date_text):
    """Utility function to test if string is a date using the '%m/%d/%Y' Month/day/Year formula

    Arguments:
        date_text (string) -- text to consider as data

    Returns:
        (bool) -- Returns True if text is string is date False otherwise
    """

    try:
        datetime.datetime.strptime(date_text, '%m/%d/%Y')
        return True
    except ValueError:
        return False
