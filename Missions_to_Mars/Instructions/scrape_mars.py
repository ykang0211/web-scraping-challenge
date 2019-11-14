from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup



def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars={}

    # title and paragraph
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)



    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    mars["news"] = soup.find('ul', class_='item_list')
    mars["news_title"] = news.h3.text
    mars["news_p"] = news.find('div', class_="article_teaser_body").text

    # JPL Mars Space Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

 

    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    mars["image"] = soup.article.figure.a['href'] 
    featured_image_url = 'https://www.jpl.nasa.gov/' + image
    mars["src"] = featured_image_url

    # Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)


  
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    mars["mars_weather"] = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text


    # Mars Facts
    url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(url)

    mars_facts_df = mars_facts[0]
    mars_facts_df.columns = ['description', 'value']
    mars_facts_df.set_index('description', inplace=True)
    mars_facts_df
    mars["html_table"] = mars_facts_df.to_html(header=False, index=False)


    # Mars Hemisphere
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)



    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    hemisphere_image_urls = []
    products = soup.h3.text
    products = soup.find('div', class_='collapsible results')
    hemispheres = products.find_all('div', class_='item')   
    products = soup.find('div', class_='collapsible results')
    hemi = products.find_all('div', class_='item')                        

    for hemi in hemi:                                               
        title = hemi.find('div', class_='description')
        
        title_text = title.a.text                                               
        title_text = title_text.replace(' Enhanced', '')
        browser.click_link_by_partial_text(title_text)                          
        
        html = browser.html                                             
        soup = BeautifulSoup(html, 'lxml')                               
        
        image = soup.find('div', class_='downloads').find('ul').find('li') 
        img_url = image.a['href']
        
        hemisphere_image_urls.append({'title': title_text, 'img_url': img_url})


        src_h = hemisphere_image_urls
        mars['src_h'] = src_h

    # mars = {
    #     'news_title': news_title,
    #     'news_p': news_p,
    #     'src': featured_image_url,
    #     'mars_weather': mars_weather,
    #     'html_table': html_table,
    #     'hemisphere_image_urls': hemisphere_image_urls
    # }
    browser.quit()

    return mars