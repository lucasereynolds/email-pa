import datetime
import requests
import logging

from bs4 import BeautifulSoup

class Scraper():
    """Scraper class to get response object from HTTP request."""
    
    TARGET_URL = "https://www.towerbridge.org.uk/lift-times"
    TIMEOUT = 5
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
        }
    
    def __init__(self, target_url):
        self.target_url = target_url
    
    def scrape(self):
        """
        Return response object from HTTTP request if successful.
               
        If any error occurs, we log appropriately and then exit.        
        
        Raises
        ------
        SystemExit
            DESCRIPTION.

        Returns
        -------
        requests.Response
            Response of the HTTP request made if successful, None otherwise.
        """
        try:
            response = requests.get(self.target_url,\
                                    headers=Scraper.HEADERS, \
                                    timeout=Scraper.TIMEOUT)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # TODO: Log appropriately
            raise SystemExit(e)
        except requests.exceptions.ConnectionError as e:
            # TODO: Log appropriately
            print("Connection Failed.")
            print(e)
            raise SystemExit(e)
        except requests.exceptions.RequestException as e:
            # TODO: Log appropriately
            raise SystemExit(e)
        
        return response.text


class Parser():
    """Parser class to pass HTML from Scraper."""
    
    def __init__(self):
        """Construct an empty Parser object."""
        pass
        
    def parse(self, text):
        """Parse HTML and return list of bridge lift events."""
        events = []
        
        soup = BeautifulSoup(text, "html.parser")
        
        # To filter out events more than one week ahead
        cur_date = datetime.date.today() + datetime.timedelta(days=6)
        
        table = self._get_table(soup)
        rows = table.find_all("tr")
        rows = rows[1:]  # remove header
        for row in rows:
            event = row.find_all("td")
            date = event[1].text.strip()
            time = event[2].text.strip()
            vessel = event[3].text.strip()
            if self._to_date(date) < cur_date:  # only show for this week
                events.append(LiftEvent(date, time, vessel))
    
        return events
    
    def _get_table(self, soup):
        return soup.find("table", class_="views-table")
    
    @staticmethod
    def _to_date(date_string):
        """Aux function to convert date as string into datetime object."""
        date_object = datetime.datetime.strptime(date_string, "%d %b %Y").date()
        return date_object
    

class LiftEvent():
    """Class to store informationa about each bridge lift event."""
    
    def __init__(self, date, time, vessel):
        """Construct LiftEvent object."""
        self.date = date
        self.time = time
        self.vessel = vessel
    
    def __repr__(self):
        """Return nice string representation of LiftEvent object."""
        return f"Date: {self.date} | Time: {self.time} | Vessel: {self.vessel}"
 
if __name__ == "__main__":       
    scraper = Scraper()
    parser = Parser()
    response = scraper.scrape()
    events = parser.parse(response)