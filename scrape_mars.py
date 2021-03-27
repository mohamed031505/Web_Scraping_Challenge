from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    
    browser = init_browser()
    # Setup NASA-MARS NEWS URL
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(3)
    # Scraping News Title and Teaser
    nasa_html = browser.html
    soup = BeautifulSoup(nasa_html, 'html.parser')
    news_results = soup.find('div', class_="list_text")
    news_title = news_results.find('div', class_="content_title").text       
    news_teaser = news_results.find('div', class_="article_teaser_body").text
    # SETUP JPL MARS SPACE URL 
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html' 
    browser.visit(url)
    time.sleep(3)
    # JPL Mars Space Images - Featured Image Scrape
    browser.links.find_by_partial_text('FULL IMAGE').click()
    time.sleep(3)
    jpl_html = browser.html
    soup = BeautifulSoup(jpl_html, 'html.parser')
    jpl_image = soup.find_all('img')[1]['src']
    # print(jpl_image)
    featured_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{jpl_image}'
    # print(featured_image_url)
    #Mars Facts
    url = 'https://space-facts.com/mars/'
    df = pd.read_html(url)
    mars_facts_df = df[0]
    mars_facts_df.columns = ["Description", "Information"]
    mars_facts_table = mars_facts_df.to_html()
    # mars_facts_df.to_html("table.html")
    # print(mars_facts_table)
    # Setup Hemispheres URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    #Mars Hemispheres Scrape

    hemisphere_image_urls_dic ={'title':[],
                                'img_url':[]
                            }
    # mars_data_dic = {
    #     "news_title" : news_title,
    #     "news_teaser" : news_teaser,
    #     "mars_facts" : mars_facts_table ,
    #     "featured_image_url" : featured_image_url,
    #     "hemisphere_image" : hemisphere_image_urls_dic
    #     }
    for i in range(4):  
        
        browser.links.find_by_partial_text('Hemisphere Enhanced')[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        image_link = soup.find_all('div',class_='downloads')
        img = image_link[0].find_all('a')
        img_url = img[0]['href']
        title = soup.find_all('div', class_='content')
        title = title[0].find('h2').text
    #     print(title)
    #     print(img_url) 
        hemisphere_image_urls_dic['title'].append(title)
        hemisphere_image_urls_dic['img_url'].append(img_url)
        
        browser.back()
    # mars_data_dic['hemisphere_image'] = hemisphere_image_urls_dic

        
    mars_data_dic ={"news_title" : news_title,
                    "news_teaser" : news_teaser,
                    "mars_facts" : mars_facts_table ,
                    "featured_image_url" : featured_image_url,
                    "hemisphere_image" : hemisphere_image_urls_dic
                    }

    print(mars_data_dic)

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data_dic
