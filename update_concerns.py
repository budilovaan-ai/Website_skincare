import sqlite3
import os

SKINCARE_KNOWLEDGE = {
    "Anti-Aging (Fine lines)": [
        "Retinol", "Retinal", "Hydroxypinacolone Retinoate", "Bakuchiol",
        "Ascorbic Acid", "Tocopherol", "Tocopheryl Acetate", "Adenosine",
        "Hydrolyzed Collagen", "Soluble Collagen", "Snail Secretion Filtrate",
        "Resveratrol", "Ubiquinone", "Ferulic Acid", "Acetyl Hexapeptide-8",
        "Copper Tripeptide-1", "Palmitoyl Pentapeptide-4", "Palmitoyl Tripeptide-1",
        "Palmitoyl Tetrapeptide-7", "sh-Oligopeptide-1", "Dipeptide Diaminobutyroyl Benzylamide Diacetate"
    ],
    "Acné and clogged pores": [
        "Salicylic Acid", "Betaine Salicylate", "Niacinamide", "Melaleuca Alternifolia",
        "Zinc PCA", "Zinc Oxide", "Houttuynia Cordata", "Kaolin", "Bentonite",
        "Azelaic Acid", "Potassium Azeloyl Diglycinate", "Charcoal Powder",
        "Sulfur", "Benzoyl Peroxide", "Succinic Acid", "Gluconolactone",
        "Lactobionic Acid", "Salix Alba", "Salix Nigra"
    ],
    "Hydration": [
        "Glycerin", "Sodium Hyaluronate", "Hyaluronic Acid", "Hydrolyzed Hyaluronic Acid",
        "Sodium Acetylated Hyaluronate", "Panthenol", "Ceramide NP", "Ceramide AP",
        "Ceramide EOP", "Squalane", "Sodium PCA", "Ectoin", "Betaine", "Trehalose",
        "Polyglutamic Acid", "Urea", "Butylene Glycol", "Propylene Glycol",
        "Beta-Glucan", "Aloe Barbadensis"
    ],
    "Soothing and calming (Redness)": [
        "Centella Asiatica", "Madecassoside", "Asiaticoside", "Asiatic Acid",
        "Madecassic Acid", "Panthenol", "Allantoin", "Artemisia Princeps",
        "Artemisia Vulgaris", "Camellia Sinensis", "Avena Sativa", "Propolis Extract",
        "Bambusa Vulgaris", "Bisabolol", "Chamomilla Recutita", "Calendula Officinalis",
        "Portulaca Oleracea", "Glycyrrhiza Glabra", "Hedera Helix (Ivy) Leaf/Stem Extract"
    ],
    "Skin barrier (Nourishing)": [
        "Ceramide NP", "Cholesterol", "Phytosphingosine", "Squalane",
        "Olea Europaea", "Glycine Soja", "Macadamia Ternifolia", "Cocos Nucifera",
        "Butyrospermum Parkii", "Simmondsia Chinensis", "Argania Spinosa",
        "Rosa Canina", "Linoleic Acid", "Oleic Acid", "Caprylic/Capric Triglyceride",
        "Helianthus Annuus", "Stearic Acid", "Palmitic Acid"
    ],
    "PIE(post acne marks)": [
        "Niacinamide", "Alpha-Arbutin", "Arbutin", "Ascorbic Acid",
        "Sodium Ascorbyl Phosphate", "Tetrahexyldecyl Ascorbate", "Ascorbyl Glucoside",
        "Ethyl Ascorbic Acid", "Azelaic Acid", "Potassium Azeloyl Diglycinate",
        "Oryza Sativa", "Glycolic Acid", "Lactic Acid", "Mandelic Acid", "Malic Acid",
        "Tartaric Acid", "Citric Acid", "Tranexamic Acid", "Kojic Acid",
        "Glutathione", "Acetyl Glucosamine", "Glycyrrhiza Glabra"
    ],
    "Peptides": [
        "Copper Tripeptide-1", "Acetyl Hexapeptide-8", "Palmitoyl Pentapeptide-4", "Palmitoyl Tripeptide-1", "Palmitoyl Tetrapeptide-7", "Palmitoyl Tripeptide-38", "Dipeptide Diaminobutyroyl Benzylamide Diacetate", "Acetyl Tetrapeptide-5", "Palmitoyl Tripeptide-5", "Palmitoyl Tripeptide-8", "Hexapeptide-11", "Tripeptide-1", "Nonapeptide-1", "SH-Polypeptide-121", "Oligopeptide-68", "Myristoyl Pentapeptide-17", "Carnosine", "Trifluoroacetyl Tripeptide-2", "Acetyl Octapeptide-3", "Tetrapeptide-21", "SH-Oligopeptide-1", "SH-Oligopeptide-2", "SH-Polypeptide-1", "SH-Polypeptide-11", "SH-Polypeptide-9"
    ],
    "Cell-communicating":[
        "Niacinamide", "Retinol", "Retinal", "Adenosine", "Acetyl Hexapeptide-8", "Copper Tripeptide-1", "Palmitoyl Pentapeptide-4", "Palmitoyl Tripeptide-1", "Palmitoyl Tetrapeptide-7", "Bakuchiol", "Phytosphingosine", "Carnosine", "Retinyl Palmitate", "Hydroxypinacolone Retinoate", "Dipeptide Diaminobutyroyl Benzylamide Diacetate", "Palmitoyl Tripeptide-5", "Palmitoyl Tripeptide-38"
    ],
    "Brightening": [
        "Ascorbic Acid", " Magnesium Ascorbyl Phosphate", "Niacinamide", "Alpha-Arbutin", "Arbutin", "Tranexamic Acid", "Kojic Acid", "Azelaic Acid", "Potassium Azeloyl Diglycinate", "Glycyrrhiza Glabra (Licorice) Root Extract", "Glycolic Acid", "Lactic Acid", "Glutathione", "Resveratrol", "Acetyl Glucosamine", "Oryza Sativa (Rice) Extract"
    ],
    "Antioxidant": [
        "Ascorbic Acid", " Phaseolus Angularis Seed Extract", "Tocopherol", "Tocopheryl Acetate", "Ferulic Acid", "Resveratrol", "Camellia Sinensis Leaf Extract", "Epigallocatechin Gallate", "Centella Asiatica Extract", "Madecassoside", "Asiaticoside", "Panax Ginseng Root Extract", "Ubiquinone", "Superoxide Dismutase", "Glutathione", "Hydroxydecyl Ubiquinone", "Rosmarinus Officinalis (Rosemary) Leaf Extract", "Vitis Vinifera (Grape) Seed Extract", "Astaxanthin", "Bakuchiol", "Caffeine", "Carnosine", "Phytic Acid", "Portulaca Oleracea Extract", "Propolis Extract", "Salvia Officinalis (Sage) Leaf Extract", "Scutellaria Baicalensis Root Extract", "Tetrahexyldecyl Ascorbate", "Sodium Ascorbyl Phosphate", "Ethyl Ascorbic Acid", "Ascorbyl Glucoside"
    ],
    "Exfoliant": [
        "Salicylic Acid", "Glycolic Acid", "Lactic Acid", "Mandelic Acid", "Gluconolactone", "Lactobionic Acid", "Betaine Salicylate", "Capryloyl Salicylic Acid", "Malic Acid", "Tartaric Acid", "Citric Acid", "Papain", "Bromelain", "Salix Alba (Willow) Bark Extract", "Salix Nigra (Willow) Bark Extract", "Carica Papaya (Papaya) Fruit Extract", "Lactobacillus/Pumpkin Ferment Extract"
    ]
}

def update_concerns_in_db():
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_path, 'skincare.db')

    if not os.path.exists(db_path):
        print("Databáze neexistuje.")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print("Spouštím expertní systém a propojuji ingredience s problémy pleti...\n")

    try:
        cur.execute("PRAGMA foreign_keys = ON;")

        for concern_name, keywords in SKINCARE_KNOWLEDGE.items():
            cur.execute("INSERT OR IGNORE INTO concerns (concern_name) VALUES (?)", (concern_name,))
            cur.execute("SELECT concern_id FROM concerns WHERE concern_name = ?", (concern_name,))
            concern_id = cur.fetchone()[0]

            match_count = 0

            for keyword in keywords:
                cur.execute("SELECT ingredient_id, ingred_name FROM ingredients WHERE ingred_name LIKE ?",
                            (f"%{keyword}%",))
                found_ingredients = cur.fetchall()

                for ing_id, ing_name in found_ingredients:
                    cur.execute("INSERT OR IGNORE INTO ingredient_to_concern (ingredient_id, concern_id) VALUES (?, ?)",
                                (ing_id, concern_id))

                    cur.execute("SELECT product_id FROM product_to_ingredient WHERE ingredient_id = ?", (ing_id,))
                    products_with_ing = cur.fetchall()

                    for prod_id_tuple in products_with_ing:
                        prod_id = prod_id_tuple[0]
                        cur.execute("INSERT OR IGNORE INTO product_to_concern (product_id, concern_id) VALUES (?, ?)",
                                    (prod_id, concern_id))

                    match_count += 1

            print(f"{concern_name}: Nalezeno a propojeno {match_count} látek v databázi.")

        conn.commit()
        print("\nHotovo. Všechny produkty jsou propojené s účinky.")

    except Exception as e:
        print(f"Chyba: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    update_concerns_in_db()