from datetime import datetime


class Item:
    def __init__(self, name, description, price, currency, websiteOrigin, url):
        self.name = name
        self.description = description
        self.price = price
        self.currency = currency
        self.websiteOrigin = websiteOrigin
        self.url = url
        self.dataInserted = datetime.now()
        self.dataUpdated = None