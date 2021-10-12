#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape():
    # Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # create dictionary for scraped data
    scraped_data = {}

    # nasa new from redplanetscience.com
    url = "https://redplanetscience.com/"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    news_title = soup.find('div', class_='content_title').getText()
    news_p = soup.find('div',class_='article_teaser_body').getText()
    
    scraped_data['news_title'] = news_title
    scraped_data['news_p'] = news_p

    # JPL Mars Space Images - Featured Image
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    featured_image = soup.find('img', class_='fancybox-image')
    image_path = featured_image['src']
    featured_image_URL = url + image_path
    scraped_data['featured_image']=featured_image_URL
 

    # Mars Facts
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)
    time.sleep(1)
    tables = pd.read_html(url)
    df = tables[1]
    html_table = df.to_html(index= False,header=None,classes="table table-striped table-hover")
    html_table.replace('\n', '')
    scraped_data["mars_facts"] = html_table

    # Mars Hemispheres
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    image_links = soup.find_all('div', class_='item')

    link_list=[]
    
    #append the href to url
    for link in image_links:
        a = link.find('a')
        href=a['href']
        link_list.append(url+href)
    
    hemisphere_image_urls = []
    dict1 = {}

    for x in range(len(link_list)):
        url = link_list[x]
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h2', class_='title').getText()                         
        image_url = soup.find('img', class_='wide-image')
        complete_url="https://marshemispheres.com/"+image_url['src'] 

        dict1["title"]= title
        dict1["img_url"]= complete_url

        hemisphere_image_urls.append(dict1.copy())

    scraped_data["mars_hemispheres"] = hemisphere_image_urls
    browser.quit()

    return scraped_data