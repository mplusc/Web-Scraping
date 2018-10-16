
# coding: utf-8

# In[1]:


# Import Libraries
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser


# In[2]:


# Create executable path using Chrome
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# URL of page that will be scraped
news_url = "https://mars.nasa.gov/news/"
browser.visit(news_url)

#Parsing html code using BS
html = browser.html
soup = bs(html, "html.parser")


# In[4]:


#Scarping news title and first paragraph
news_title = soup.find("div",class_="content_title").text
news_paragraph = soup.find("div", class_="article_teaser_body").text

print(f"Title: {news_title}")
print(f"Text: {news_paragraph}")


# In[5]:



img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(img_url)
html = browser.html
soup = bs(html, "lxml")


# In[6]:


img_url = soup.find("img", class_="thumb")["src"]
featured_img_url = "https://www.jpl.nasa.gov" + img_url
print(featured_img_url)


# In[7]:


twitter_url = "https://twitter.com/marswxreport?lang=en"
browser.visit(twitter_url)


# In[8]:


# Parsing html code using BeautifulSoup
html = browser.html
soup = bs(html, 'html.parser')

mars_weather = soup.find('p', class_= 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
print(mars_weather)


# In[9]:


# Mars Facts
mars_facts_url = "http://space-facts.com/mars/"


# In[10]:


#Scrape Mars facts tables using Pandas
mars_facts = pd.read_html(mars_facts_url)
mars_facts[0]


# In[11]:


df = mars_facts[0]
df.columns = ['Characteristics', 'Values']
df.head()


# In[12]:


# Using Pandas to convert the data to HTML table string
mars_html_table = df.to_html()


# Replacing extra '\n' with spaces
mars_html_table.replace('\n', '')

# Save HTML table 
df.to_html('mars_facts_table.html')


# In[13]:


url_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url_hemispheres)
html = browser.html
soup = bs(html, "html.parser")


# In[14]:


# Create a container to hold list of images
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


# In[15]:


url_hemisphere_images

