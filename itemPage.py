# import library
from bs4 import BeautifulSoup
import requests
import json

base_url='https://www.jaycar.com.au/'


#The page for the Item.
def itemPage(item_code):
  url = base_url + "p/" + item_code

  req=requests.get(url)
  #Makes sure was successful.
  if req.status_code == 200:
    
    #Get info into beautiful soup.
    content=req.text
    soup=BeautifulSoup(content,features="html.parser")
    item = {}
    
    item["Title"] = soup.find("h1",{"class":"productName"}).text
    
    #Getting Image.
    item["Image"] = base_url + soup.find("div",{"class":"productImagePrimary"}).findChildren("img" , recursive=False)[0]["src"] or "https://www.jaycar.com.au/_ui/responsive/theme-jaycar_rebrand/images/missing-product-300x300.jpg"

    #Getting base price.
    item["Price"] = soup.find("div", {"class":"priceContainer"}).findChildren("span" , recursive=False)[0].text.partition('$')[2]
  #Getting what product is.
    item['makerHub'] = False
    item['clearance'] = False
    item['discontinued'] = False
    item['specialOrder'] = False
    for z in soup.find_all("div",{"class":"ps_nowonsale makerColor"}):
      item['makerHub'] = True
    for z in soup.find_all("div",{"class":"ps_nowonsale storeOnlyColor"}):
      item['clearance'] = True
    for z in soup.find_all("div",{"class":"ps_nowonsale purplecolor"}):
      item['discontinued'] = True
    for z in soup.find_all("div",{"class":"ps_nowonsale specialOrder"}):
      item['specialOrder'] = True
    #Gets the bulk buying price breaks.
    price_breaks = []
    for x in soup.find("table",{"class":"volume-prices"}).findChildren("tr" , recursive=True):
      count = {}
      count["VolumePriceQuantity"] = x.find("td",{"class":"volume-price-quantity"}).text.partition('									')[2].partition('\n\t\t\t\t\t\t\t\t\t\t')[0]
      count["VolumePriceAmount"] = x.find("td",{"class":"volume-price-amount"}).text
      price_breaks.append(count)
      
    item["PriceBreaks"] = price_breaks

    #Gets the summary.
    item["Summary"] = soup.find("div",{"class":"summary"}).text.replace("\n        ","").replace("• ","\n")
    
    #Gets description.
    item["Description"] = soup.find("div",{"class":"tabBody"}).text.replace("\n\t\t","").replace("\n\t\n\t\n\t\n\t","").replace("\n\t\n\t\xa0","\n").replace("\n\t\n\t","").replace("\n\n"," ").replace("\r","")

    #Gets specification.
    specifications = []
    itemsSearch = soup.find_all("table",{"class":"specifications"})
    x= 0
    titles = soup.find_all("div",{"class":"headline"})
    for itemed in itemsSearch:
      

      items = itemed.find("tbody",recursive=False).findChildren("tr",recursive=True)
      
      blocks = []
      for y in items:
        
        rows = {}
        
        stuff = y.find_all("td")
        print(stuff)
        
        if y.find("span", {"class": "noTick"}) is not None:
          rows["Value"] = 'noTick'
        elif y.find("span",{"class":"yesTick"}) is not None:
          rows["Value"] = 'yesTick'
        else:
          rows["Value"] = stuff[1].text.replace("\n            \t\t","")
        rows["Title"] = stuff[0].text.replace("\n   \t\t\t\t\t ","").replace("\n\t\t\t\t","").replace("\n   \t\t\t\t\t","")
        
        
        blocks.append(rows)
      specifications.append({"Title":titles[x].text,"Data":blocks})
      x = x + 1
    item["Specifications"] = specifications

    #Returns JSON format.

    return item
  else:
    #Returns no info if empty.
    return []