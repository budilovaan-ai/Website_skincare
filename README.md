# Skincare Database & Expert System

A comprehensive full-stack application and data processing pipeline designed for managing, scraping, and analyzing cosmetic products, ingredients, and skin concerns. Built with Python, SQLite, and Flask.

## About the Project
This project serves as a centralized database and analytical tool for skincare enthusiasts and data analysts. It automates the extraction of cosmetic data from INCIDecoder, maps active ingredients to specific skin concerns using a custom expert logic system, and provides both a web interface (Flask) and a robust set of command-line tools for database management and analysis.

---

## Tech Stack
* **Backend:** Python, Flask, SQLite
* **Web Scraping:** BeautifulSoup4, Requests, RegEx
* **Database Design:** Relational Schema (Star Schema principles, M:N junction tables, Foreign Keys)
* **Frontend Templates:** HTML5, Jinja2

---

## Project Structure

### 1. Core Web App & Database Setup
* **`app.py`** – Main Flask web application handling routing, search queries, product details, and ingredient views.
* **`main.py`** – Initialization script that builds the SQLite database from scratch using the SQL schema.
* **`skincare_schema.sql`** – Relational database architecture defining tables (`products`, `ingredients`, `functions`, `concerns`, `categories`) and junction tables.

### 2. Data Collection & Scraping
* **`master_scraper.py`** – Advanced web scraper that extracts brand names, prices, usage times, and ingredient functions from INCIDecoder.
* **`ingredient_description.py`** – Automated script to fetch and populate detailed descriptions for database ingredients.

### 3. Database Management & Utilities
* **`add_product.py`** – Interactive CLI tool for manual product insertion and category management.
* **`delete_product_2.py`** – Secure product removal tool with cascading cleanup of related junction table rows.
* **`full_reset_2.py`** – Database maintenance script for a complete system reset (nuclear option).

### 4. Expert System, Tagging & Analysis
* **`update_concerns.py`** – The core "expert system" script containing rich dermatological logic that maps active ingredients (e.g., retinoids, salicylic acid, ceramides) to target skin concerns.
* **`auto_tag.py`** – Automation script for bulk-tagging products based on keyword matching in their names.
* **`search_product_2.py`** – Advanced terminal search tool displaying detailed product compositions, concentrations, and targeted concerns.
* **`search_ingredient_2.py`** – CLI utility to query products and their functions by a specific ingredient.
* **`analyze_product_2.py`** – Text-based inspection tool for reviewing product formulations and ingredient functions directly in the terminal.

---



## Key Highlights
* **Relational Integrity:** Implements strict foreign key constraints and junction tables to handle complex Many-to-Many relationships between products, ingredients, functions, and skin concerns.
* **Smart Tagging Pipeline:** Automatically bridges raw scraped ingredients with clinical skin targets (e.g., acne, barrier repair, anti-aging) using a rule-based expert dictionary.
