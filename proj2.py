#proj2.py
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#### Problem 1 ####
print('\n*********** PROBLEM 1 ***********')
print('New York Times -- First 10 Story Headings\n')

url = 'http://www.nytimes.com'
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

storynumber = 0
for story_heading in soup.find_all(class_="story-heading"):
    if storynumber < 10:
        if story_heading.a:
            print(story_heading.a.text.replace("\n", " ").strip())
        else:
            print(story_heading.contents[0].strip())
        storynumber = storynumber + 1


#### Problem 2 ####
print('\n*********** PROBLEM 2 ***********')
print('Michigan Daily -- MOST READ\n')

url = 'https://www.michigandaily.com/'
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

for most_read in (soup.find_all(class_="view-most-read")):
     print(most_read.ol.text.strip())


#### Problem 3 ####
print('\n*********** PROBLEM 3 ***********')
print("Mark's page -- Alt tags\n")

url = 'http://newmantaylor.com/gallery.html'
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

for image in soup.findAll("img"):
    if image.get('alt'):
        print (image.get('alt'))
    else:
        print ('No alternative text provided!!')


#### Problem 4 ####
print('\n*********** PROBLEM 4 ***********')
print("UMSI faculty directory emails\n")

req = urllib.request.Request('https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=4', None, {'User-Agent': 'SI_CLASS'})
html = urllib.request.urlopen(req, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

#list for urls to the list of faculty, 1 empty list for the individual faculty page links, and 1 empty list for the final emails
pagelist = ['https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=4', 'https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=4&page=1', 'https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=4&page=2', 'https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=4&page=3', 'https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=4&page=4', 'https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=4&page=5']
urllist = []
emaillist = []

#loop through the pages
for page in pagelist:
    req = urllib.request.Request(page, None, {'User-Agent': 'SI_CLASS'})
    html = urllib.request.urlopen(req, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')

#loop through one page at a time, find faculty contact link, make a url out of it
    for link in soup.findAll('a', href=True, text='Contact Details'):
        node = (link['href'])
        contacturl = 'https://www.si.umich.edu' + node
        urllist.append(contacturl)

#loop through each newly created faculty url
    for i in urllist:
        req = urllib.request.Request(i, None, {'User-Agent': 'SI_CLASS'})
        html = urllib.request.urlopen(req, context=ctx).read()
        soup = BeautifulSoup(html, 'html.parser')

#loop through the html for each faculty page, find the email text, add it to email list
        for email in soup.find_all('a', href=True, text=re.compile('.+@umich\.edu')):
            if email.string in emaillist:
                pass
            else:
                emaillist.append(email.string)

#print enumerated email list
for counter, email in enumerate(emaillist, 1):
    print(counter, email)
