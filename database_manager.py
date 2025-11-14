import sqlite3

class DatabaseManager:
    def __init__(self, db_name="food_app.db"):
        
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password TEXT NOT NULL,
            age INTEGER,
            country TEXT,
            city TEXT,
            region TEXT
           
        );
        """)

        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            rest_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            country TEXT,
            city TEXT,
            region TEXT
        );
        """)

        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            rest_id INTEGER,
            status TEXT,
            total_price REAL,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (rest_id) REFERENCES restaurants(rest_id)
        );
        """)

        self.conn.commit()

    
    def execute(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor

   
    def fetchall(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def close(self):
        self.conn.close()
