from itertools import cycle
import requests
from proxyService import getProxies

proxies = getProxies()

def get(url):
    
    for proxy in proxies:
        print("Request using proxy " +  proxy)
    
        try:
            response = requests.get(url, proxies={"http": proxy, "https": proxy})
            return response
    
        except:
            print("Couln't connect to: " + proxy)
            
        
        