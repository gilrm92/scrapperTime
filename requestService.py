from itertools import cycle
import threading
import requests
import random
import concurrent.futures
from dbManager import getProxies

def refreshProxies() :
    threading.Timer(60.0, refreshProxies).start()
    global proxies 
    proxies = list(getProxies())

refreshProxies()

def requestUrl(url, proxy):
    try:
        #print("requesting with proxy " + proxy["ip"])
        response = requests.get(url, timeout=10, proxies={"http": proxy["ip"], "https": proxy["ip"]})
        return response

    except:
        #print("failed proxy " + proxy["ip"])
        pass

def get(url):
    data = None
    while data is None:
        random.shuffle(proxies)
        with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:    
            future_request = {executor.submit(requestUrl, url, proxy): proxy for proxy in proxies}

            for future in concurrent.futures.as_completed(future_request):
                request = future_request[future]
            try:
                data = future.result()
                if data is not None:
                    if "nav-logo" in data.text:
                        return data.text
                    else:
                        raise Exception("website blocked IP")    
                else :
                    raise Exception("website returned none")    
            except Exception as exc:
                print('%r generated an exception: %s' % (request, exc))        