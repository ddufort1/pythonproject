import sqlite3
import pprint
import ssl
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from urllib.parse import urlencode 
from bs4 import BeautifulSoup
import dateutil.parser 

def make_request(url):
    try:
        with urlopen(url, timeout=10) as response:
            print(response.status)
            return response.read(), response
    except HTTPError as error:
        print(error.status, error.reason)
    except URLError as error:
        print(error.reason)
    except TimeoutError:
        print("Request timed out")

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('mydb.sqlite')
cur = conn.cursor()

def create_tables():
    cur.executescript('''
    DROP TABLE IF EXISTS WikiTitle;
    DROP TABLE IF EXISTS WikiChange;

    CREATE TABLE WikiTitle (
        id     INTEGER PRIMARY KEY,
        title_id  TEXT UNIQUE,
        title   TEXT 
    );

    CREATE TABLE WikiChange (
        id     INTEGER PRIMARY KEY,
        mod_date  DATE
    );

    ''')


create_tables()

# navigating pages
#https://www.wikidata.org/w/index.php?title=Q202937&action=history&dir=prev #oldest
#https://www.wikidata.org/w/index.php?title=Q202937&action=history&dir=prev&offset=20131027105346%7C81888404
#https://www.wikidata.org/w/index.php?title=Q202937&action=history #newest

initial_url = "https://www.wikidata.org/w/index.php?"
params = {'title': 'Q202937'
          , 'action': 'history'
          , 'query': "stevie+ray+vaughan"
          , 'limit': '500' 
         }
surl = urlencode(params, doseq=True)
url = initial_url+surl
title = 'Stevie Ray Vaughan Wiki Page'

print(url)

html = urlopen(url, context=ctx, timeout=20).read()
soup = BeautifulSoup(html, "html.parser")

# Retrieve  tags
tags = soup.find_all("a", class_="mw-changeslist-date")

for tag in tags:
    # Look at the parts of a tag
    print('TAG:', tag)
#    print('Date:', tag.get_text())    
#    print('Attrs:', tag.attrs)
#    print(tag['title'])

    title_id = (tag['title'])
    t_date = (tag.get_text())
    mod_date = dateutil.parser.parse(t_date)

    print(title, mod_date)

    cur.execute('''INSERT OR IGNORE INTO WikiTitle (title_id, title)
        VALUES ( ?, ? )''', ( title_id, title, ) )

    cur.execute('''INSERT OR IGNORE INTO WikiChange (mod_date)
        VALUES ( ? )''', ( mod_date, ) )


conn.commit()
cur.close()




