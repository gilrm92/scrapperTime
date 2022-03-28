from item import Item
from bs4 import BeautifulSoup
import requestService
import dbManager
import concurrent.futures

def GetDescription(url) :
    productHtml = requestService.get(url)
    if productHtml is None :
        return ""
    
    productPage = BeautifulSoup(productHtml)
    description = productPage.find("p", attrs={"class" : "ui-pdp-description__content"})
    if description is None :
        return ""
    
    return description.text

def scrapCategory(category):
    print("starting category " + category["href"])
    categoryUrl = category["href"]
    categoryHtml = requestService.get(categoryUrl)

    if categoryHtml is None :
        return
    
    pageCounter = 1
    categorySoup = BeautifulSoup(categoryHtml)
    while categorySoup.find("a", attrs={"class": "andes-pagination__link ui-search-link", "title":"Seguinte"}) is not None:
        print("starting item page number " + str(pageCounter))
        items = categorySoup.find_all(attrs={"class" : "ui-search-result__wrapper"})
        nextLink = categorySoup.find("a", attrs={"class": "andes-pagination__link ui-search-link", "title":"Seguinte"})
        for item in items:
            url = item.find(attrs={"class" : "ui-search-link"})["href"]
            if not dbManager.existsInDb(url) :
                
                name = item.find(attrs={"class" : "ui-search-link"})["title"]
                description = GetDescription(url)
                priceDiv = item.find("div", attrs={"class" : "ui-search-price__second-line"})
                price = priceDiv.find(attrs={"class":"price-tag-fraction"}).text
                currency = priceDiv.find(attrs={"class":"price-tag-symbol"}).text
                websiteOrigin = "Mercado Livre"
                newItem = Item(name, description, price, currency, websiteOrigin, url)
                print("new item " + name + " created")
                dbManager.saveItem(newItem)
            else:
                print("item already exists " + url)
        pageCounter += 1
        categoryHtml = requestService.get(nextLink["href"])
        categorySoup = BeautifulSoup(categoryHtml)

## Start execution ##
print("trying to get categories page")
htmlPage = requestService.get("https://www.mercadolivre.com.br/categorias#menu=categories")
soup = BeautifulSoup(htmlPage)
categories = soup.find_all("a", attrs={"class" : "categories__subtitle"})
allItems = []

with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    future_request = {executor.submit(scrapCategory, category): category for category in categories}
    
                   
        
    
    

