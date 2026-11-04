import sqlite3
import os


def analyze_db():
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_path, 'skincare.db')

    if not os.path.exists(db_path):
        print("Database doesn't exist.")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    hledat = input("\n Zadej část názvu produktu (nebo dej Enter pro výpis všeho): ").strip()


    query = """
            SELECT p.brand, \
                   p.product_name, \
                   i.ingred_name, \
                   GROUP_CONCAT(f.function_name, ', ')
            FROM products p
                     JOIN product_to_ingredient pti ON p.product_id = pti.product_id
                     JOIN ingredients i ON pti.ingredient_id = i.ingredient_id
                     LEFT JOIN ingredient_to_function itf ON i.ingredient_id = itf.ingredient_id
                     LEFT JOIN functions f ON itf.function_id = f.function_id
            WHERE p.product_name LIKE ? \
               OR p.brand LIKE ?
            GROUP BY p.product_id, i.ingredient_id \
            """

    cur.execute(query, (f"%{hledat}%", f"%{hledat}%"))
    rows = cur.fetchall()

    if not rows:
        print("Nic nebylo nalezeno.")
        conn.close()
        return

    current_product = ""
    for brand, p_name, ing_name, funcs in rows:
        prod_full = f"{brand} - {p_name}"


        if prod_full != current_product:
            print(f"\n" + "=" * 80)
            print(f"✨ ANALÝZA: {prod_full}")
            print("=" * 80)
            print(f"{'INGREDIENCE':<40} | {'FUNKCE'}")
            print("-" * 80)
            current_product = prod_full

       
        f_display = funcs if funcs else "---"
        print(f"🔹 {ing_name[:38]:<38} | {f_display}")

    conn.close()


if __name__ == "__main__":
    analyze_db()