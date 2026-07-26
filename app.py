from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DB = "baccarat.db"


def init_db():
    con = sqlite3.connect(DB)
    con.execute("""
    CREATE TABLE IF NOT EXISTS records(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        result TEXT
    )
    """)
    con.commit()
    con.close()


def get_history():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT result FROM records ORDER BY id")
    data = [x[0] for x in cur.fetchall()]
    con.close()
    return data


def analyze():

    history = get_history()

    last20 = history[-20:]

    b = last20.count("B")
    p = last20.count("P")

    if b > p:
        msg = "庄方向较强"
    elif p > b:
        msg = "闲方向较强"
    else:
        msg = "走势平衡"

    return {
        "记录": last20,
        "分析": msg,
        "庄": b,
        "闲": p
    }


@app.route("/")
def index():
    return render_template(
        "index.html",
        data=analyze()
    )


@app.route("/add", methods=["POST"])
def add():

    result = request.json["result"]

    con = sqlite3.connect(DB)

    con.execute(
        "INSERT INTO records(result) VALUES(?)",
        (result,)
    )

    con.commit()
    con.close()

    return jsonify(analyze())


if __name__ == "__main__":
    init_db()
    app.run()
