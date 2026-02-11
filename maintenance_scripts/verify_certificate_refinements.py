import sqlite3
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from genealogy_engine import obtener_arbol, obtener_detalles_ave, generar_qr, generar_certificado_pdf
DB_PATH = os.path.join(BASE_DIR, 'database', 'aviario.db')
TMP_DIR = os.path.join(BASE_DIR, 'temp')

if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)

def test_refinements():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # Use the Expo Periquito we just created
    target_anilla = "EXPO-2024-01"
    bird = conn.execute("SELECT uuid FROM pajaros WHERE anilla = ?", (target_anilla,)).fetchone()
    if not bird:
        print("Error: Target bird not found in DB!")
        return
    
    son_uuid = bird['uuid']
    
    # 2. Test Engine
    ave = obtener_detalles_ave(DB_PATH, son_uuid)
    arbol = obtener_arbol(DB_PATH, son_uuid)
    
    print(f"--- Verification ---")
    print(f"Ave: {ave['anilla']}")
    print(f"Especie: {ave.get('especie_nombre')}")
    print(f"Fecha Nac.: {ave.get('fecha_nacimiento')}")
    
    # 3. Generate Certificate
    qr_path = os.path.join(TMP_DIR, "verify_qr.png")
    pdf_path = os.path.join(TMP_DIR, "verify_certificado.pdf")
    
    generar_qr(son_uuid, qr_path)
    generar_certificado_pdf(ave, arbol, pdf_path, qr_path)
    
    print(f"PDF generado exitosamente en: {pdf_path}")
    print(f"Por favor, revisa que no aparezcan N/A y que el árbol esté alineado.")

if __name__ == "__main__":
    test_refinements()
