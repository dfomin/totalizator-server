SELECT_COMPETITIONS = """
SELECT * FROM competitions
"""

INSERT_COMPETITION = """
INSERT INTO competitions (name) VALUES (?) RETURNING id
"""

SELECT_USERS = """
SELECT * FROM users
"""

INSERT_USER = """
INSERT OR IGNORE INTO users (id, name) VALUES (?, ?) RETURNING id
"""

INSERT_COMPETITION_USER = """
INSERT OR IGNORE INTO competition_users (user_id, competition_id) VALUES (?, ?) RETURNING id
"""

SELECT_PARTICIPANTS = """
SELECT name FROM users LEFT JOIN competition_users ON users.id = competition_users.user_id WHERE competition_id = ?
"""

INSERT_MATCH = """
INSERT INTO matches (competition_id, name, score1, score2) VALUES (?, ?, ?, ?) RETURNING id
"""

UPDATE_MATCH = """
UPDATE matches SET score1 = ?, score2 = ? WHERE id = ?
"""

INSERT_VOTE = """
INSERT INTO votes (user_id, match_id, score1, score2) VALUES (?, ?, ?, ?) RETURNING id
"""

SELECT_VOTES = """
SELECT users.name, matches.name, votes.score1, votes.score2
FROM users
LEFT JOIN competition_users
ON users.id = competition_users.user_id
LEFT JOIN votes
ON competition_users.id = votes.user_id
LEFT JOIN matches
ON matches.competition_id = com
"""
