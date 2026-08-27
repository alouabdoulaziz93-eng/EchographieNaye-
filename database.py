import sqlite3

DB_NAME = "echographie_naye.db"

def init_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT,
            age TEXT,
            sexe TEXT,
            telephone TEXT
        )
    """)

    conn.commit()
    conn.close()

    print("BASE DE DONNEES OK")


if __name__ == "__main__":
    init_database()