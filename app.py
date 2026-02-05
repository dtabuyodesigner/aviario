import os
import sqlite3
from flask import Flask, jsonify, request, send_from_directory, send_file
from genetics_api import bp as genetics_bp
import datetime
from datetime import datetime, date, timedelta

app = Flask(__name__, static_folder='.')
app.register_blueprint(genetics_bp)

# Configuration
DB_PATH = os.path.join(os.path.dirname(__file__), 'aviario.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
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

def init_db():
    if not os.path.exists(DB_PATH):
        print("Initializing database...")
        conn = get_db_connection()
        with open(SCHEMA_PATH, 'r') as f:
            conn.executescript(f.read())
        conn.close()
        print("Database initialized.")

# Routes for Frontend
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

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
        
    conn = get_db_connection()
    try:
        cur = conn.cursor()

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

    try:
        cur = conn.cursor()

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
                precio = data.get('precio', 0)
                notas = data.get(
                    'motivo_salida',
                    f"Cambio de estado a {new_status}"
                )

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
            data.get('tipo', 'Curativo'),
            data.get('fecha_inicio'),
            data.get('fecha_fin'),
            data.get('sintomas'),
            data.get('diagnostico'),
            data.get('observaciones'),
            data.get('estado', 'Activo'),
            data.get('resultado')
        ))
        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return jsonify({'id': new_id}), 201
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
        return jsonify({'error': str(e)}), 400

@app.route('/api/backup', methods=['GET'])
def download_backup():
    try:
        return send_file(DB_PATH, as_attachment=True, download_name=f'aviario_backup_{datetime.datetime.now().strftime("%Y%m%d")}.db')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/restore', methods=['POST'])
def restore_backup():
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

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8080)
