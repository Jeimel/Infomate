from sqlite3 import connect
from os import makedirs, path


DIRECTORY = "../data"


class TokenDatabase:
    def __init__(self) -> None:
        if not path.exists(DIRECTORY):
            makedirs(DIRECTORY)
        self.con = connect("../data/tokens.db")
        self.cursor = self.con.cursor()

    def _execute(self, sql: str, parameters: tuple=(), commit: bool=False) -> bool:
        try:
            self.cursor.execute(sql, parameters)
            if commit:
                self.con.commit()
        except:
            return False
        
        return True

    def create(self, name: str) -> None:
        self._execute(
            "CREATE TABLE IF NOT EXISTS {} (value TEXT PRIMARY KEY, name TEXT)".format(name),
        )
    
    def add(self, app: str, name: str, value: str) -> bool:
        return self._execute(
            "INSERT INTO {}(value, name) VALUES(?, ?)".format(app),
            (value, name),
            commit=True
        )
        
    def remove(self, app: str, name: str) -> bool:
        return self._execute(
            "DELETE FROM {} WHERE name = ?".format(app),
            (name,),
            commit=True
        )

    def update(self, app: str, name: str, value: str) -> bool:
        return self._execute(
            "UPDATE {} SET value = ? WHERE name = ?".format(app),
            (value, name),
            commit=True
        )
