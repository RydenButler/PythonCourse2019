#### Reading and writing files


## Reading text files ------------------------------------------------
import sys

## Read all lines as one string
with open('test_readfile.txt') as f:
  the_whole_thing = f.read()
  print(the_whole_thing)


## Read line by line
with open('test_readfile.txt') as f:
  lines_list = f.readlines()
  for l in lines_list:
    print(l)

## More efficiently we can loop over the file object
## (i.e. we don't need the variable lines)
with open('test_readfile.txt') as f:   
  for l in f:
    print(l)
    
    
## We can also manually open and close files,
## now we need to handle exceptions and close
## I never do this
f =  open('test_readfile.txt')
print(f.read())
f.close()


## Writing text files ------------------------------------------------

## Writing files is easy,
## open command takes r, w, a, plus some others
with open('test_writefile.txt', 'w') as f:
  ## wipes the file clean and opens it
  f.write("Hi guys.")
  f.write("Does this go on the second line?")
  f.writelines(['a\n', 'b\n', 'c\n'])

with open('test_writefile.txt', 'a') as f:
  ## appends
  f.write("I got appended!")



## Writing csv files ------------------------------------------------
import csv

## Open a file stream and create a CSV writer object
with open('test_writecsv.csv', 'w') as f:
  my_writer = csv.writer(f)
  for i in range(1, 100):
    my_writer.writerow([i, i-1])


## Now read in the csv
with open('test_writecsv.csv', 'r') as f:
  my_reader = csv.reader(f)
  mydat = []
  for row in my_reader:
    mydat.append(row)
print(mydat)

    
## Adding column names
with open('test_csvfields.csv', 'w') as f:
  my_writer = csv.DictWriter(f, fieldnames = ("A", "B"))
  my_writer.writeheader()
  for i in range(1, 100):
    my_writer.writerow({"B":i, "A":i-1})
    
    
with open('test_csvfields.csv', 'r') as f:
  my_reader = csv.DictReader(f)
  for row in my_reader:
    print(row)






#### Parsing HTML


## Parsing HTML ------------------------------------------------

## pip3 install beautifulsoup4

from bs4 import BeautifulSoup
import urllib.request
import random
import time
import os

## Open a web page
web_address = 'https://polisci.wustl.edu/people/88/'
web_page = urllib.request.urlopen(web_address)
web_page

## Parse it
soup = BeautifulSoup(web_page.read())
soup.prettify()

## Find all cases of a certain tag
## Returns a list... remember this!
soup.find_all('a')
soup.find_all('h3')

## Get the script of a certain tag
fields = soup.find_all('h3') ## list of html entries
[i.text for i in fields] ## grab just the text from each one

# Get the attributes
all_a_tags = soup.find_all('a')
all_a_tags

all_a_tags[57]
all_a_tags[57].attrs ## a dictionary with the attributes
l = {"class" : [], "href" : []}
for p in [57,58]:
  l["class"].append(all_a_tags[p].attrs["class"])

print(l)

all_a_tags[57].attrs.keys()
all_a_tags[57]['href']
all_a_tags[57]['class']


## Use this info about HTML elements to grab them
soup.find_all('a', {'class' : "card"})

## There may be tags within tags
sections = soup.find_all('div')
len(sections)
sections[2].a ## FIRST 'a' tag within the 'div' tag
sections[2].find_all('a') ## ALL 'a' tags within the 'div' tag


## Creating a tree of objects
all_fields = soup.find_all('div')
randy = all_fields[31]

randy.find_all("h3")

randy.contents ## Gives a list of all children
randy.children ## Creates an iterator for children

for i, child in enumerate(randy.children):
  print("Child %d: %s" % (i,child))

for sib in randy.next_siblings:
  print(sib)

for sib in randy.previous_siblings:
  print(sib)

randy.parent

# Other methods to check family:
# Beautiful Soup documentation
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/



## Function to save a web page ------------------------------------------------

def download_page(address, filename, wait = 5):
  time.sleep(random.uniform(0,wait))
  page = urllib.request.urlopen(address)
  page_content = page.read()
  if os.path.exists(filename) == False:
    with open(filename, 'wb') as p_html:
      p_html.write(page_content)
  else:
    print("Can't overwrite file " + filename)

download_page('https://polisci.wustl.edu/people/88/', "polisci_ppl.html")

## You can also parse a page that is saved on your computer
## Useful to scrape now, parse later.
with open('polisci_ppl.html') as f:
  myfile = f.read()
  
soup = BeautifulSoup(myfile)
soup.prettify()





#### Using Selenium: An Example

from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
import time

def start_chrome(webpage):
    driver = webdriver.Chrome()
    driver.get(webpage)
    return driver

## Interactive example:

# start the web drivers
driver = start_chrome('https://www.facebook.com')
# find the username element and enter text
username = driver.find_element_by_name('email')
username.send_keys('r.butler@wustl.edu')
# find the password field and enter text
password = driver.find_element_by_name('pass')
password.send_keys('ImNotActuallyShowingYouMyPassword')
# find login button and click
login = driver.find_element_by_id("loginbutton")
login.click()


## Functionalized example (courtesy of Erin Rossiter):
def define_search(driver):
    ## search element changed id randomly, class was the only other info
    ## but 2 elements in this class... we want the 2nd.
    search_elem = driver.find_elements_by_class_name('searchmenu_open')
    search_elem[1].click()

    time.sleep(2)

    keyword_elem = driver.find_element_by_name("query")

    time.sleep(5)

    keyword_elem.send_keys("Shirley Clark")

    time.sleep(2)

    button_elem = driver.find_element_by_xpath("//input[@value='Search']")
    button_elem.click()

    return driver

def get_headlines(driver):
    html_source = driver.page_source
    soup = bs(html_source, "lxml")
    
    gma_tags = soup.find_all("span", {"class" : "headline a"})
    gma_headlines = [tag.get_text() for tag in gma_tags]
    with open("headlines.txt", "w") as f:
        f.writelines("\n".join(gma_headlines))

    driver.quit()

def main(webpage):
    driver = start_chrome(webpage)
    time.sleep(2)
    driver = define_search(driver)
    time.sleep(2)
    get_headlines(driver)

main("http://www.spencerdailyreporter.com/")

## Check here for more help
## https://selenium-python.readthedocs.io/locating-elements.html#locating-by-name


# Copyright (c) 2014 Matt Dickenson
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
