import os
from flask import Blueprint, request, jsonify
from genetics_engine import calculate_genetics
from genetics_db import load_loci_from_db

bp = Blueprint("genetics", __name__)

# Use absolute path to ensure DB is found
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'aviario.db')

@bp.route("/api/genetics/calculate", methods=["POST"])
def calculate():
    try:
        # VERIFICACIÓN DEMO
        # Simple in-memory counter for this process
        if not hasattr(calculate, "demo_count"):
             calculate.demo_count = 0
        
        if calculate.demo_count >= 5:
             # Reset on server restart only, which is fine for demo zip
             return jsonify({'error': 'Límite DEMO: Máximo 5 cálculos genéticos por sesión.'}), 403
        
        calculate.demo_count += 1

        data = request.json
        
        male = data.get("male", [])
        female = data.get("female", [])
        species = data.get("species")
        
        if not species:
            return jsonify({'error': 'Species is required'}), 400

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
