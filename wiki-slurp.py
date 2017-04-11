#!/usr/bin/env python2.7

# Wiki-Slurp by Shane Ryan

import os
import requests
import multiprocessing
from lxml import html


BASE = 'https://commons.wikimedia.org' # common denominator of needed URLs
URL  = BASE + '/wiki/Commons:Picture_of_the_Year/'    # contains galleries from 2006+
XPATH_GALLERY = '//li[@class]//a[contains(@href,"File")]/@href'
XPATH_IMAGE = '//div[a="Original file"]/a[@href]/@href'

#TODO: use flags or interactive prompt to list the categories within galleries
# For example, list 2016 genres, categories, etc., or find every photo from a
# certain genre or category that made it to round 2 or was featured during a
# certain month.
# Also, download the caption for each photo and save in an accompanying text
# file to be displayed as part of the image's use for a desktop background

'''
wget acts as a pythonic version of the traditional unix 'wget' function
just pass it a URL and getit!!
doesn't return anything, just writes to file, enabling functional programming
(although i should add something to handle exceptions on file not found, etc.)
'''
def wget(url):
    p = os.path.basename(url)   # automatically name the downloaded files
    r = requests.get(url)
    print 'Downloading', url
    with open('Pictures/' + p, 'wb') as f:
        f.write(r.content)

'''
this function takes the url to an images File page on wikipedia commons and
retrieves the upload link to the full-size, original file
'''
def get_original_image_URL(url):
    image_page_response = requests.get(url)
    image_tree = html.fromstring(image_page_response.content)
    return image_tree.xpath(XPATH_IMAGE)[0]


'''
the following block of code is able to scrape the image page URLs from a
desired year / gallery listing.
'''
pool = multiprocessing.Pool(4)

gallery_page_response = requests.get(URL + '2016/R2/Gallery')
tree = html.fromstring(gallery_page_response.content)
print 'Scraping image pages from gallery...'
images = [BASE + asset for asset in tree.xpath(XPATH_GALLERY)]
print 'Obtaining original image links...'
original_images = [get_original_image_URL(item) for item in images]

pool.map(wget, original_images)
#map(wget, original_images)




