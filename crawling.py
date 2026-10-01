import pandas as pd
import MySQLdb
import requests
import json
from bs4 import BeautifulSoup
page = 1 
list = []

while True:
    url = "https://scholarship.dongguk.edu/article/notice/list"+"?pageIndex="+str(page)

    response = requests.get(url)
    soup= BeautifulSoup(response.text, "html.parser")
    pagenation = soup.find("div", {"class": "pagenation"})
    pages = pagenation.find_all("a")
    last_page = int(pages[-1]["href"].replace("/article/notice/list?pageIndex=", ""))
    a= soup.find_all("td", {"class": "td_tit"})
    if  page== last_page+1: break
    for i in a:
        place = i.span.text  
        titlename = i.get_text(" ", strip=True)
        titlename = titlename.replace(place, "", 1).strip()
        urlname= i.a["href"]
        if (urlname== "#none"):
            continue
        dict = {"place": place, "title":titlename, "url": urlname}
        list.append(dict)
    page+=1

with open("DGU.json", "w", encoding="utf-8") as dgu:
    json.dump(list, dgu, ensure_ascii= False, indent=4)
with open("DGU.json", "r", encoding="utf-8") as dgu:
    DGU= json.load(dgu)

conn = MySQLdb.connect(
    user = "crawl_user",
    password = "Test001",
    host = "localhost",
    db = "crawl_data"
)

cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS DGU (Place VARCHAR(500), Title VARCHAR(500), URL VARCHAR(500) UNIQUE)")
sql = "INSERT IGNORE INTO DGU (Place, Title, URL) VALUES (%s, %s, %s)"

for i in DGU:
    cursor.execute(sql, (i["place"], i["title"], i["url"]))

conn.commit()

df = pd.DataFrame(DGU)
df.index= range(1,len(df)+1)
df.to_excel("근로 장학 공지.xlsx")
import os
print(os.path.abspath("근로장학공지.xlsx"))