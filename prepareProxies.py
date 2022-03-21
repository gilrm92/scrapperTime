from socket import timeout
import requests
import threading
import concurrent.futures

lock = threading.Lock()

def prepareProxyList(line, w):
    try:
        response = requests.get("https://www.google.com",timeout=5, proxies={"http": line.replace("\n", ""), "https": line.replace("\n", "")})
        print("connected to " + line)
        lock.acquire();
        w.write(line)
        lock.release();
    except:
        print("Couln't connect to: " + line.replace("\n", ""))

f = open("proxy-list.txt")
with open("proxy-filtered-list.txt",'w',encoding='utf-8') as w:
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
     for line in f:
        print("running for " + line)
        future = executor.submit(prepareProxyList, line, w)
        
        while future.running():
            pass
        
print("done")