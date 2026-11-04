import sqlite3
import os

def smazat_produkt():
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_path, 'skincare.db')

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    print("--- DELETE PRODUCT ---")

    cur.execute("SELECT product_id, brand, product_name FROM products")
    produkty = cur.fetchall()

    if not produkty:
        print("V databázi nejsou žádné produkty.")
        conn.close()
        return

    print(f"{'ID':<5} | {'ZNAČKA':<20} | {'NÁZEV PRODUKTU'}")
    print("-" * 50)
    for p_id, brand, name in produkty:
        print(f"{p_id:<5} | {brand:<20} | {name}")

    target_id = input("\nZadej ID produktu, který chceš VYMAZAT (nebo Enter pro zrušení): ").strip()

    if not target_id:
        print("Akce zrušena.")
        conn.close()
        return

    try:
       
        tables_to_clean = ["product_to_ingredient", "product_to_function", "product_to_concern"]
        for table in tables_to_clean:
            cur.execute(f"DELETE FROM {table} WHERE product_id = ?", (target_id,))


        cur.execute("DELETE FROM products WHERE product_id = ?", (target_id,))
        
        conn.commit()
        print(f"Produkt s ID {target_id} byl vymazán.")
        
    except Exception as e:
        print(f"Error when deleting: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    smazat_produkt()