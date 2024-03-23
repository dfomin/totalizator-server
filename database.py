import sqlite3
from pathlib import Path
from typing import Any, List

from queries import SELECT_COMPETITIONS, SELECT_USERS, INSERT_COMPETITION, INSERT_USER, SELECT_PARTICIPANTS, \
    INSERT_COMPETITION_USER, INSERT_MATCH, UPDATE_MATCH, INSERT_VOTE


class Database:
    def __init__(self, path: str):
        self.path = path
        if not Path(path).exists():
            with sqlite3.connect(path, check_same_thread=False) as connection:
                cursor = connection.cursor()
                with open("data.sql") as f:
                    cursor.executescript(f.read())

    def _select(self, request: str, params: Any = None) -> List[Any]:
        with sqlite3.connect(self.path, check_same_thread=False) as connection:
            cursor = connection.cursor()
            if params is not None:
                return cursor.execute(request, params).fetchall()
            else:
                return cursor.execute(request).fetchall()

    def _insert(self, request: str, params: Any) -> int:
        with sqlite3.connect(self.path, check_same_thread=False) as connection:
            cursor = connection.cursor()
            if params is not None:
                row_id = next(cursor.execute(request, params))
            else:
                row_id = next(cursor.execute(request))
            return row_id

    def _update(self, request: str, params: Any):
        with sqlite3.connect(self.path, check_same_thread=False) as connection:
            cursor = connection.cursor()
            return cursor.execute(request, params)

    def competitions(self):
        return self._select(SELECT_COMPETITIONS)

    def create_competition(self, name: str):
        self._insert(INSERT_COMPETITION, name)

    def users(self):
        return self._select(SELECT_USERS)

    def create_user(self, user_id: int, name: str):
        self._insert(INSERT_USER, (user_id, name))

    def join(self, user_id: int, competition_id: int):
        self._insert(INSERT_COMPETITION_USER, (user_id, competition_id))

    def participants(self, competition_id) -> List[str]:
        return list(map(lambda x: x[0], self._select(SELECT_PARTICIPANTS, (competition_id,))))

    def add_match(self, competition_id: int, name: str):
        self._insert(INSERT_MATCH, (competition_id, name))

    def add_match_result(self, match_id: int, score1: int, score2: int):
        self._update(UPDATE_MATCH, (score1, score2, match_id))

    def vote(self, user_id: int, match_id: int, score1: int, score2: int):
        self._insert(INSERT_VOTE, (user_id, match_id, score1, score2))

    def votes(self, competition_id: int):
