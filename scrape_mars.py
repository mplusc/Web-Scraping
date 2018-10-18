
# coding: utf-8

# Import Libraries
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser



# URL of page that will be scraped
def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)  
   
    mars = {}
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, "html.parser")
    news_title = soup.find("div", class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
        
    mars["news_title"]= news_title
    mars["news_paragraph"]= news_paragraph
   



    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    html = browser.html
    soup = bs(html, "lxml")
    img_src = soup.find("img", class_="thumb")["src"]
    featured_img_url = "https://www.jpl.nasa.gov" + img_url
    
    mars["featured_src"] = img_src
    mars["featured_image"] = featured_img_url




    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_weather = soup.find('p', class_= "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    
    mars["weather"] = mars_weather.strip()
    



    mars_facts_url = "http://space-facts.com/mars/"
    mars_facts = pd.read_html(mars_facts_url)
    mars_facts[0]
    df = mars_facts[0]
    df.columns = ["Characteristics", "Values"]
    df.head()

    # Using Pandas to convert the data to HTML table string
    mars_html_table = df.to_html()

    # Replacing extra '\n' with spaces
    mars_html_table.replace('\n', '')

    # Save HTML table 
    #df.to_html('mars_facts_table.html')
    mars["facts"] = df


    url_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemispheres)
    html = browser.html
    soup = bs(html, "html.parser")

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

    mars["hemispheres"]= url_hemisphere_images    
    browser.quit()     

    return mars


