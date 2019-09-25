import os, requests, pprint, json, bs4

def find_all(uri):
    soup = bs4.BeautifulSoup(requests.get(uri).text, 'html.parser')
    pprint.pprint(soup.find('div', {'class':'results-dl'}))


find_all("https://tangorin.com/sentences?search=晴れる")