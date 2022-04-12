CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

CREATE TABLE points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exact REAL,
    diff REAL,
    close REAL,
    result REAL
);

CREATE TABLE competitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

CREATE TABLE matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    competition_id INTEGER,
    name TEXT,
    score1 INT,
    score2 INT,

    FOREIGN KEY(competition_id) REFERENCES competition(id)
);

CREATE TABLE competition_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    competition_id INTEGER,

    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(competition_id) REFERENCES competition(id)
);

CREATE TABLE votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    match_id INTEGER,
    score1 INTEGER,
    score2 INTEGER,

    FOREIGN KEY(user_id) REFERENCES competition_users(id),
    FOREIGN KEY(match_id) REFERENCES matches(id)
);

INSERT INTO points(exact, diff, close, result) VALUES (2, 1, 0, 1);
INSERT INTO points(exact, diff, close, result) VALUES (1, 1, 0, 1);
INSERT INTO points(exact, diff, close, result) VALUES (1.5, 0.5, 0.5, 1);