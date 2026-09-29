import MySQLdb

conn = MySQLdb.connect(
    user = "crawl_user",
    password = "Test001",
    host = "localhost",
    db = "crawl_data"
)
print(type(conn))
cursor = conn.cursor()
print(type(cursor))
cursor.execute("CREATE TABLE Title (title text, url text)")
conn.commit()

