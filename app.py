from flask import Flask, render_template, request
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
    return render_template("index.html")

@app.route("/api/action", methods=["POST"])
def action():
    post_data = request.form.to_dict(flat=False)
    action = post_data.get("select_action", ["chase"])
    colors = post_data.get("select_colors", ["white"])
    print action, colors

    # todo - figure out best way to insert data
    # conn = sqlite3.connect("color_app.db")
    #with conn:
    #    c = conn.cursor()
    #    c.execute("INSERT INTO colors (value) VALUES (?)", (value,))
    #    conn.commit()

    return jsonify({"colors": colors, "action": action})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)