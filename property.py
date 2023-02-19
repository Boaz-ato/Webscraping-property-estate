import requests
from bs4 import BeautifulSoup
import pandas as pd
import math

r=requests.get("https://www.century21.com/real-estate/new-york-ny/LCNYNEWYORK/?",headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c=r.content
soup=BeautifulSoup(c,"html.parser")
pages=soup.find_all("div",{"class":"results-label"})[0].text
pages=int((pages.replace("New York Homes for Sale","")).replace("\n","").replace("(","").replace(")","").replace(",",""))
pages=math.ceil(pages/100)
property=[]


url="https://www.century21.com/real-estate/new-york-ny/LCNYNEWYORK/?p="

   
for page in range(0,pages+1):
    
    r=requests.get(url+str(page),headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    
    all=soup.find_all("div",{"class":"property-card-primary-info"})
    for info in all:
        df={}
        try:
            sale=info.find("div", {"class":"pdp-listing-type sale"}).text
            df["Listing type"]=sale
        except:
            df["Listing type"]="Not available"
        try:
            price=info.find("a",{"class":"listing-price"}).text
            price=price.replace(" ","").replace("\n","")
            df["Price"]=price
        except:
            df["Price"]="Not available"
        try:
            bed=info.find_all("div",{"class":"property-beds"})[0].text
            bed=bed.replace(" ","").replace("\n","")
            if len(bed)==4:
                bed=bed.replace("bed","")
            else:
                bed=bed.replace("beds","")
            df["Beds"]=bed
        except:
            df["Beds"]="None"
        try:
            bath=info.find_all("div",{"class":"property-baths"})[0].text
            bath=bath.replace(" ","").replace("\n","")
            if len(bath)==5:
                bath=bath.replace("bath","")
            else:
                bath=bath.replace("baths","")
            df["Baths"]=bath
        except:
            df["Baths"]="None"
        try:
            area=info.find_all("div",{"class":"property-sqft"})[0].text
            area=area.replace(" ","").replace("sq","").replace(".","").replace("ft","").replace(",","").replace("\n","")
            df["Square feet"]=area
        except:
            df["Square feet"]="Not available"
        try:
            address=info.find_all("div",{"class":"property-address"})[0].text
            address=address.replace("\n ","").replace("  ","")
            df["address"]=address
        except:
            df["address"]="Not available"
        try:
            city=info.find_all("div",{"class":"property-city"})[0].text
            city=city.replace("\n ","").replace("  ","")
            df["City"]=city
        except:
            df["City"]="Not available"
        property.append(df)


properties=pd.DataFrame(property)
properties.to_excel("Property_Estate.xlsx")
        
        
        
        
        
        
        