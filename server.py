import sqlite3
from collections import defaultdict
from pathlib import Path

from fastapi import FastAPI

app = FastAPI()

prefix = ""


def init_db():
    if not Path("data.db").exists():
        with sqlite3.connect("data.db", check_same_thread=False) as connection:
            cursor = connection.cursor()
            with open("data.sql") as f:
                cursor.executescript(f.read())


init_db()


@app.get(f"{prefix}/competitions")
def competitions():
    with sqlite3.connect("data.db", check_same_thread=False) as connection:
        cursor = connection.cursor()
        return cursor.execute("SELECT * FROM competitions").fetchall()


@app.post(f"{prefix}/create_competition")
def create_competition(name: str) -> int:
    with sqlite3.connect("data.db", check_same_thread=False) as connection:
        cursor = connection.cursor()
        row_id = next(cursor.execute("INSERT INTO competitions (name) VALUES (?) RETURNING id", (name,)))
        return row_id


@app.get(f"{prefix}/users")
def users():
    with sqlite3.connect("data.db", check_same_thread=False) as connection:
        cursor = connection.cursor()
        return cursor.execute("SELECT * FROM users").fetchall()


@app.post(f"{prefix}/create_user")
def create_user(user_id: int, name: str):
    with sqlite3.connect("data.db", check_same_thread=False) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (id, name) VALUES (?, ?)", (user_id, name))


@app.post(f"{prefix}/join")
def join(user_id: int, competition_id: int):
    with sqlite3.connect("data.db", check_same_thread=False) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT OR IGNORE INTO competition_users (user_id, competition_id) VALUES (?, ?)", (user_id, competition_id))
    return participants(competition_id)


@app.post(f"{prefix}/participants")
def participants(competition_id: int):
    with sqlite3.connect("data.db", check_same_thread=False) as connection:
        cursor = connection.cursor()
        names = cursor.execute("SELECT name FROM users LEFT JOIN competition_users ON users.id = competition_users.user_id WHERE competition_id = ?", (competition_id,)).fetchall()
        return [x[0] for x in names]


@app.get(f"{prefix}/matches")
def matches():
    with sqlite3.connect("data.db") as connection:
        cursor = connection.cursor()
        return cursor.execute("SELECT * FROM matches;").fetchall()


@app.post(f"{prefix}/add_match")
def add_match(competition_id: int, name: str):
    with sqlite3.connect("data.db", check_same_thread=False) as connection:
        cursor = connection.cursor()
        row_id = next(cursor.execute("INSERT INTO matches (competition_id, name, score1, score2) VALUES (?, ?, ?, ?) RETURNING id", (competition_id, name, None, None)))
        return row_id


@app.post(f"{prefix}/add_match_result")
def add_match_result(match_id: int, score1: int, score2: int):
    with sqlite3.connect("data.db", check_same_thread=False) as connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE matches SET score1 = ?, score2 = ? WHERE id = ?", (score1, score2, match_id))
        return "OK"


@app.post(f"{prefix}/vote")
def vote(user_id: int, match_id: int, score1: int, score2: int):
    with sqlite3.connect("data.db", check_same_thread=False) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO votes (user_id, match_id, score1, score2) VALUES (?, ?, ?, ?)", (user_id, match_id, score1, score2))
        return "OK"


@app.get(f"{prefix}/votes")
def votes():
    with sqlite3.connect("data.db", check_same_thread=False) as connection:
        cursor = connection.cursor()
        result = []
        for row in cursor.execute("SELECT * FROM votes").fetchall():
            _, user_id, match_id, score1, score2 = row
            name, = cursor.execute("SELECT name FROM users LEFT JOIN competition_users ON users.id = competition_users.user_id WHERE competition_users.user_id = ?;", (user_id,)).fetchone()
            _, _, match, _, _ = cursor.execute("SELECT * FROM matches WHERE id = ?;", (match_id,)).fetchone()
            teams = list(map(str.capitalize, match.split("_")))
            result.append(f"{name} {teams[0]} {score1}:{score2} {teams[1]}")
        return result


@app.get(f"{prefix}/points")
def points(competition_id: int, points_id: int):
    with sqlite3.connect("data.db", check_same_thread=False) as connection:
        cursor = connection.cursor()
        user_points = defaultdict(int)
        exact, diff, close, result = cursor.execute("SELECT exact, diff, close, result FROM points WHERE id = ?", (points_id,)).fetchone()
        for row in cursor.execute("SELECT * FROM matches WHERE score1 IS NOT NULL AND score2 IS NOT NULL").fetchall():
            match_id, _, _, score1, score2 = row
            for (user_id,) in cursor.execute("SELECT user_id FROM competition_users WHERE competition_id = ?", (competition_id,)).fetchall():
                _, _, _, vote1, vote2 = cursor.execute("SELECT * FROM votes WHERE user_id = ? AND match_id = ?", (user_id, match_id)).fetchone()
                name, = cursor.execute("SELECT name FROM competition_users LEFT JOIN users ON competition_users.user_id = users.id WHERE users.id = ?", (user_id,)).fetchone()
                if vote1 == score1 and vote2 == score2:
                    user_points[name] += exact
                if vote1 - vote2 == score1 - score2:
                    user_points[name] += diff
                if (vote1 > vote2 and score1 > score2) or (vote1 < vote2 and score1 < score2) or (vote1 == vote2 and score1 == score2):
                    user_points[name] += result
                    if abs(vote1 - score1) + abs(vote2 - score2) == 1:
                        user_points[name] += close
        response = {k: v for k, v in sorted(user_points.items(), key=lambda x: -x[1])}
        return response
