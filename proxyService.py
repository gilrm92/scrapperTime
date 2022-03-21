from lxml.html import fromstring 
 
 
def getProxies():
    file = open("proxy-filtered-list.txt")
    proxies = set() 
    for line in file:
        proxies.add(line.replace("\n", ""))
            
    return proxies