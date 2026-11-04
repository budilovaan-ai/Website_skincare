import sqlite3
import os

def init_db():
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    db_file = os.path.join(base_path, 'skincare.db')
    sql_file = os.path.join(base_path, 'skincare_schema.sql')

    if os.path.exists(db_file):
        os.remove(db_file)

    try:
        conn = sqlite3.connect(db_file)
        
        conn.execute("PRAGMA foreign_keys = ON;")
        
        cursor = conn.cursor()

        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        cursor.executescript(sql_script)
        
        conn.commit()
        print("Databáze 'skincare.db' byla úspěšně vytvořena a inicializována.")
        
    except Exception as e:
        print(f"Chyba: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()