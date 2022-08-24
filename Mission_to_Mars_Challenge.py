#!/usr/bin/env python
# coding: utf-8

# ### CHALLENGE CODE

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# html parser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### JPL Space Images Featured Image

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
hemisphere_soup = soup(html, 'html.parser')

# Get the links for each of the 4 hemispheres
hemisphere_links = hemi_soup.find_all('h3')

# loop through each hemisphere link
for hemi in hemisphere_links:
    # Navigate and click the link of the hemisphere
    img_page = browser.find_by_text(hemi.text)
    img_page.click()
    html= browser.html
    img_soup = soup(html, 'html.parser')
    # Scrape the image link
    img_url = 'https://astrogeology.usgs.gov/' + str(img_soup.find('img', class_='wide-image')['src'])
    # Scrape the title
    title = img_soup.find('h2', class_='title').text
    # Define and append to the dictionary
    hemisphere_dict = {'img_url': img_url,'title': title}
    hemisphere_image_urls.append(hemisphere_dict)
    browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()

