import urllib2
import re
import utils
from bs4 import BeautifulSoup


authors_list_slug = 'List_of_science_fiction_authors'
author_slugs = []


def wikipedia_url(slug):
    return 'https://en.wikipedia.org/wiki/%s' % slug

def get_soup(url):
    opened_url = urllib2.urlopen(url)
    return BeautifulSoup(opened_url.read(), 'html.parser')


# get author slugs

list_of_authors_soup = get_soup(wikipedia_url(authors_list_slug))

for author_tag in list_of_authors_soup.find_all(utils.is_author_list_tag):
    author_slug = author_tag.get('href').replace('/wiki/', '')
    author_slugs.append(author_slug)


# get author data

with open('author_data.csv', 'w') as author_data_file:

    for author_slug in author_slugs:

        opened_author_url = urllib2.urlopen(wikipedia_url(author_slug))
        author_html = opened_author_url.read()

        author_soup = BeautifulSoup(author_html, 'html.parser')
        author_info = author_soup.find('table', class_='infobox')

        try:
            name       = author_soup.find('h1').text
        except AttributeError:
            name = ''

        lifespan_pattern = re.compile(r'[A-Z][a-z]+ \d+, \d{4} \xe2\x80\x93 [A-Z][a-z]+ \d+, \d{4}')
        lifespan_text = re.findall(lifespan_pattern, author_html)

        birthdate, deathdate = None, None

        if len(lifespan_text) > 1:
            raise Exception('Multiple lifespan deaths')
        elif len(lifespan_text) == 1:
            birthdate, deathdate = lifespan_text[0].split(' \xe2\x80\x93 ')

        if not birthdate:
            try:
                birthdate  = author_info.find('span', class_="bday").text
            except AttributeError:
                birthdate = ''

        try:
            birthplace = author_info.find('a', class_='mw-redirect').text
        except AttributeError:
            birthplace = ''

        if not deathdate:
            try:
                deathdate = author_info.find('span', class_="dday").text
            except AttributeError:
                deathdate = ''

        try:
            deathplace = author_info.find('span', class_="fdsfds").text
        except AttributeError:
            deathplace = ''

        author_data = '%s, %s, %s, %s, %s\n' % (
                name,
                birthdate,
                birthplace,
                deathdate,
                deathplace
            )

        author_data_file.write(author_data.encode('utf-8'))
