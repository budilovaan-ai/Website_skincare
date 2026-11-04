import sqlite3
import os


def nuclear_reset():
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_path, 'skincare.db')

    if not os.path.exists(db_path):
        print("Soubor databáze neexistuje.")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print(f"Probíhá totální reset: {db_path}")

    try:
        tabulky = [
            "product_to_ingredient",
            "product_to_function",
            "product_to_concern",
            "ingredient_to_function",
            "ingredient_to_concern",
            "products",
            "ingredients",
            "functions",
            "concerns",
            "categories"
        ]

        for tabulka in tabulky:
            cur.execute(f"DELETE FROM {tabulka};")
            cur.execute(f"DELETE FROM sqlite_sequence WHERE name='{tabulka}';")

        conn.commit()
        print("Hotovo. Databáze je naprosto prázdná a připravená.")

    except Exception as e:
        print(f"Chyba při mazání: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    print("Varování: Tohle smaže úplně všechna data, tedy produkty i naučené ingredience.")
    confirm = input("Chceš opravdu začít od nuly? (ano/ne): ")
    if confirm.lower() == 'ano':
        nuclear_reset()
    else:
        print("Reset zrušen.")