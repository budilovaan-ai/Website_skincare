import sqlite3
import os

TAGS = {
    "Ginseng Cleansing": [82, 75],
    "Centella Light": [76, 75],
    "Cream-to-Foam": [75, 77],
    "Quercetinol": [74, 76],
    "SA smoothing": [74, 83],
    "Niacinamide": [74, 78, 80, 81],
    "Salicylic": [74, 83],
    "aPAD": [74, 78, 81],
    "AHA BHA": [83, 81, 74],
    "Chestnut": [74, 83],
    "azealic": [74, 78, 81],
    "Hyaluron": [75, 77],
    "snail 96": [75, 76],
    "Centella Ampoule": [76, 82],
    "Green Tea": [76, 82, 77],
    "Ginseng snail": [73, 75, 76],
    "Black Rice": [77, 75, 82],
    "6 Peptide": [79, 80, 73],
    "Pink Peptide": [79, 73, 77],
    "Glow Deep": [81, 78],
    "Propolis": [81, 74, 82],
    "Revive Eye": [73, 80],
    "retinal": [73, 80, 74],
    "caffeine": [82, 81],
    "Mighty Bamboo": [77, 76, 75],
    "hydration station": [75, 77],
    "barriereschutz": [77, 76],
    "Red Bean Water": [75, 79],
    "Poremizing": [74, 76, 79],
    "Red Bean Refreshing": [74, 83],
    "Lion pair": [74, 76],
    "Pink Spot": [74, 76],
    "mighty patch": [74],
    "Tea-Trica": [74, 76],
    "NIVEA SUN": [76, 77],
    "BOJ spf": [77, 75, 82],
    "MIXA": [77, 75],
    "hyaluronic cream": [75, 82],
    "345 RELIEF": [76, 77, 78]
}

base_path = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_path, 'skincare.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

print("Mazání a oprava názvů...")
cur.execute("DELETE FROM product_to_concern")
cur.execute("UPDATE concerns SET concern_name = 'Acne and clogged pores' WHERE concern_name LIKE 'Acné%'")

cur.execute("SELECT product_id, product_name FROM products")
products = cur.fetchall()

nalezeno = 0
for p_id, p_name in products:
    for klic, concerns in TAGS.items():
        if klic.lower() in p_name.lower():
            for c_id in concerns:
                cur.execute("INSERT OR IGNORE INTO product_to_concern (product_id, concern_id) VALUES (?, ?)", (p_id, c_id))
            nalezeno += 1
            break

conn.commit()
conn.close()
print(f"Automaticky oštítkováno {nalezeno} produktů!")




