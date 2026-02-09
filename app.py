import sys
import os

# --- LOGGING SETUP (AS EARLY AS POSSIBLE) ---
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

import logging
log_file = os.path.join(BASE_DIR, 'app_error.log')
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    filemode='a' # Append mode
)
logging.info("--- APPLICATION STARTUP ---")

import sqlite3
from flask import Flask, jsonify, request, send_from_directory, send_file
from genetics_api import bp as genetics_bp
import datetime
from datetime import datetime, date, timedelta

# Configuration
TRIAL_MODE = True

# Configuration
if getattr(sys, 'frozen', False):
    # Running as PyInstaller EXE
    ASSETS_DIR = sys._MEIPASS
    app = Flask(__name__, static_folder=ASSETS_DIR)
else:
    # Running as normal Python script
    app = Flask(__name__, static_folder='.')
    ASSETS_DIR = BASE_DIR

# Ensure database directory exists in BASE_DIR
DB_FOLDER = os.path.join(BASE_DIR, 'database')
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)

DB_PATH = os.path.join(DB_FOLDER, 'aviario.db')
print(f"DEBUG: BASE_DIR={BASE_DIR}")
print(f"DEBUG: ASSETS_DIR={ASSETS_DIR}")
print(f"DEBUG: DB_PATH={DB_PATH}")

SCHEMA_PATH = os.path.join(ASSETS_DIR, 'database', 'schema.sql')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper to save files
def save_file(file):
    if not file: return None
    import uuid
    from werkzeug.utils import secure_filename
    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex[:8]}_{filename}"
    file.save(os.path.join(UPLOAD_FOLDER, unique_name))
    return f"uploads/{unique_name}"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def filter_data_for_table(table_name, data):
    """Filters dictionary data to only include columns that exist in the target SQLite table."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({table_name})")
        columns = [row['name'] for row in cur.fetchall()]
        conn.close()
        
        # Filter data
        filtered = {k: v for k, v in data.items() if k in columns}
        
        # Log if we ignored something (useful for debug)
        ignored = [k for k in data.keys() if k not in columns]
        if ignored:
            logging.debug(f"Filtrado v2.0: Ignoradas columnas en {table_name}: {ignored}")
            
        return filtered
    except Exception as e:
        logging.error(f"Error filtrando columnas para {table_name}: {e}")
        return data # Fallback to original

def init_db():
    conn = get_db_connection()
    if not os.path.exists(DB_PATH):
        print("Initializing database...")
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        print("Database initialized.")
    else:
        # AUTOMATIC MIGRATIONS v2.0
        print("Checking for migrations (v2.0)...")
        cur = conn.cursor()
        
        # 1. Add missing columns to 'pajaros'
        pajaros_cols = [
            ('reservado', 'BOOLEAN DEFAULT 0'),
            ('id_criador_externo', 'INTEGER'),
            ('precio_compra', 'REAL DEFAULT 0'),
            ('fecha_compra', 'DATE'),
            ('tipo_compra', 'TEXT'),
            ('cites_numero', 'TEXT'),
            ('documento_cesion', 'TEXT')
        ]
        for col, col_type in pajaros_cols:
            try:
                cur.execute(f"SELECT {col} FROM pajaros LIMIT 1")
            except sqlite3.OperationalError:
                print(f"Migration: Adding '{col}' to 'pajaros'")
                cur.execute(f"ALTER TABLE pajaros ADD COLUMN {col} {col_type}")
                conn.commit()
            
        # 2. Add 'es_propio' to 'especies'
        try:
            cur.execute("SELECT es_propio FROM especies LIMIT 1")
        except sqlite3.OperationalError:
            print("Migration: Adding 'es_propio' to 'especies'")
            cur.execute("ALTER TABLE especies ADD COLUMN es_propio BOOLEAN DEFAULT 0")
            conn.commit()

        # 3. Ensure 'configuracion' has all fields
        config_cols = [
            ('telefono', 'TEXT'), ('email', 'TEXT'), ('direccion_calle', 'TEXT'),
            ('direccion_cp', 'TEXT'), ('direccion_poblacion', 'TEXT'),
            ('direccion_provincia', 'TEXT'), ('direccion', 'TEXT'), ('logo_path', 'TEXT'),
            ('dni', 'TEXT'), ('n_criador_nacional', 'TEXT')
        ]
        for col_name, col_type in config_cols:
            try:
                cur.execute(f"SELECT {col_name} FROM configuracion LIMIT 1")
            except sqlite3.OperationalError:
                print(f"Migration: Adding '{col_name}' to 'configuracion'")
                cur.execute(f"ALTER TABLE configuracion ADD COLUMN {col_name} {col_type}")
                conn.commit()

    conn.close()

def check_trial_limit(table, limit, condition=""):
    if not TRIAL_MODE: return True
    try:
        conn = get_db_connection()
        query = f"SELECT count(*) FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        count = conn.execute(query).fetchone()[0]
        conn.close()
        return count < limit
    except Exception as e:
        print(f"Error checking trial limit: {e}")
        return True # Fallback to allow in case of error, though maybe we should block?

# Routes for Frontend
@app.route('/')
def index():
    logging.info("Solicitud recibida en /")
    try:
        path = os.path.join(ASSETS_DIR, 'index.html')
        if not os.path.exists(path):
            logging.error(f"No se encuentra index.html en: {ASSETS_DIR}")
            return f"Error: index.html no encontrado en {ASSETS_DIR}", 404
        return send_from_directory(ASSETS_DIR, 'index.html')
    except Exception as e:
        logging.exception("Error al servir index.html")
        return str(e), 500

@app.route('/<path:path>')
def serve_static(path):
    logging.debug(f"Solicitud de archivo estático: {path}")
    return send_from_directory(ASSETS_DIR, path)

@app.route('/api/ping')
def ping():
    logging.info("Heartbeat/Ping recibido")
    return jsonify({'status': 'ok', 'message': 'Servidor funcionando correctamente'})

@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# API Routes
@app.route('/api/birds', methods=['GET'])
def get_birds():
    conn = get_db_connection()
    # Join with species to get names
    sql = '''
        SELECT p.*, e.nombre_comun as especie 
        FROM pajaros p 
        LEFT JOIN especies e ON p.id_especie = e.id_especie
    '''
    birds = conn.execute(sql).fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in birds])

@app.route('/api/birds', methods=['POST'])
def add_bird():
    # Handle Form Data (Multipart)
    data = request.form.to_dict()
    file = request.files.get('foto')
    
    if file:
        data['foto_path'] = save_file(file)
        
    # --- TRIAL MODE LIMIT ---
    if not check_trial_limit("pajaros", 5, "estado = 'Activo'"):
        return jsonify({'error': 'Límite de la versión de prueba alcanzado (Máx 5 pájaros activos)'}), 403

    conn = get_db_connection()
    try:
        cur = conn.cursor()

        # Bug Fix: Map 'precio' to 'precio_compra'
        if 'precio' in data:
            data['precio_compra'] = data.pop('precio')
        
        # 1. Resolve 'especie' text to 'id_especie'
        # Note: variable name was 'new_bird' in previous context but 'data' here? 
        # Inspecting previous view: Lines 71 uses 'data'. Lines 82 uses 'new_bird'. 
        # ERROR: undefined variable 'new_bird'. CHECK THIS.
        # It seems I must fix the variable name too.
        
        # Fixing variable name 'new_bird' -> 'data'
        if 'especie' in data:
            species_name = data.pop('especie') # Remove 'especie' key, we want 'id_especie'
            
            # Look up ID
            res = cur.execute('SELECT id_especie FROM especies WHERE nombre_comun = ?', (species_name,)).fetchone()
            
            if res:
                data['id_especie'] = res['id_especie']
            else:
                # Optional: Create species if not exists, or error out. 
                # For now, let's auto-create it to be user friendly
                cur.execute('INSERT INTO especies (nombre_comun) VALUES (?)', (species_name,))
                data['id_especie'] = cur.lastrowid

        if 'criador_externo' in data:
            data['id_criador_externo'] = data.pop('criador_externo')

        # --- v2.0 Robust Filtering ---
        data = filter_data_for_table("pajaros", data)

        # 2. Construct SQL dynamically based on remaining keys
        keys = ', '.join(data.keys())
        question_marks = ', '.join(['?'] * len(data))
        values = list(data.values())
        
        sql = f'INSERT INTO pajaros ({keys}) VALUES ({question_marks})'
        
        cur.execute(sql, values)
        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return jsonify({'id': new_id, 'message': 'Bird created successfully'}), 201
    except sqlite3.Error as e:
        conn.close()
        # Print error to console for debugging
        print(f"Error inserting bird: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/birds/<int:id>', methods=['PUT'])
def update_bird(id):

    # Detect multipart o JSON
    if request.content_type and 'multipart/form-data' in request.content_type:
        data = request.form.to_dict()
        file = request.files.get('foto')

        if file:
            data['foto_path'] = save_file(file)

        # --- FIX CHECKBOX ---
        # Aceptar "on", "1", "true", etc.
        data['disponible_venta'] = 1 if str(data.get('disponible_venta', '')).lower() in ['1', 'true', 'on'] else 0
        data['reservado'] = 1 if str(data.get('reservado', '')).lower() in ['1', 'true', 'on'] else 0

    else:
        data = request.json or {}

        # También asegurar conversión si llega JSON
        if 'disponible_venta' in data:
            data['disponible_venta'] = 1 if str(data.get('disponible_venta')).lower() in ['1', 'true'] else 0

        if 'reservado' in data:
            data['reservado'] = 1 if str(data.get('reservado')).lower() in ['1', 'true'] else 0


    conn = get_db_connection()

    conn = get_db_connection()

    try:
        cur = conn.cursor()

        # Bug Fix: Map 'precio' to 'precio_compra' for the bird record
        # Note: If it's a sale, it should be popped and used for movement only.
        # But if it's changing the purchase price after the fact, it's precio_compra.
        # The frontend seems to send 'precio' for both.
        if 'precio' in data:
            # We pop it here to avoid the "no column named precio" error.
            # We'll handle 'precio_compra' explicitly if needed, or re-add it as precio_compra.
            val = data.pop('precio')
            # If not in a sale flow (where we use it for movement), we can update precio_compra
            if 'estado' not in data or data['estado'] == 'Activo':
                data['precio_compra'] = val
            # If it's a sale/cession, 'precio_for_movement' variable above will still get it from the pop result if we saved it?
            precio_for_movement = val
        
        # --- v2.0 Robust Filtering ---
        data = filter_data_for_table("pajaros", data)

        # --- Resolver especie ---
        if 'especie' in data:
            species_name = data.pop('especie')

            res = cur.execute(
                'SELECT id_especie FROM especies WHERE nombre_comun = ?',
                (species_name,)
            ).fetchone()

            if res:
                data['id_especie'] = res['id_especie']
            else:
                cur.execute(
                    'INSERT INTO especies (nombre_comun) VALUES (?)',
                    (species_name,)
                )
                data['id_especie'] = cur.lastrowid

        # --- Obtener estado actual ---
        current_bird = cur.execute(
            'SELECT estado FROM pajaros WHERE id_ave = ?',
            (id,)
        ).fetchone()

        if current_bird:

            current_status = current_bird['estado']
            new_status = data.get('estado', current_status)

            # --- AUTOMATIZACIÓN 1 ---
            # Cambio a estado no activo
            if new_status != 'Activo' and new_status != current_status:

                data['disponible_venta'] = 0
                data['reservado'] = 0

                tipo_evento = (
                    'Venta' if new_status == 'Vendido'
                    else 'Cesión' if new_status == 'Cedido'
                    else 'Baja'
                )

                fecha = data.get(
                    'fecha_salida',
                    datetime.now().strftime('%Y-%m-%d')
                )

                id_contacto = data.get('id_contacto_salida')
                precio = precio_for_movement # Use the popped value
                notas = data.get(
                    'motivo_salida',
                    f"Cambio de estado a {new_status}"
                )

                # --- TRIAL MODE LIMIT: MOVEMENTS ---
                if not check_trial_limit("movimientos", 3):
                    return jsonify({'error': 'Límite de movimientos (ventas/cesiones) alcanzado en la versión de prueba (Máx 3)'}), 403

                cur.execute("""
                    INSERT INTO movimientos
                    (id_ave, tipo_evento, fecha, id_contacto, precio, detalles)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (id, tipo_evento, fecha, id_contacto, precio, notas))


            # --- AUTOMATIZACIÓN 2 ---
            elif new_status != 'Activo':
                data['disponible_venta'] = 0
                data['reservado'] = 0


        # --- UPDATE DINÁMICO ---
        columns = ', '.join(f'{key} = ?' for key in data.keys())
        values = list(data.values())
        values.append(id)

        sql = f'UPDATE pajaros SET {columns} WHERE id_ave = ?'

        cur.execute(sql, values)

        if cur.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Bird not found'}), 404

        conn.commit()
        conn.close()

        return jsonify({'message': 'Bird updated successfully'})

    except sqlite3.Error as e:
        conn.close()
        print(f"Error updating bird: {e}")
        return jsonify({'error': str(e)}), 400


@app.route('/api/birds/<int:id>', methods=['DELETE'])
def delete_bird(id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute('DELETE FROM pajaros WHERE id_ave = ?', (id,))
        if cur.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Bird not found'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Bird deleted successfully'})
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

# Gallery Routes
@app.route('/api/birds/<int:id>/gallery', methods=['GET'])
def get_bird_gallery(id):
    conn = get_db_connection()
    photos = conn.execute('SELECT * FROM bird_photos WHERE id_bird = ? ORDER BY created_at DESC', (id,)).fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in photos])

@app.route('/api/birds/<int:id>/gallery', methods=['POST'])
def add_bird_photo(id):
    if TRIAL_MODE:
        return jsonify({'error': 'La galería está desactivada en la versión de prueba'}), 403
    file = request.files.get('foto')
    if not file:
        return jsonify({'error': 'No file provided'}), 400
    
    path = save_file(file)
    if not path:
        return jsonify({'error': 'File save failed'}), 500
        
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute('INSERT INTO bird_photos (id_bird, file_path) VALUES (?, ?)', (id, path))
        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return jsonify({'id_photo': new_id, 'file_path': path, 'id_bird': id}), 201
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/gallery/<int:photo_id>', methods=['DELETE'])
def delete_bird_photo(photo_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        # Get path to delete file
        photo = cur.execute('SELECT file_path FROM bird_photos WHERE id_photo = ?', (photo_id,)).fetchone()
        
        if photo:
            # Delete record
            cur.execute('DELETE FROM bird_photos WHERE id_photo = ?', (photo_id,))
            conn.commit()
            
            # Try delete file
            full_path = os.path.join(os.path.dirname(__file__), photo['file_path'])
            if os.path.exists(full_path):
                os.remove(full_path)
                
            conn.close()
            return jsonify({'message': 'Photo deleted successfully'})
        else:
            conn.close()
            return jsonify({'error': 'Photo not found'}), 404
            
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 400
@app.route('/api/mutations', methods=['GET'])
def get_mutations():
    species_filter = request.args.get('species')
    conn = get_db_connection()
    
    if species_filter:
        # Case insensitive search
        mutations = conn.execute(
            'SELECT * FROM mutaciones WHERE LOWER(especie_asociada) LIKE LOWER(?) ORDER BY subgrupo, nombre', 
            (f'%{species_filter}%',)
        ).fetchall()
    else:
        mutations = conn.execute('SELECT * FROM mutaciones ORDER BY especie_asociada, subgrupo, nombre').fetchall()
    
    conn.close()
    return jsonify([dict(ix) for ix in mutations])

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    conn = get_db_connection()
    contacts = conn.execute('SELECT * FROM contactos ORDER BY nombre_razon_social').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in contacts])

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    if not check_trial_limit("contactos", 3):
        return jsonify({'error': 'Límite de la versión de prueba alcanzado (Máx 3 contactos)'}), 403
    data = request.json
    conn = get_db_connection()
    try:
        cur = conn.cursor()

        # Duplicate Check (Phone/Email)
        conditions = []
        params = []
        
        if data.get('telefono'):
            conditions.append("telefono = ?")
            params.append(data.get('telefono'))
        
        if data.get('email'):
            conditions.append("email = ?")
            params.append(data.get('email'))

        if conditions:
            # Check if any (OR logic)
            query = f"SELECT id_contacto, nombre_razon_social, telefono, email FROM contactos WHERE {' OR '.join(conditions)}"
            cur.execute(query, params)
            existing = cur.fetchone()
            
            if existing:
                # Determine what matched
                msg = []
                if data.get('telefono') and str(existing['telefono']) == str(data.get('telefono')):
                    msg.append(f"El teléfono '{data.get('telefono')}' ya existe")
                if data.get('email') and str(existing['email']) == str(data.get('email')):
                    msg.append(f"El email '{data.get('email')}' ya existe")
                
                conn.close()
                return jsonify({'error': " / ".join(msg) + f" (Contacto: {existing['nombre_razon_social']})"}), 409

        keys = ', '.join(data.keys())
        question_marks = ', '.join(['?'] * len(data))
        values = list(data.values())
        
        sql = f'INSERT INTO contactos ({keys}) VALUES ({question_marks})'
        cur.execute(sql, values)
        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return jsonify({'id': new_id, 'nombre_razon_social': data.get('nombre_razon_social')}), 201
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    data = request.json
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        
        # Check if contact exists
        cur.execute('SELECT id_contacto FROM contactos WHERE id_contacto = ?', (id,))
        if not cur.fetchone():
            conn.close()
            return jsonify({'error': 'Contact not found'}), 404

        # Duplicate Check (Phone/Email) - Excluding SELF
        conditions = []
        params = []
        
        if data.get('telefono'):
            conditions.append("telefono = ?")
            params.append(data.get('telefono'))
        
        if data.get('email'):
            conditions.append("email = ?")
            params.append(data.get('email'))

        if conditions:
            # Add exemption for self
            query = f"SELECT id_contacto, nombre_razon_social, telefono, email FROM contactos WHERE ({' OR '.join(conditions)}) AND id_contacto != ?"
            params.append(id) # Exclude self
            cur.execute(query, params)
            existing = cur.fetchone()
            
            if existing:
                msg = []
                if data.get('telefono') and str(existing['telefono']) == str(data.get('telefono')):
                    msg.append(f"El teléfono '{data.get('telefono')}' ya existe")
                if data.get('email') and str(existing['email']) == str(data.get('email')):
                    msg.append(f"El email '{data.get('email')}' ya existe")
                
                conn.close()
                return jsonify({'error': " / ".join(msg) + f" (Contacto: {existing['nombre_razon_social']})"}), 409

        # Dynamic Update
        columns = ', '.join(f'{key} = ?' for key in data.keys())
        values = list(data.values())
        values.append(id)

        sql = f'UPDATE contactos SET {columns} WHERE id_contacto = ?'
        cur.execute(sql, values)
        
        conn.commit()
        conn.close()
        return jsonify({'message': 'Contact updated successfully'})
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        
        # Check if used in birds (optional safety check, or let foreign key handle it)
        # For now, simple delete
        cur.execute('DELETE FROM contactos WHERE id_contacto = ?', (id,))
        
        if cur.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Contact not found'}), 404
            
        conn.commit()
        conn.close()
        return jsonify({'message': 'Contact deleted successfully'})
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

# Breeding Routes (Cruces & Nidadas)

# 1. PAREJAS (Cruces)
@app.route('/api/pairs', methods=['GET'])
def get_pairs():
    conn = get_db_connection()
    # Join to get bird details
    sql = '''
        SELECT 
            c.*, 
            m.anilla as macho_anilla, m.mutacion_visual as macho_mutacion, m.foto_path as macho_foto,
            h.anilla as hembra_anilla, h.mutacion_visual as hembra_mutacion, h.foto_path as hembra_foto
        FROM cruces c
        LEFT JOIN pajaros m ON c.id_macho = m.id_ave
        LEFT JOIN pajaros h ON c.id_hembra = h.id_ave
        ORDER BY c.estado, c.id_cruce DESC
    '''
    pairs = conn.execute(sql).fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in pairs])

@app.route('/api/pairs', methods=['POST'])
def add_pair():
    data = request.json
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        
        # Validar Hibridación (Warning frontend, but backend allows it)
        # TODO: Check if compatible species?
        
        sql = '''
            INSERT INTO cruces (id_macho, id_hembra, fecha_union, variedad_objetivo, id_ubicacion, estado)
            VALUES (?, ?, COALESCE(NULLIF(?, ''), DATE('now')), ?, ?, 'Juntos')
        '''
        cur.execute(sql, (
            data.get('id_macho'), 
            data.get('id_hembra'), 
            data.get('fecha_union'), 
            data.get('variedad_objetivo'), 
            data.get('id_ubicacion')
        ))
        
        pair_id = cur.lastrowid
        
        # AUTOMATION: Create First Clutch (Nidada #1) automatically
        sql_nidada = '''
            INSERT INTO nidadas (id_cruce, numero_nidada, estado, huevos_totales) 
            VALUES (?, 1, 'Puesta', 0)
        '''
        cur.execute(sql_nidada, (pair_id,))
        
        conn.commit()
        conn.close()
        return jsonify({'id': pair_id, 'message': 'Pair and first clutch created'}), 201
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/pairs/<int:id>', methods=['PUT'])
def update_pair(id):
    data = request.json
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        
        # Only update specific fields
        # Only update specific fields
        allowed = ['estado', 'fecha_separacion', 'variedad_objetivo', 'id_ubicacion', 'fecha_union', 'id_macho', 'id_hembra']
        updates = []
        values = []
        for k in allowed:
            if k in data:
                updates.append(f"{k} = ?")
                values.append(data[k])
        
        if updates:
            values.append(id)
            sql = f"UPDATE cruces SET {', '.join(updates)} WHERE id_cruce = ?"
            cur.execute(sql, values)
            conn.commit()
            
        conn.close()
        return jsonify({'message': 'Pair updated'})
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/pairs/<int:id>', methods=['DELETE'])
def delete_pair(id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        # Cascade delete (Nidadas -> Cruce) ? 
        # For safety, manual check or let DB fail if FK constraint.
        # Let's delete nidadas first to be clean.
        cur.execute("DELETE FROM nidadas WHERE id_cruce = ?", (id,))
        cur.execute("DELETE FROM cruces WHERE id_cruce = ?", (id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Pair deleted'})
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

# 2. NIDADAS (Clutches)
@app.route('/api/pairs/<int:pair_id>/clutches', methods=['GET'])
def get_clutches(pair_id):
    conn = get_db_connection()
    sql = 'SELECT * FROM nidadas WHERE id_cruce = ? ORDER BY numero_nidada'
    clutches = conn.execute(sql, (pair_id,)).fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in clutches])

@app.route('/api/clutches/<int:id>', methods=['DELETE'])
def delete_clutch(id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM nidadas WHERE id_nidada = ?", (id,))
        if cur.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Clutch not found'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Clutch deleted'})
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/clutches/<int:id>', methods=['PUT'])
def update_clutch(id):
    data = request.json
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        
        columns = ', '.join(f'{key} = ?' for key in data.keys())
        values = list(data.values())
        values.append(id)
        
        sql = f'UPDATE nidadas SET {columns} WHERE id_nidada = ?'
        cur.execute(sql, values)
        
        conn.commit()
        conn.close()
        return jsonify({'message': 'Clutch updated'})
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/clutches', methods=['POST'])
def add_clutch():
    if not check_trial_limit("nidadas", 2):
        return jsonify({'error': 'Límite de la versión de prueba alcanzado (Máx 2 nidadas)'}), 403
    data = request.json
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        sql = '''
            INSERT INTO nidadas (id_cruce, numero_nidada, estado, fecha_primer_huevo)
            VALUES (?, ?, ?, ?)
        '''
        cur.execute(sql, (
            data.get('id_cruce'),
            data.get('numero_nidada'),
            data.get('estado', 'Puesta'),
            data.get('fecha_primer_huevo')
        ))
        row_id = cur.lastrowid
        conn.commit()
        conn.close()
        return jsonify({'id': row_id}), 201
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/birds/<int:id>/history', methods=['GET'])
def get_bird_history(id):
    conn = get_db_connection()
    try:
        # Get Movements
        sql = '''
            SELECT m.*, c.nombre_razon_social as contacto_nombre
            FROM movimientos m
            LEFT JOIN contactos c ON m.id_contacto = c.id_contacto
            WHERE m.id_ave = ?
            ORDER BY m.fecha DESC
        '''
        movements = conn.execute(sql, (id,)).fetchall()
        return jsonify([dict(m) for m in movements])
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

@app.route('/api/breeding', methods=['GET'])
def get_breeding_events():
    if TRIAL_MODE:
        return jsonify([]), 200 # Blank calendar in trial mode
    conn = get_db_connection()
    # Fetch all clutches that have a start date
    # Mapped 'fecha_primer_huevo' -> 'fecha_inicio' for frontend compatibility
    # Join with cruces -> pajaros (hembra) -> especies to get species name
    sql = '''
        SELECT 
            n.id_nidada, 
            n.id_cruce as pareja_id,
            n.fecha_primer_huevo as fecha_inicio,
            n.fecha_inicio_incubacion,
            e.nombre_comun as especie
        FROM nidadas n
        JOIN cruces c ON n.id_cruce = c.id_cruce
        JOIN pajaros ph ON c.id_hembra = ph.id_ave
        LEFT JOIN especies e ON ph.id_especie = e.id_especie
        WHERE n.fecha_primer_huevo IS NOT NULL
    '''
    clutches = conn.execute(sql).fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in clutches])

# Health Routes
# 1. RECIPES (Botiquín)
@app.route('/api/recipes', methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/recipes/<int:id>', methods=['PUT', 'DELETE'])
def recipes_block(id=None):
    if TRIAL_MODE:
        return jsonify({'error': 'El módulo de Salud está desactivado en la versión de prueba'}), 403

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recetas ORDER BY nombre_receta').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in recipes])

@app.route('/api/recipes', methods=['POST'])
def add_recipe():
    data = request.json
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        sql = 'INSERT INTO recetas (nombre_receta, indicaciones, dosis, ingredientes) VALUES (?, ?, ?, ?)'
        cur.execute(sql, (
            data.get('nombre_receta'),
            data.get('indicaciones'),
            data.get('dosis'),
            data.get('ingredientes')
        ))
        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return jsonify({'id': new_id}), 201
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/recipes/<int:id>', methods=['PUT'])
def update_recipe(id):
    data = request.json
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        columns = ', '.join(f'{key} = ?' for key in data.keys())
        values = list(data.values())
        values.append(id)
        
        sql = f'UPDATE recetas SET {columns} WHERE id_receta = ?'
        cur.execute(sql, values)
        conn.commit()
        conn.close()
        return jsonify({'message': 'Recipe updated'})
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    conn = get_db_connection()
    try:
        # Check if used?
        cur = conn.cursor()
        cur.execute('DELETE FROM recetas WHERE id_receta = ?', (id,))
        if cur.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Recipe not found'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Recipe deleted'})
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

# 2. TREATMENTS (Hospital / Historial)
@app.route('/api/treatments', methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/treatments/<int:id>', methods=['PUT', 'DELETE'])
def treatments_block(id=None):
    if TRIAL_MODE:
        return jsonify({'error': 'El módulo de Salud está desactivado en la versión de prueba'}), 403

@app.route('/api/treatments', methods=['GET'])
def get_treatments():
    active_only = request.args.get('active', 'false').lower() == 'true'
    conn = get_db_connection()
    
    sql = '''
        SELECT t.*, p.anilla, r.nombre_receta 
        FROM tratamientos t
        LEFT JOIN pajaros p ON t.id_ave = p.id_ave
        LEFT JOIN recetas r ON t.id_receta = r.id_receta
    '''
    
    if active_only:
        sql += " WHERE t.estado = 'Activo'"
        
    sql += " ORDER BY t.fecha_inicio DESC"
    
    treatments = conn.execute(sql).fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in treatments])

@app.route('/api/treatments', methods=['POST'])
def add_treatment():
    data = request.json
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        sql = '''
            INSERT INTO tratamientos (id_ave, id_receta, tipo, fecha_inicio, fecha_fin, sintomas, diagnostico, observaciones, estado, resultado)
            VALUES (?, ?, ?, COALESCE(NULLIF(?, ''), DATE('now')), ?, ?, ?, ?, ?, ?)
        '''
        cur.execute(sql, (
            data.get('id_ave'),
            data.get('id_receta'),
            data.get('tipo'),
            data.get('fecha_inicio'),
            data.get('fecha_fin'),
            data.get('sintomas'),
            data.get('diagnostico'),
            data.get('observaciones'),
            data.get('estado', 'Activo'),
            data.get('resultado')
        ))
        row_id = cur.lastrowid
        conn.commit()
        conn.close()
        return jsonify({'id': row_id}), 201
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/treatments/<int:id>', methods=['PUT'])
def update_treatment(id):
    data = request.json
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        columns = ', '.join(f'{key} = ?' for key in data.keys())
        values = list(data.values())
        values.append(id)
        
        sql = f'UPDATE tratamientos SET {columns} WHERE id_tratamiento = ?'
        cur.execute(sql, values)
        conn.commit()
        conn.close()
        return jsonify({'message': 'Treatment updated'})
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/treatments/<int:id>', methods=['DELETE'])
def delete_treatment(id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute('DELETE FROM tratamientos WHERE id_tratamiento = ?', (id,))
        if cur.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Treatment not found'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Treatment deleted'})
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 400


# --- CONFIGURATION & SETTINGS ---
@app.route('/api/config', methods=['GET'])
def get_config():
    conn = get_db_connection()
    config = conn.execute('SELECT * FROM configuracion LIMIT 1').fetchone()
    conn.close()
    if config:
        return jsonify(dict(config))
    return jsonify({})

@app.route('/api/config', methods=['POST'])
def save_config():
    data = request.json
    
    # --- v2.0 Robust Filtering ---
    data = filter_data_for_table("configuracion", data)
    
    conn = get_db_connection()
    try:
        # Check if config exists
        exists = conn.execute('SELECT 1 FROM configuracion LIMIT 1').fetchone()
        if exists:
            conn.execute('''
                UPDATE configuracion SET 
                    nombre_criador=?, dni=?, n_criador_nacional=?, direccion=?, logo_path=?, telefono=?, email=?,
                    direccion_calle=?, direccion_poblacion=?, direccion_provincia=?, direccion_cp=?
                WHERE id_config=(SELECT id_config FROM configuracion LIMIT 1)
            ''', (
                data.get('nombre_criador'),
                data.get('dni'),
                data.get('n_criador_nacional'),
                data.get('direccion'),
                data.get('logo_path'),
                data.get('telefono'),
                data.get('email'),
                data.get('direccion_calle'),
                data.get('direccion_poblacion'),
                data.get('direccion_provincia'),
                data.get('direccion_cp')
            ))
        else:
            conn.execute('''
                INSERT INTO configuracion (nombre_criador, dni, n_criador_nacional, direccion, logo_path, telefono, email, direccion_calle, direccion_poblacion, direccion_provincia, direccion_cp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('nombre_criador'),
                data.get('dni'),
                data.get('n_criador_nacional'),
                data.get('direccion'),
                data.get('logo_path'),
                data.get('telefono'),
                data.get('email'),
                data.get('direccion_calle'),
                data.get('direccion_poblacion'),
                data.get('direccion_provincia'),
                data.get('direccion_cp')
            ))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Configuration saved'}), 200
    except sqlite3.Error as e:
        conn.close()
        print(f"Error saving config: {e}") # Log to console
        return jsonify({'error': str(e)}), 400

@app.route('/api/backup', methods=['GET'])
def download_backup():
    if TRIAL_MODE:
        return jsonify({'error': 'Las copias de seguridad están desactivadas en la versión de prueba'}), 403
    try:
        return send_file(DB_PATH, as_attachment=True, download_name=f'aviario_backup_{datetime.datetime.now().strftime("%Y%m%d")}.db')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/restore', methods=['POST'])
def restore_backup():
    if TRIAL_MODE:
        return jsonify({'error': 'La restauración está desactivada en la versión de prueba'}), 403
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        try:
            # Save to a temporary path first? Or directly overwrite?
            # Direct overwrite is risky but requested.
            file.save(DB_PATH)
            return jsonify({'message': 'Database restored successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/incubation-parameters', methods=['GET'])
def get_incubation_parameters():
    conn = get_db_connection()
    params = conn.execute('SELECT * FROM parametros_incubacion').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in params])

import webbrowser
import threading
import time

def open_browser():
    """Wait for server to start and then open the browser."""
    time.sleep(2) # Give the server time to bind the port
    webbrowser.open("http://127.0.0.1:8081")

if __name__ == '__main__':
    print("========================================")
    print("   INICIANDO AVIARIO - ESTABLE (v2.1)")
    print("========================================")
    
    try:
        # Logging errors to a file
        import logging
        log_file = os.path.join(BASE_DIR, 'app_error.log')
        logging.basicConfig(filename=log_file, level=logging.DEBUG, 
                            format='%(asctime)s %(levelname)s: %(message)s')
        logging.info("--- STARTUP HEARTBEAT v2.1 ---")
        print(f"Directorio Base: {BASE_DIR}")
        print(f"Directorio Assets: {ASSETS_DIR}")
        print(f"Iniciando base de datos...")
        
        init_db()
        
        print(f"Servidor arrancando en el puerto 8081")
        print(f"Abriendo navegador automáticamente: http://localhost:8081")
        print("MANTENGA ESTA VENTANA ABIERTA PARA QUE EL PROGRAMA FUNCIONE")
        print("========================================")
        
        # Start browser thread
        threading.Thread(target=open_browser, daemon=True).start()
        
        # Use 8081 in case 8080 is ghosted, and 0.0.0.0 for broader reach
        app.run(host='0.0.0.0', debug=False, port=8081, threaded=True)
        
    except Exception as e:
        import logging
        logging.exception("Failed to start application")
        print(f"\nERROR CRÍTICO AL ARRANCAR: {e}")
        print("\nEl error se ha guardado en 'app_error.log'")
        input("\nPresione ENTER para cerrar...")
    finally:
        print("\nAlicación finalizada.")
        if getattr(sys, 'frozen', False):
            input("\nPresione ENTER para salir...")
