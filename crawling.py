import MySQLdb
import requests
from bs4 import BeautifulSoup
url = "https://scholarship.dongguk.edu/article/notice/list"
response = requests.get(url)
soup= BeautifulSoup(response.text, "html.parser")

a= soup.find_all("td", {"class": "td_tit"})
for i in a:
    print(i.text)
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

titlename= "[법무대학원 학사운영실] 주말 국가근로장학생 모집(~10/2 17시까지)(지원마감, 선발중)"
urlname = "https://scholarship.dongguk.edu/article/notice/detail/215142?pageIndex=1&"
cursor.execute( f'INSERT INTO DGU VALUES("{titlename}","{urlname}")')
conn.commit()


