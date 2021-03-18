#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
import bs4
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time


# ## NASA Mars News
#   * Scrape the NASA Mars News Site and collect the **latest** News Title and Paragraph Text. Assign the text to variables that you can reference later.



def scrape_info():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(3)


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    news_title = soup.find_all("div", class_="content_title")[1].text

    news_description = soup.find("div", class_='article_teaser_body').text

    soup.find_all("div", class_="content_title")[1].find("a")["href"]

    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    image = soup.find("a", class_="fancybox-thumbs")["href"]


    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'+image

    url = 'https://space-facts.com/mars/'
    all_tables = pd.read_html(url)
    all_tables


    mars_facts_table = all_tables[0]
    mars_facts_table.columns = ["Description", "Value"]
    mars_facts_table

    table_html = mars_facts_table.to_html()

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(3)


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    all_hemispheres = soup.find('div', class_='collapsible results')
    hemispheres = all_hemispheres.find_all('div', class_='item')

    starting_url = 'https://astrogeology.usgs.gov'

    hemisphere_image_urls = []

    for result in hemispheres:
        hemisphere = result.find('div', class_="description")
        title = hemisphere.h3.text
        
        ending_url = hemisphere.a["href"]    
        browser.visit(starting_url + ending_url)
        time.sleep(3)
        
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')
        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']
        
        hemisphere_dict = {}
        hemisphere_dict['title'] = title
        hemisphere_dict['img_url'] = image_url
        
        hemisphere_image_urls.append(hemisphere_dict)

    hemisphere_image_urls

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_description": news_description,
        "featured_image_url": featured_image_url,
        "table_html": table_html,
        "hemisphere_image_urls" : hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
