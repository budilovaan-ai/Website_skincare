import sqlite3
import os


def najdi_produkty_podle_ingredience():
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_path, 'skincare.db')

    if not os.path.exists(db_path):
        print("Chyba: Databáze nebyla nalezena. Nejdřív spusť scraper.")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    hledana_latka = input("\nZadej název ingredience, kterou hledáš: ").strip()

    query = """
            SELECT p.brand, p.product_name, f.function_name
            FROM products p
                     JOIN product_to_ingredient pti ON p.product_id = pti.product_id
                     JOIN ingredients i ON pti.ingredient_id = i.ingredient_id
                     LEFT JOIN ingredient_to_function itf ON i.ingredient_id = itf.ingredient_id
                     LEFT JOIN functions f ON itf.function_id = f.function_id
            WHERE i.ingred_name LIKE ? \
            """

    cur.execute(query, (f"%{hledana_latka}%",))
    vysledky = cur.fetchall()

    if vysledky:
        print(f"\nProdukty obsahující '{hledana_latka}':")
        print("-" * 60)
        vypsane_produkty = set()

        for znackka, jmeno, funkce in vysledky:
            ID_produktu = f"{znackka} - {jmeno}"
            if ID_produktu not in vypsane_produkty:
                print(f"{znackka} | {jmeno}")
                vypsane_produkty.add(ID_produktu)

            if funkce:
                print(f"   ∟ Funkce v tomto produktu: {funkce}")
    else:
        print(f"Žádný produkt s ingrediencí '{hledana_latka}' v databázi není.")

    conn.close()


if __name__ == "__main__":
    najdi_produkty_podle_ingredience()