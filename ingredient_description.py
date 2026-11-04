import sqlite3
import requests
from bs4 import BeautifulSoup
import os
import time
import re

def get_db_connection():
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_path, 'skincare.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def update_ingredient_descriptions():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT ingredient_id, ingred_name FROM ingredients WHERE description IS NULL OR description = ''")
    to_scrape = cur.fetchall()
    
    print(f"Zpracovávám {len(to_scrape)} ingrediencí...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    for row in to_scrape:
        ing_id = row['ingredient_id']
        ing_name = row['ingred_name']
        
        clean_name = re.sub(r'\(.*?\)', '', ing_name).strip()
        url_name = clean_name.lower().replace(" ", "-").replace("/", "-")
        url = f"https://incidecoder.com/ingredients/{url_name}"
        
        print(f"Stahuji: {ing_name}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            description = ""
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                details_section = soup.find("div", {"id": "showmore-section-details"})
                
                if details_section:
                    content_div = details_section.find("div", class_="content")
                    if content_div:
                        paragraphs = content_div.find_all('p')
                        if paragraphs:
                            description = "\n\n".join([p.get_text(separator=" ", strip=True) for p in paragraphs]).strip()
                        else:
                            description = content_div.get_text(separator=' ', strip=True).strip()
                            
                cur.execute("UPDATE ingredients SET description = ? WHERE ingredient_id = ?", (description, ing_id))
                conn.commit()
                
                if description:
                    print(f"Popis aktualizován pro: {ing_name}")
                else:
                    print(f"Popis nebyl na stránce nalezen pro: {ing_name}")
            else:
                print(f"Stránka nenalezena (Stav {response.status_code}): {url}")
        
        except Exception as e:
            print(f"Chyba při stahování {ing_name}: {e}")
        
        time.sleep(1.5)

    conn.close()
    print("Hotovo. Databáze je aktualizována.")

if __name__ == "__main__":
    update_ingredient_descriptions()