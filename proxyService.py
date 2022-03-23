from lxml.html import fromstring 
 
 
def getProxies():
    file = open("proxy-list.txt")
    proxies = []
    for line in file:
        proxies.append(line.replace("\n", ""))
            
    return proxies