"""
Created on Mon Oct 25 21:04:38 2021

@author: LReynolds
"""

import requests
from bs4 import BeautifulSoup

class Scraper():
    TARGET_URL = "https://www.towerbridge.org.uk/lift-times"
    TIMEOUT = 5
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
        }
    
    def __init__(self):
        pass
    
    def scrape(self):
        try:
            response = requests.get(Scraper.TARGET_URL,\
                                    headers=Scraper.HEADERS, \
                                    timeout=Scraper.TIMEOUT)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
            return None
        except requests.exceptions.ConnectionError as e:
            print("Connection Failed.")
            print(e)
            return None
        except requests.exceptions.RequestException as e:
            # Ambigous error, bail
            raise SystemExit(e)
        
        return response.text


class Parser():
    def __init__(self):
        pass
        
    def parse(self, text):
        events = []
        
        soup = BeautifulSoup(text, 'html.parser')
        
        table = self._get_table(soup)
        rows = table.find_all('tr')
        i = 0
        for row in rows:
            print(i)
            event = row.find_all('views-field views-field-field-date-time')
            date = event[1].text.strip()
            time = event[2].text.strip()
            vessel = event[3].text.strip()
            events.append(LiftEvent(date, time, vessel))
            i = i+1
    
        return events
    
    def _get_table(self, soup):
        return soup.find('table', class_='views-table')
    

class LiftEvent():
    def __init__(self, date, time, vessel):
        self.date = date
        self.time = time
        self.vessel = vessel
        
scraper = Scraper()
parser = Parser()
response = scraper.scrape()
#events = parser.parse(response)