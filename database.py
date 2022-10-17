from sqlite3 import connect
def exec(string, values=[]):
    with connect("database.db") as db:
        cursor = db.cursor()
        return cursor.execute(string, values)

class database_object:
    def __init__(self, name):
        self._name = name
    def set(self, id, column, value):
        if exec(f"SELECT * FROM {self._name} WHERE id = ?", [str(id.id)]).fetchone() == None:
            return "Error Info"
        else:
            exec(f"UPDATE {self._name} SET {column} = ? WHERE id = ?", [value, str(id.id)])
            return True
    def get(self, id, column):
        if exec(f"SELECT * FROM {self._name} WHERE id = ?", [str(id.id)]).fetchone() == None:
            return "Error Info"
        else:
            return exec(f"SELECT {column} FROM {self._name} WHERE id = ?", [str(id.id)])
    def insert(self, columns, values):
        exec(f"""INSERT INTO {self._name}({columns}) VALUES({'?, '*(len(values)-1)}?)""", values)
