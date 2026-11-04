from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

def get_db_connection():
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_path, 'skincare.db')
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    search_query = request.args.get('q')
    results = []

    if search_query:
        conn = get_db_connection()
        hledane_slovo = f"%{search_query}%"
        
        sql_query = """
            SELECT p.product_id, p.brand, p.product_name, GROUP_CONCAT(DISTINCT c.concern_name) as concerns
            FROM products p
            LEFT JOIN product_to_concern ptc ON p.product_id = ptc.product_id
            LEFT JOIN concerns c ON ptc.concern_id = c.concern_id
            LEFT JOIN product_to_ingredient pti ON p.product_id = pti.product_id
            LEFT JOIN ingredients i ON pti.ingredient_id = i.ingredient_id
            WHERE p.brand LIKE ? 
               OR p.product_name LIKE ?
               OR i.ingred_name LIKE ?
               OR c.concern_name LIKE ?
            GROUP BY p.product_id
        """
        
        results = conn.execute(sql_query, (hledane_slovo, hledane_slovo, hledane_slovo, hledane_slovo)).fetchall()
        conn.close()

    return render_template('index.html', search_query=search_query, results=results)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()
    
    product = conn.execute('''
        SELECT p.product_id, p.brand, p.product_name, c.category_name, p.time_of_use, p.personal_notes
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        WHERE p.product_id = ?
    ''', (product_id,)).fetchone()
    
    ingredients_raw = conn.execute('''
        SELECT i.ingredient_id, i.ingred_name, 
               GROUP_CONCAT(f.function_name, ', ') as functions
        FROM ingredients i
        JOIN product_to_ingredient pti ON i.ingredient_id = pti.ingredient_id
        LEFT JOIN ingredient_to_function itf ON i.ingredient_id = itf.ingredient_id
        LEFT JOIN functions f ON itf.function_id = f.function_id
        WHERE pti.product_id = ?
        GROUP BY i.ingredient_id
    ''', (product_id,)).fetchall()
    
    conn.close()
    
    if product is None:
        return "Product not found :(", 404

    vip_functions = [
        "antioxidant", "cell-communicating", "brightening", 
        "soothing", "anti-acne", "moisturizer", "humectant", "skin-identical", 
        "exfoliant", "sunscreen", "antimicrobial", "antibacterial", "emollient"
    ]

    icky_keywords = [
        "parfum", "fragrance", "flavor", "T-Butyl Alcohol",
        "alcohol denat", "sd alcohol", "isopropyl alcohol", "ethanol", 
        "limonene", "linalool", "citronellol", "geraniol", "eugenol", "farnesol",
        "peppermint", "mentha piperita", "eucalyptus", "citrus", "lavandula", "lavender",
        "sodium lauryl sulfate", "sls"
    ]

    all_ingredients = []
    key_ingredients = []

    for row in ingredients_raw:
        ing = dict(row) 
        funcs_str = ing['functions'] if ing['functions'] else ""
        ing_name_lower = ing['ingred_name'].lower()
        
        ing['is_star'] = any(vip in funcs_str.lower() for vip in vip_functions)
        ing['is_icky'] = any(icky in ing_name_lower for icky in icky_keywords)
        
        if ing['is_star']:
            key_ingredients.append(ing)
            
        all_ingredients.append(ing)
        
    return render_template('detail.html', product=product, ingredients=all_ingredients, key_ingredients=key_ingredients)

@app.route('/ingredient/<int:ingredient_id>')
def ingredient_detail(ingredient_id):
    conn = get_db_connection()
    
    ingredient = conn.execute('SELECT * FROM ingredients WHERE ingredient_id = ?', (ingredient_id,)).fetchone()
    
    if ingredient is None:
        conn.close()
        return "Ingredient not found :(", 404
        
    funcs = conn.execute('''
        SELECT f.function_name
        FROM functions f
        JOIN ingredient_to_function itf ON f.function_id = itf.function_id
        WHERE itf.ingredient_id = ?
    ''', (ingredient_id,)).fetchall()
    
    products = conn.execute('''
        SELECT p.product_id, p.brand, p.product_name
        FROM products p
        JOIN product_to_ingredient pti ON p.product_id = pti.product_id
        WHERE pti.ingredient_id = ?
    ''', (ingredient_id,)).fetchall()
    
    conn.close()
    
    vip_functions = [
        "antioxidant", "cell-communicating", "brightening", 
        "soothing", "anti-acne", "moisturizer", "humectant", "skin-identical", 
        "exfoliant", "sunscreen", "antimicrobial", "antibacterial", "emollient"
    ]
    
    icky_keywords = [
        "parfum", "fragrance", "flavor", "T-Butyl Alcohol",
        "alcohol denat", "sd alcohol", "isopropyl alcohol", "ethanol", 
        "limonene", "linalool", "citronellol", "geraniol", "eugenol", "farnesol",
        "peppermint", "mentha piperita", "eucalyptus", "citrus", "lavandula", "lavender",
        "sodium lauryl sulfate", "sls"
    ]
    
    funcs_str = " ".join([f['function_name'].lower() for f in funcs])
    ing_name_lower = ingredient['ingred_name'].lower()
    
    is_star = any(vip in funcs_str for vip in vip_functions)
    is_icky = any(icky in ing_name_lower for icky in icky_keywords)
    
    return render_template('ingredient.html', 
                           ingredient=ingredient, 
                           functions=funcs,
                           products=products, 
                           is_star=is_star, 
                           is_icky=is_icky)

if __name__ == '__main__':
    app.run(debug=True)