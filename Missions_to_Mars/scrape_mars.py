#!/usr/bin/env python
# coding: utf-8


from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def init_browser():
# Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    # Gets title and first paragraph
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(3)


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('li', class_='slide')[0]



    title_div = results.find("div", class_="content_title")
    news_title = title_div.find('a').text

    news_p = results.find("div", class_="article_teaser_body").text





    # Gets the featured image
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')



    img_results = soup.find("div", class_="header")

    image = img_results.find('img', class_="headerimage")['src']


    featured_img_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/" + image
    

    #-------------------------------------------------
    # Using pandas to grab a table from the website and turns it back to HTML

    url = "https://space-facts.com/mars/"

    tables = pd.read_html(url)
    tables[0]

    mars_df = tables[0]

    mars_df = mars_df.rename(columns={0: "Category", 1: "Data"})

    mars_df 



    html_mars_df = mars_df.to_html(index=False).replace('dataframe', 'table')
    html_mars_df


    # Grabs the Name and High Rez image of each Hemisphere
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    time.sleep(1)

    hem_list = ["Cerberus Hemisphere Enhanced", "Schiaparelli Hemisphere Enhanced", "Syrtis Major Hemisphere Enhanced", "Valles Marineris Hemisphere Enhanced"]

    img_urls = []

    for name in hem_list:

        browser.visit(url)

        time.sleep(1)

        link_name = browser.links.find_by_partial_text(name)
    #     print(link_name.value)
        link_name.click()
        
        #grabs html of current page
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        
        download_area = soup.find('div', class_='downloads')

        list_area = download_area.find('ul')
        
        li  = list_area.find_all('li')[0]
        
        image_url = li.find('a')['href']
    
        img_urls.append(image_url)

    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": img_urls[0]},
    {"title": "Cerberus Hemisphere", "img_url": img_urls[1]},
    {"title": "Schiaparelli Hemisphere", "img_url": img_urls[2]},
    {"title": "Syrtis Major Hemisphere", "img_url": img_urls[3]},
    ]


    mars_dict={
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_img_url,
        "mars_data":html_mars_df,
        "hemisphere_images":hemisphere_image_urls
    }

     # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_dict


if __name__ == "__main__":
    data = scrape()
    print(data)

