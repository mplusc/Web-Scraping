
# coding: utf-8

# In[0]:


# Import Libraries
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import splinter
from splinter import Browser

def scrape():
    mars_data = {}
# Create executable path using Chrome
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    
# In[1]:
# URL of page that will be scraped
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, "html.parser")
    news_title = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
        
    mars_data["news_title"] = news_title
    mars_data["news_summary"] = news_paragraph
# In[5]:

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = bs(html, "lxml")
    image_src = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image_url

    mars_data["featured_src"] = image_src
    mars_data["featured_image"] = featured_image_url


# In[7]:

    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather = soup.find('p', class_= 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    mars_data["weather"] = mars_weather.strip()


# In[9]:

    mars_facts_url = "http://space-facts.com/mars/"
    mars_facts = pd.read_html(mars_facts_url)
    mars_facts[0]
    df = mars_facts[0]
    df.columns = ['Characteristics', 'Values']
    df.head()
    mars_html_table = df.to_html()
    mars_html_table.replace('\n', '')
    df.to_html('mars_facts_table.html')

    mars_data["facts"] = df
# In[13]:

    url_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemispheres)
    html = browser.html
    soup = bs(html, "html.parser")
    url_hemisphere_images = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + link    
        browser.visit(image_link)
        html = browser.html
        soup= bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        url_hemisphere_images.append({"title": title, "img_url": image_url})
        
    mars_data["hemispheres"]= url_hemisphere_images    
    browser.quit()
    
    return mars_data

