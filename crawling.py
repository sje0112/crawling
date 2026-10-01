import MySQLdb
import requests
import json
from bs4 import BeautifulSoup
url = "https://scholarship.dongguk.edu/article/notice/list"
response = requests.get(url)
soup= BeautifulSoup(response.text, "html.parser")

a= soup.find_all("td", {"class": "td_tit"})
list = []
for i in a:
    place = i.span.text  
    titlename = i.get_text(" ", strip=True)
    titlename = titlename.replace(place, "", 1).strip()
    urlname= i.a["href"]
    if (urlname== "#none"):
        continue
    dict = {"place": place, "title":titlename, "url": urlname}
    list.append(dict)
with open("DGU.json", "w", encoding="utf-8") as file:
    json.dump(dict, file, ensure_ascii= False, indent=4)

conn = MySQLdb.connect(
    user = "crawl_user",
    password = "Test001",
    host = "localhost",
    db = "crawl_data"
)
print(type(conn))
cursor = conn.cursor()
print(type(cursor))
cursor.execute("DROP TABLE IF EXISTS DGU")
cursor.execute("CREATE TABLE DGU (title text, url text)")

cursor.execute( f'INSERT INTO DGU VALUES("{titlename}","{urlname}")')
conn.commit()


