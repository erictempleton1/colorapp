from flask import Flask
from flask.json import jsonify
import sqlite3
app = Flask(__name__)


@app.route("/api/status", methods=["GET"])
def status():
    conn = sqlite3.connect("color_app.db")
    with conn:
        c = conn.cursor()
        c.execute("SELECT value FROM colors WHERE selected = ?", (1,))
        status = c.fetchone()
        if status:
            return jsonify({"status": status[0]})
    return jsonify({"status": []})

@app.route("/", methods=["GET"])
def index():
    conn = sqlite3.connect("color_app.db")
    with conn:
        c = conn.cursor()
        c.execute("SELECT * FROM colors")
        results = c.fetchall()
    return jsonify({"results": results})

@app.route("/api/action/<string:value>", methods=["POST"])
def action(value):
    conn = sqlite3.connect("color_app.db")
    with conn:
        c = conn.cursor()
        c.execute("INSERT INTO colors (value) VALUES (?)", (value,))
        conn.commit()
    return "hello"  # todo - return something else here!

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)