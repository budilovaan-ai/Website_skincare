import sqlite3
import os

def add_new_product():
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_path, 'skincare.db')
    
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    print("---ADD NEW PRODUCT TO DATABASE ---")

    # 1. KATEGORIE
    cat_name = input("Category (e.g., Serum, Moisturizer, Cleanser): ").strip()
    
    cursor.execute("SELECT category_id FROM categories WHERE category_name = ?", (cat_name,))
    result = cursor.fetchone()

    if result:
        cat_id = result[0]
        print(f"-> Using existing category ID: {cat_id}")
    else:
        cursor.execute("INSERT INTO categories (category_name) VALUES (?)", (cat_name,))
        cat_id = cursor.lastrowid
        print(f"-> Created new category '{cat_name}' with ID: {cat_id}")

    # 2. PRODUKT
    brand = input("Brand (e.g., The Ordinary): ").strip()
    name = input("Product Name: ").strip()
    fragrance = input("Has fragrance? (y/n): ").lower() == 'y'
    time = input("Time of use (AM/PM/Both): ").strip()
    pao = input("PAO months (number): ").strip()

    try:
        cursor.execute("""
            INSERT INTO products (brand, product_name, category_id, has_fragrance, time_of_use, pao_months)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (brand, name, cat_id, fragrance, time, pao))
        
        new_product_id = cursor.lastrowid
        conn.commit()
        print(f"'{name}' added with ID: {new_product_id}")
        
    except Exception as e:
        print(f" Error when adding new product: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_new_product()

try:
    cursor.execute("DELETE FROM categories WHERE category_id = 5")
    conn.commit()
    print("Done")
except Exception as e:
    print(f"Error when cleaning{e}")
finally:
    conn.close()