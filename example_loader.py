import sqlite3, time

conn = sqlite3.connect("color_app.db")

while True:
    with conn:
        c = conn.cursor()
        c.execute(
            "SELECT * FROM actions WHERE processed = 0 ORDER BY added ASC LIMIT 1;"
        )
        result = c.fetchone()
        if result:
            print "new record: ", result
            c.execute("UPDATE actions SET processing = 1 WHERE id = ?", (result[0],))
            conn.commit()
            print "processing..."
            time.sleep(10)
            c.execute(
                "UPDATE actions SET processing = 0, processed = 1 WHERE id = ?",
                (result[0],)
            )
            conn.commit()
        else:
            # revert to default here
            print "nothing found...waiting"
            time.sleep(10)