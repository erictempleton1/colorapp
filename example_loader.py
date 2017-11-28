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
        # todo - update record to processing here
        print "processing..."
        time.sleep(10)
        # todo - update record to processed here
    else:
        # revert to default here
        print "nothing found...waiting"
        time.sleep(10)