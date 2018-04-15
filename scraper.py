# For parsing the command line arguments 
import argparse

# For parsing the HTML
from bs4 import BeautifulSoup

# For getting the HTML
from requests import get
from requests.exceptions import RequestException
from contextlib import closing

# For converting string to JSON
import json

# For writing to CSV files
import csv

# Get the url (specified as a command line argument)
parser = argparse.ArgumentParser()
parser.add_argument("url")
args = parser.parse_args()

print("Scraping: ")
print(args.url)

# Custom scraping code for pulling out the relevant information

def scrape_url(url):
    # Get the raw HTML for the page (Since it's a React app, it isn't
    # going to render when we grab it from a python script)
    response = simple_get(url)

    # If we got a successful response....
    if response is not None:
        # ...turn it into HTML
        html = BeautifulSoup(response, 'html.parser')

        # There are multiple <script> tags containing things like Google Analytics
        # the React client library, and some other stuff, but we only care about the
        # one with the initialAppState JSON array in it
        script_sections = html.find_all('script')
        # print(script_sections[4].text)

        json_raw = script_sections[4].text

        # Strip off the Javascript assignment leaving only the JSON
        json_raw = json_raw[25:-1]

        # Turn it into JSON!
        club_info = json.loads(json_raw)
        print(club_info)

        return club_info

def write_to_csv(club_info):

    fields = [
        club_info['preFetchedData']['organization']['primaryContact']['primaryEmailAddress'],
        club_info['preFetchedData']['organization']['primaryContact']['firstName'],
        club_info['preFetchedData']['organization']['primaryContact']['lastName'],
        club_info['preFetchedData']['organization']['description'],
        club_info['preFetchedData']['organization']['name'],
        club_info['preFetchedData']['organization']['status'],
        club_info['preFetchedData']['organization']['socialMedia'].get('facebookUrl', ''),
        club_info['preFetchedData']['organization']['socialMedia'].get('externalWebsite', ''),
        club_info['preFetchedData']['organization']['socialMedia'].get('flickrUrl', ''),
        club_info['preFetchedData']['organization']['socialMedia'].get('instagramUrl', ''),
        club_info['preFetchedData']['organization']['socialMedia'].get('pinterestUrl', ''),
        club_info['preFetchedData']['organization']['socialMedia'].get('googlePlusUrl', ''),
        club_info['preFetchedData']['organization']['socialMedia'].get('googleCalendarUrl', ''),
        club_info['preFetchedData']['organization']['socialMedia'].get('linkedInUrl', ''),
        club_info['preFetchedData']['organization']['socialMedia'].get('tumblrUrl', ''),
        club_info['preFetchedData']['organization']['socialMedia'].get('vimeoUrl', ''),
        club_info['preFetchedData']['organization']['socialMedia'].get('youtubeUrl', ''),
        club_info['preFetchedData']['organization']['socialMedia'].get('twitterUrl', ''),
        club_info['preFetchedData']['organization']['socialMedia'].get('twitterUserName', '')
     ]

    with open('clubs.csv', 'a') as csvfile:
        club_writer = csv.writer(csvfile)
        club_writer.writerow(fields)

# Functions supporting the scraping, stolen from RealPython.com!
# https://realpython.com/python-web-scraping-practical-introduction/

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=False)) as resp:
            print(resp)
            if is_good_response(resp):
                return resp.content
            else:
                print("Bad response")
                print(resp)
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

    def log_error(e):
        """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

# The actual code that runs:
club_info = scrape_url(args.url)
write_to_csv(club_info)
