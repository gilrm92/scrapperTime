from item import Item
from bs4 import BeautifulSoup
import requests


def GetDescription(url) :
    productHtml = requests.get(url).text
    productPage = BeautifulSoup(productHtml)
    return productPage.find("p", attrs={"class" : "ui-pdp-description__content"}).text

htmlPage = requests.get("https://www.mercadolivre.com.br/categorias#menu=categories").text
soup = BeautifulSoup(htmlPage)
categories = soup.find_all(attrs={"itemprop" : "url"})
allItems = []

for category in categories:
    print("starting category " + category["href"])
    categoryUrl = category["href"]
    categoryHtml = requests.get(categoryUrl).text
    categorySoup = BeautifulSoup(categoryHtml)
    items = categorySoup.find_all(attrs={"class" : "ui-search-result__wrapper"})
    for item in items:
        
        name = item.find(attrs={"class" : "ui-search-link"})["title"]
        url = item.find(attrs={"class" : "ui-search-link"})["href"]
        description = GetDescription(url)
        priceDiv = item.find("div", attrs={"class" : "ui-search-price__second-line"})
        price = priceDiv.find(attrs={"class":"price-tag-fraction"}).text
        currency = priceDiv.find(attrs={"class":"price-tag-symbol"}).text
        websiteOrigin = "Mercado Livre"
        
        newItem = Item(name, description, price, currency, websiteOrigin, url)
        print("new item " + name + " created")    
        allItems.append(newItem)

print(allItems)
        
    
    

