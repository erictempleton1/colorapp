import sqlite3, time

conn = sqlite3.connect("color_app.db")
c = conn.cursor()

while True:
    c.execute(
        "SELECT * FROM actions WHERE processed = 0 ORDER BY added ASC LIMIT 1;"
    )
    results = c.fetchone()
    if results:
        print "new record: ", results
        print "processing..."
        time.sleep(10)
    else:
        print "nothing found...waiting"
        time.sleep(10)