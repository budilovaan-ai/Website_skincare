-- 1. Categories
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name VARCHAR(50) UNIQUE NOT NULL
);

-- 2. Products
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand VARCHAR(100),
    product_name VARCHAR(255) NOT NULL,
    category_id INTEGER REFERENCES categories(category_id),
    has_fragrance BOOLEAN,
    time_of_use VARCHAR(20),
    pao_months INTEGER,
    personal_notes TEXT, 
    price NUMERIC(10, 2)
);

-- 3. Ingredients
CREATE TABLE ingredients (
    ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingred_name VARCHAR(255) UNIQUE NOT NULL,
    inci_name VARCHAR(255) UNIQUE NOT NULL,
    comedogenic_rating INTEGER,
    is_fungal_acne_safe BOOLEAN,
    description TEXT
);

-- 4. Functions
CREATE TABLE functions (
    function_id INTEGER PRIMARY KEY AUTOINCREMENT,
    function_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN,
    scientific_group VARCHAR(50)
);

-- 5. Concerns
CREATE TABLE concerns (
    concern_id INTEGER PRIMARY KEY AUTOINCREMENT,
    concern_name VARCHAR(100) UNIQUE NOT NULL
);

-- JUNCTION TABLES (M:N Relationships)

CREATE TABLE product_to_ingredient (
    product_id INTEGER REFERENCES products(product_id),
    ingredient_id INTEGER REFERENCES ingredients(ingredient_id),
    PRIMARY KEY (product_id, ingredient_id)
);

CREATE TABLE ingredient_to_function (
    ingredient_id INTEGER REFERENCES ingredients(ingredient_id),
    function_id INTEGER REFERENCES functions(function_id),
    PRIMARY KEY (ingredient_id, function_id)
);

CREATE TABLE ingredient_to_concern (
    ingredient_id INTEGER REFERENCES ingredients(ingredient_id),
    concern_id INTEGER REFERENCES concerns(concern_id),
    PRIMARY KEY (ingredient_id, concern_id)
);

CREATE TABLE product_to_concern (
    product_id INTEGER REFERENCES products(product_id),
    concern_id INTEGER REFERENCES concerns(concern_id),
    PRIMARY KEY (product_id, concern_id)
);

CREATE TABLE product_to_function (
    product_id INTEGER REFERENCES products(product_id),
    function_id INTEGER REFERENCES functions(function_id),
    PRIMARY KEY (product_id, function_id)
);

CREATE TABLE ingredient_conflicts (
    conflict_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_id_1 INTEGER,
    ingredient_id_2 INTEGER,
    reason TEXT, -- např. "Zvyšuje riziko podráždění a narušení kožní bariéry."
    FOREIGN KEY (ingredient_id_1) REFERENCES ingredients(ingredient_id),
    FOREIGN KEY (ingredient_id_2) REFERENCES ingredients(ingredient_id)
);

--- INITIAL DATA LOAD ---

-- Categories
INSERT INTO categories (category_name) VALUES ('Serum');
INSERT INTO categories (category_name) VALUES ('Moisturizer');

-- Products
INSERT INTO products (brand, product_name, category_id, has_fragrance, time_of_use, personal_notes, pao_months) 
VALUES ('The Ordinary', 'Salicylic Acid 2% Solution', 1, 0, 'PM', 'Gold standard', 12);

-- Ingredients
INSERT INTO ingredients (ingred_name, inci_name, comedogenic_rating, is_fungal_acne_safe, description) 
VALUES ('Salicylic Acid (BHA)', 'Salicylic Acid', 0, 1, 'Exfoliates skin on the surface and in the pores.');

-- Concerns
INSERT INTO concerns (concern_name) VALUES ('Acne'); -- ID 1
INSERT INTO concerns (concern_name) VALUES ('Blackheads'); -- ID 2

-- Functions
INSERT INTO functions (function_name) VALUES ('Pore cleaner'); -- ID 1
INSERT INTO functions (function_name) VALUES ('Exfoliant'); -- ID 2

--- ESTABLISH CONNECTIONS ---

-- Product 1 to Ingredient 1
INSERT INTO product_to_ingredient (product_id, ingredient_id) VALUES (1, 1);

-- Product 1 to Concerns 1 and 2
INSERT INTO product_to_concern (product_id, concern_id) VALUES (1, 1);
INSERT INTO product_to_concern (product_id, concern_id) VALUES (1, 2);

--