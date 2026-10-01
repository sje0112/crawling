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


