>>> from scrapy.item import Item, Field
>>> from items import LivingSocialDeal
>>> deal = LivingSocialDeal(title="$20 off yoga classes", price="50")
>>> print deal
LivingSocialDeal(title='$20 off yoga classes', price='50')
>>> deal['title']
'XXXXXXXXXXXXXXXXXXXX'
>>> deal.get('title')
'XXXXXXXXXXXXXXXXXXXX'
>>> deal['price']
'50'
>>> deal['location'] = "New York"
>>> deal['location']
'New York'
