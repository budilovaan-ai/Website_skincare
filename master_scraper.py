import sqlite3
import requests
from bs4 import BeautifulSoup
import os
import time
import re


def get_ingredient_safety(ing_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
    try:
        time.sleep(0.3)
        resp = requests.get(f"https://incidecoder.com{ing_url}", headers=headers, timeout=10)
        soup = BeautifulSoup(resp.content, 'html.parser')
        safety_div = soup.find('div', class_='safety-info-container')
        if safety_div:
            for row in safety_div.find_all('tr'):
                if "Comedogenic" in row.text:
                    val = row.find('span', class_='value')
                    if val: return int(val.text.strip().split('-')[0].split(' ')[0])
        return 0
    except:
        return 0


def scrape_expert_product(url):
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_path, 'skincare.db')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

    print(f"Připojuji se k: {url}")
    response = requests.get(url, headers=headers, timeout=20)
    soup = BeautifulSoup(response.content, 'html.parser')

    h1 = soup.find('h1')
    full_title = h1.get_text(strip=True) if h1 else "Neznámý produkt"

    brand_link = soup.find('a', class_='product-brand-link')
    detected_brand = brand_link.get_text(strip=True) if brand_link else full_title.split(' ')[0]

    print(f"\n--- PRODUKT: {full_title} ---")
    brand = input(f"BRAND (Enter pro '{detected_brand}'): ").strip() or detected_brand
    product_name = re.sub(re.escape(brand), '', full_title, flags=re.IGNORECASE).strip().lstrip('- ').strip()

    user_cat = input("Category: ").strip()

    time_of_use = input("Time of use (AM/PM/Both): ").strip()

    if time_of_use.lower() == 'both':
        time_of_use = 'AM/PM'

    price = input("Price: ").strip()
    notes = input("Note: ").strip()

    all_links = soup.find_all('a', href=re.compile(r'^/ingredients/'))

    ingred_data = []
    seen_urls = set()

    ignore_words = ['goodie', 'superstar', 'icky', 'average', 'unknown']

    for link in all_links:
        url_ing = link.get('href')
        name = link.get_text(strip=True)

        tr = link.find_parent('tr')
        if not tr or url_ing in seen_urls or not name:
            continue

        seen_urls.add(url_ing)

        func_text = ""

        td_name = link.find_parent('td')
        if td_name:
            td_func = td_name.find_next_sibling('td')
            if td_func:
                func_text = td_func.get_text(separator=", ", strip=True)

        func_text = func_text.replace("show more", "").replace("...", "").strip(" ,|")

        if func_text.lower() == name.lower() or re.match(r'^[\d\s\-,|]+$', func_text):
            func_text = ""

        ingred_data.append({'name': name, 'url': url_ing, 'functions': func_text})

    if not ingred_data:
        print("Chyba: Stránka se načetla, ale v tabulce nebyly nalezeny žádné ingredience.")
        return

    print(f"Nalezeno {len(ingred_data)} čistých ingrediencí. Ukládám...")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        cur.execute("PRAGMA foreign_keys = ON;")
        cur.execute("INSERT OR IGNORE INTO categories (category_name) VALUES (?)", (user_cat,))
        cur.execute("SELECT category_id FROM categories WHERE category_name = ?", (user_cat,))
        cat_id = cur.fetchone()[0]

        cur.execute("""
                    INSERT INTO products (brand, product_name, category_id, time_of_use, price, personal_notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """, (brand, product_name, cat_id, time_of_use, float(price) if price else 0, notes))
        product_id = cur.lastrowid

        for ing in ingred_data:
            i_name = ing['name']
            i_url = ing['url']
            func_raw = ing['functions']

            cur.execute("SELECT ingredient_id FROM ingredients WHERE ingred_name = ?", (i_name,))
            res = cur.fetchone()
            if not res:
                print(f"  Učím se novou látku: {i_name}")
                comedo = get_ingredient_safety(i_url)
                cur.execute(
                    "INSERT INTO ingredients (ingred_name, inci_name, comedogenic_rating, is_fungal_acne_safe) VALUES (?, ?, ?, 1)",
                    (i_name, i_name, comedo))
                ing_id = cur.lastrowid
            else:
                ing_id = res[0]

            cur.execute("INSERT OR IGNORE INTO product_to_ingredient (product_id, ingredient_id) VALUES (?, ?)",
                        (product_id, ing_id))

            if func_raw:
                funcs = [f.strip() for f in func_raw.split(',')]
                valid_funcs = []
                for f in funcs:
                    if len(f) > 2 and f.lower() not in ignore_words:
                        valid_funcs.append(f)

                if valid_funcs:
                    print(f"    Funkce: {', '.join(valid_funcs)}")
                    for f_name in valid_funcs:
                        cur.execute("INSERT OR IGNORE INTO functions (function_name) VALUES (?)", (f_name,))
                        cur.execute("SELECT function_id FROM functions WHERE function_name = ?", (f_name,))
                        f_id = cur.fetchone()[0]
                        cur.execute(
                            "INSERT OR IGNORE INTO ingredient_to_function (ingredient_id, function_id) VALUES (?, ?)",
                            (ing_id, f_id))

        conn.commit()
        print(f"\nHotovo. Produkt '{product_name}' je úspěšně uložen.")

    except Exception as e:
        print(f"Chyba: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    url = input("Vlož URL: ").strip()
    if url: scrape_expert_product(url)