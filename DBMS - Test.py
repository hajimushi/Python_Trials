import os
import json


class Hypercube_Data:
    def __init__(self, db_name):
        self.db_name = db_name
        self.tables = {}
        self.table_names = []
        self.load_tables()

    def create_table(self, table_name, columns):
        if table_name in self.table_names:
            print(f"Error: table {table_name} already exists.")
            return

        self.table_names.append(table_name)
        self.tables[table_name] = {"columns": columns, "data": []}
        self.save_tables()
        print(f"Table {table_name} created successfully.")

    def insert_data(self, table_name, data):
        if table_name not in self.table_names:
            print(f"Error: table {table_name} does not exist.")
            return

        table = self.tables[table_name]
        if len(data) != len(table["columns"]):
            print(f"Error: the number of values does not match the number of columns.")
            return

        table["data"].append(dict(zip(table["columns"], data)))
        self.save_tables()
        print(f"Data inserted into table {table_name} successfully.")

    def select_data(self, table_name, columns=None, where=None):
        if table_name not in self.table_names:
            print(f"Error: table {table_name} does not exist.")
            return

        table = self.tables[table_name]
        if columns is None:
            columns = table["columns"]

        data = []
        for row in table["data"]:
            if where is None or where(row):
                data.append([row[column] for column in columns])

        print(" ".join(columns))
        for row in data:
            print(" ".join(str(x) for x in row))

    def save_tables(self):
        with open(f"{self.db_name}.json", "w") as f:
            json.dump(self.tables, f)

    def load_tables(self):
        if os.path.exists(f"{self.db_name}.json"):
            with open(f"{self.db_name}.json") as f:
                self.tables = json.load(f)
                self.table_names = list(self.tables.keys())

    def reset_table(self, table_name):
        if table_name not in self.table_names:
            print(f"Error: table {table_name} does not exist.")
            return

        self.tables[table_name]["data"] = []
        self.save_tables()
        print(f"Table {table_name} reseted data successfully.")



#Data Entry

"""""
db.create_table("users", ["id", "name", "age"])
db.insert_data("users", [1, "Ahmed Salman", 30])
"""""
db = Hypercube_Data("TESTING")
db.select_data("users")
db.reset_table("users")