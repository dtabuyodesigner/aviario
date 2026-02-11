import os
import sys
from flask import Blueprint, request, send_file, jsonify
from genealogy_engine import obtener_arbol, obtener_detalles_ave, generar_qr, generar_certificado_pdf

bp = Blueprint("genealogy", __name__)

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, 'database', 'aviario.db')
TMP_DIR = os.path.join(BASE_DIR, 'temp')

if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)

@bp.route("/api/birds/<uuid>/certificate", methods=["GET"])
def get_certificate(uuid):
    try:
        # 1. Get Data
        ave = obtener_detalles_ave(DB_PATH, uuid)
        if not ave:
            return jsonify({'error': 'Bird not found'}), 404
            
        arbol = obtener_arbol(DB_PATH, uuid)
        
        # 2. Prepare paths
        qr_filename = f"qr_{uuid}.png"
        qr_path = os.path.join(TMP_DIR, qr_filename)
        pdf_filename = f"certificado_{ave.get('anilla') or uuid}.pdf"
        pdf_path = os.path.join(TMP_DIR, pdf_filename)
        
        # 3. Generate
        generar_qr(uuid, qr_path)
        generar_certificado_pdf(ave, arbol, pdf_path, qr_path)
        
        # 4. Return file
        return send_file(pdf_path, as_attachment=True, download_name=pdf_filename)
        
    except Exception as e:
        print(f"Error generating certificate: {e}")
        return jsonify({'error': str(e)}), 500
