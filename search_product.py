import sqlite3
import os


def ultimate_search():
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_path, 'skincare.db')

    if not os.path.exists(db_path):
        print("Databáze neexistuje.")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    search_term = input("\nZadej název produktu nebo značky (nebo stiskněte Enter pro všechny): ").strip()

    cur.execute("""
                SELECT p.product_id, p.brand, p.product_name, c.category_name, p.time_of_use, p.price, p.personal_notes
                FROM products p
                         LEFT JOIN categories c ON p.category_id = c.category_id
                WHERE p.product_name LIKE ?
                   OR p.brand LIKE ?
                """, (f"%{search_term}%", f"%{search_term}%"))

    products = cur.fetchall()

    if not products:
        print("V databázi nebylo nic nalezeno. Zkuste jiný název.")
        conn.close()
        return

    for product in products:
        p_id, brand, name, cat, time_use, price, notes = product

        print(f"\n{'=' * 115}")
        print(f"{brand.upper()} - {name.upper()}")
        print(f"{'=' * 115}")
        print(f"Kategorie: {cat} | Doba použití: {time_use} | Cena: {price} Kč")
        if notes and notes.lower() != 'x':
            print(f"Vaše poznámka: {notes}")

        cur.execute("""
                    SELECT DISTINCT c.concern_name
                    FROM concerns c
                             JOIN product_to_concern ptc ON c.concern_id = ptc.concern_id
                    WHERE ptc.product_id = ?
                    """, (p_id,))

        concerns = [row[0] for row in cur.fetchall()]
        if concerns:
            print(f"Cílené problémy (Celkově): [ {']  ['.join(concerns)} ]")
        else:
            print("Cílené problémy: (Zatím nepřiřazeno)")

        print("-" * 115)
        print(f"{'INGREDIENCE':<33} | {'%':<6} | {'HLAVNÍ ZAMĚŘENÍ (PROBLÉM)':<35} | {'FUNKCE'}")
        print("-" * 115)

        cur.execute("""
                    SELECT i.ingred_name,
                           pti.concentration,
                           GROUP_CONCAT(DISTINCT c.concern_name),
                           GROUP_CONCAT(DISTINCT f.function_name)
                    FROM ingredients i
                             JOIN product_to_ingredient pti ON i.ingredient_id = pti.ingredient_id
                             LEFT JOIN ingredient_to_concern itc ON i.ingredient_id = itc.ingredient_id
                             LEFT JOIN concerns c ON itc.concern_id = c.concern_id
                             LEFT JOIN ingredient_to_function itf ON i.ingredient_id = itf.ingredient_id
                             LEFT JOIN functions f ON itf.function_id = f.function_id
                    WHERE pti.product_id = ?
                    GROUP BY i.ingredient_id
                    """, (p_id,))

        ingredients_data = cur.fetchall()

        for ing_name, conc, ing_concerns, funcs in ingredients_data:
            conc_str = f"{conc}" if conc else ""

            concern_str = ing_concerns.replace(',', ', ') if ing_concerns else "---"

            func_str = funcs.replace(',', ', ') if funcs else "---"

            if conc_str or ing_concerns:

                print(f"⭐ {ing_name[:32]:<32} | {conc_str:<6} | 🌿 {concern_str[:32]:<32} | {func_str}")

            else:

                print(f"🔹 {ing_name[:32]:<32} | {conc_str:<6} |    {concern_str[:32]:<32} | {func_str}")

    conn.close()


if __name__ == "__main__":
    ultimate_search()