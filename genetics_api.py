import os
from flask import Blueprint, request, jsonify
from genetics_engine import calculate_genetics
from genetics_db import load_loci_from_db

bp = Blueprint("genetics", __name__)

# Use absolute path to ensure DB is found
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, 'database', 'aviario.db')

# Trial Limit
CALC_COUNT = 0
MAX_CALCS = 3

@bp.route("/api/genetics/calculate", methods=["POST"])
def calculate():
    global CALC_COUNT
    if CALC_COUNT >= MAX_CALCS:
        return jsonify({'error': 'Límite de la versión de prueba alcanzado (Máx 3 cálculos genéticos)'}), 403
    
    try:
        data = request.json
        
        male = data.get("male", [])
        female = data.get("female", [])
        species = data.get("species")
        
        if not species:
            return jsonify({'error': 'Species is required'}), 400

        # Increment count
        CALC_COUNT += 1

        # Load Loci definitions from DB
        loci = load_loci_from_db(DB_PATH, species)

        # Calculate
        result = calculate_genetics(male, female, loci)

        return jsonify(result)
        
    except Exception as e:
        print(f"Genetics Calculation Error: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route("/api/genetics/species", methods=["GET"])
def get_species():
    # Proxy to reusing existing DB logic or simple query?
    # Existing app has no direct endpoint for this in blueprint, 
    # but the frontend calls /api/genetics/species.
    # We should implement it here if we removed it from app.py, 
    # OR keep it in app.py if it's generic.
    # The user didn't provide this in the snippet, but the frontend needs it.
    # Let's add it basic.
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT nombre_comun FROM especies")
    rows = cur.fetchall()
    conn.close()
    return jsonify([r[0] for r in rows])
