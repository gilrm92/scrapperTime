from pymongo import MongoClient
from item import Item

CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING)
scrapperItemsDb = client["scrapperItems"]
scrapperProxiesDb = client["scrapperProxies"]
itemCollection = scrapperItemsDb["item"]
proxiesCollection = scrapperProxiesDb["proxies"]
    
def saveItem(item) :
    try :
        itemCollection.insert_one(item.__dict__)
        
    except Exception as ex :
        print("error when adding. ex: %s" % (ex))
        
def existsInDb(url) :
    try :
        item = itemCollection.find_one({"url": url}, {"_id"})
        return item is not None;
            
    except Exception as ex :
        print("error when finding. ex: %s" % (ex))
        
def getProxies() :
    try :
        proxies = proxiesCollection.find({})
        return proxies
    
    except Exception as ex : 
        print("error when finding. ex: %s" % (ex))