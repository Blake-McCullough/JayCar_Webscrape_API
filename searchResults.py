# import library
from bs4 import BeautifulSoup
import requests
import json
base_url='https://www.jaycar.com.au/'
import math
#Get search results of items.
def searchResults(searchkey,page):
  
  url = base_url + "search?q=" + searchkey.replace("%20","+") + "&page=" + page
  print(url)
  req=requests.get(url)
  #Makes sure was successful.
  if req.status_code == 200:
    
    #Get info into beautiful soup.
    content=req.text
    soup=BeautifulSoup(content,features="html.parser")
    data = []
    
    #Getting item count.
    item_count = 0
    page_count = 1
    #Gets max page count, and item count.
    try:
      count = soup.find("div",{"class":"totalResults"}).text
      if count != None:
        
        item_count = int(count.partition(' ')[0].replace(",",""))
        if item_count > 20:
          page_count = (math.ceil(item_count/20))
    except:
      pass
      
    for x in soup.find_all("div", {"class": "productListItem"}):

      #Prepare Items Array.
      item = {}

      #Getting what product is.
      item['makerHub'] = False
      item['clearance'] = False
      item['discontinued'] = False
      item['specialOrder'] = False
      for z in x.find_all("div",{"class":"ps_nowonsale makerColor"}):
        item['makerHub'] = True
      for z in x.find_all("div",{"class":"ps_nowonsale storeOnlyColor"}):
        item['clearance'] = True
      for z in x.find_all("div",{"class":"ps_nowonsale purplecolor"}):
        item['discontinued'] = True
      for z in x.find_all("div",{"class":"ps_nowonsale specialOrder"}):
        item['specialOrder'] = True



      #Getting Title.
      item["Title"] = x.find("div", {"class": "head search_listing_item_title"}).text
      
      #Getting Item Code.
      item["Code"] = x.find("div",{"class":"mobile-prcode"}).findChildren("b" , recursive=False)[0].text
      
      #Getting Image.
      img= x.find('img')
      if img.has_attr('data-original'):
    
        item["ImageURL"] = img['data-original']
      else:
        item["ImageURL"] = "https://www.jaycar.com.au/_ui/responsive/theme-jaycar_rebrand/images/missing-product-300x300.jpg"
      item["Price"] = "$" + x.find("div",{"class":"price"}).text.partition("\n\t\t\t\t\t\t$")[2]
      data.append(item)
   #Returns json of info.
    return {"results":data,"item_count":item_count,"total_page_count":page_count}
            
  else:
    return "Null"


