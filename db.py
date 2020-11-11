import sqlite3


class DB:
    def __init__(self, name):
        self.conn = sqlite3.connect(name)
        self.cursor = self.conn.cursor()
        try: # create table if not exists
            self.create_tables()
        except:
            pass

    def get_domain_risk_verdict(self, domain_name):
        self.cursor.execute("select verdict, time from domains where domain == (?)", (domain_name,))
        return self.cursor.fetchone()

    def insert_domain_verdict(self, domain_name, verdict,time):
        self.cursor.execute("INSERT INTO domains VALUES (?, ? ,?)", (domain_name, verdict, time))
        self.conn.commit()

    def update_domain_verdict(self, domain_name, verdict, time):
        self.cursor.execute("UPDATE domains SET verdict = ?, time = ? WHERE domain = ?", (verdict, time,domain_name))
        self.conn.commit()

    def insert_domain_votes(self, domain_name, votes : dict):
        for key, val in votes.items():
            self.cursor.execute("INSERT INTO voting VALUES (?,?,?)",
                                (domain_name, key, val))
            self.conn.commit()

    def insert_domain_categories(self, domain_name, categories: dict):
        for key, val in categories.items():
            self.cursor.execute("INSERT INTO categories VALUES (?,?,?)",
                                (domain_name, key, val))
            self.conn.commit()

    def update_domain_categories(self, domain_name, categories: dict):
        self.cursor.execute("DELETE FROM categories WHERE domain = ?", (domain_name,))
        self.conn.commit()
        self.insert_domain_categories(domain_name, categories)

    def update_domain_votes(self, domain_name, votes: dict):
        self.cursor.execute("DELETE FROM voting WHERE domain = ?", (domain_name,))
        self.conn.commit()
        self.insert_domain_votes(domain_name, votes)

    def create_tables(self):
        try:
            self.cursor.execute("CREATE TABLE domains(domain text PRIMARY KEY NOT NULL, verdict text NOT NULL,time INTEGER)")
        except:
            pass
        try:
            self.cursor.execute("CREATE TABLE voting(domain text NOT NULL,vote text NOT NULL,vote_count INTEGER)")
        except:
            pass
        try:
            self.cursor.execute("CREATE TABLE categories(domain text NOT NULL,category text NOT NULL,category_count INTEGER)")
        except:
            pass

        self.conn.commit()

    def __del__(self):
        self.conn.close()

