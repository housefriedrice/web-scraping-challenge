from splinter import Browser
import pandas as pd
from bs4 import BeautifulSoup

def scrape():
    executable_path ={'executable_path':'/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    soup = BeautifulSoup(browser.html)
    list = soup.find_all('li', class_='slide')
    data1 = []
    for li in list:
        h = li.find('div', class_="content_title").find('a').contents[0]
        p = li.find('div', class_="article_teaser_body").contents[0]
        data1.append({'headline':h, 'paragraph':p})

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    soup = BeautifulSoup(browser.html)
    foot = soup.find('footer')
    link = foot.find('a')['data-fancybox-href']
    featured_image_url = 'https://jpl.nasa.gov' + link

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    soup = BeautifulSoup(browser.html)
    tweet = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').contents[0]
    
    table = pd.read_html('https://space-facts.com/mars/')[0]
    tableHTML = table.to_html()

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    soup = BeautifulSoup(browser.html)
    descriptions = soup.find_all('div', class_='description')
    images_list = []
    for desc in descriptions:
        browser.visit(url)
        soup = BeautifulSoup(browser.html)
        text = desc.find('h3').contents[0]
        browser.click_link_by_partial_text(text)
        soup = BeautifulSoup(browser.html)
        img_url = soup.find('li').find('a')['href']
        images_list.append({'title':text, 'img_url':img_url})
    dict = {
        'nasa_news': data1,
        'featured_image_url': featured_image_url,
        'weather': tweet,
        'mars_facts': tableHTML,
        'images': images_list
    }
    return dict