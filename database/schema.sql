-- ESQUEMA DEFINITIVO - PROYECTO AVIARIO
-- Actualizado según petición del usuario

-- 1. CONFIGURACIÓN Y TABLAS MAESTRAS
-- 1. CONFIGURACIÓN Y TABLAS MAESTRAS
CREATE TABLE IF NOT EXISTS configuracion (
    id_config INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_criador TEXT,
    dni TEXT,
    n_criador_nacional TEXT,
    telefono TEXT,
    email TEXT,
    direccion_calle TEXT,
    direccion_cp TEXT,
    direccion_poblacion TEXT,
    direccion_provincia TEXT,
    direccion TEXT, -- Fallback
    logo_path TEXT
);

CREATE TABLE IF NOT EXISTS especies (
    id_especie INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_comun TEXT UNIQUE NOT NULL,
    nombre_cientifico TEXT,
    dias_incubacion INTEGER DEFAULT 21,
    dias_anillado INTEGER DEFAULT 8,
    grupo_genetico TEXT, -- 'Psitácida', 'Canario', 'Exótico', etc.
    categoria TEXT,
    continente TEXT,
    uuid TEXT,
    dimorfismo_sexual TEXT,
    tamano_puesta TEXT,
    notas TEXT,
    tiene_mutaciones BOOLEAN DEFAULT 0
);

-- Tabla Maestra de Mutaciones y Variedades
CREATE TABLE IF NOT EXISTS mutaciones (
    id_mutacion INTEGER PRIMARY KEY AUTOINCREMENT,
    especie_asociada TEXT NOT NULL, -- 'Agapornis Roseicollis', 'Canario', 'Diamante de Gould', etc.
    nombre TEXT NOT NULL,
    tipo_herencia TEXT, -- 'Dominante', 'Recesiva Autosómica', 'Ligada al Sexo', etc.
    subgrupo TEXT, -- Para Canarios: 'Tipo', 'Lipocromo', 'Categoría'.
    locus TEXT, -- Nuevo para motor avanzado
    dominancia INTEGER DEFAULT 0, -- 0=Rec, 2=Dom, etc.
    UNIQUE(especie_asociada, nombre, subgrupo)
);

-- 2. CONTACTOS (Agenda)
CREATE TABLE IF NOT EXISTS contactos (
    id_contacto INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT CHECK(tipo IN ('Comprador', 'Vendedor', 'Veterinario', 'Otro', 'Criador')),
    nombre_razon_social TEXT NOT NULL,
    dni_cif TEXT,
    n_criador TEXT,
    telefono TEXT,
    email TEXT,
    direccion TEXT,
    observaciones TEXT
);

-- 3. UBICACIONES
CREATE TABLE IF NOT EXISTS ubicaciones (
    id_ubicacion INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL, -- Ej: "JAULA-01", "VOLADERA-A"
    tipo TEXT,
    capacidad_maxima INTEGER
);

-- 4. PÁJAROS (Inventario)
-- Estructura fija proporcionada por el usuario
CREATE TABLE IF NOT EXISTS pajaros (
    id_ave INTEGER PRIMARY KEY AUTOINCREMENT,
    anilla TEXT UNIQUE NOT NULL,
    id_especie INTEGER,
    mutacion_visual TEXT,
    portador_de TEXT,
    id_raza TEXT,
    sexo TEXT CHECK(sexo IN ('M', 'H', '?')),
    fecha_nacimiento DATE,
    anio_nacimiento INTEGER,
    origen TEXT CHECK(origen IN ('Propio', 'Externo')),
    
    -- Genealogía
    id_padre INTEGER,
    id_madre INTEGER,
    id_criador_externo INTEGER,
    
    -- Estado y Ubicación
    estado TEXT DEFAULT 'Activo' CHECK(estado IN ('Activo', 'Baja', 'Vendido', 'Cedido')),
    id_ubicacion INTEGER,
    disponible_venta BOOLEAN DEFAULT 0,
    reservado BOOLEAN DEFAULT 0,
    
    -- Campos Legales (Psitácidas Grandes)
    cites_numero TEXT,
    documento_cesion TEXT,
    
    -- Multimedia
    foto_path TEXT,

    -- Datos de Compra (Nuevos)
    precio_compra REAL DEFAULT 0,
    fecha_compra DATE,
    tipo_compra TEXT, -- 'Cesión', 'Compra', 'Regalo'
    
    -- SaaS y v2
    uuid TEXT,
    owner_id TEXT,
    created_at TEXT DEFAULT (DATETIME('now')),
    updated_at TEXT DEFAULT (DATETIME('now')),
    deleted_at TEXT,

    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    observaciones TEXT,

    FOREIGN KEY(id_especie) REFERENCES especies(id_especie),
    FOREIGN KEY(id_padre) REFERENCES pajaros(id_ave),
    FOREIGN KEY(id_madre) REFERENCES pajaros(id_ave),
    FOREIGN KEY(id_criador_externo) REFERENCES contactos(id_contacto),
    FOREIGN KEY(id_ubicacion) REFERENCES ubicaciones(id_ubicacion)
);

-- 5. PAREJAS (Cruces)
CREATE TABLE IF NOT EXISTS cruces (
    id_cruce INTEGER PRIMARY KEY AUTOINCREMENT,
    id_macho INTEGER NOT NULL,
    id_hembra INTEGER NOT NULL,
    fecha_union DATE DEFAULT (DATE('now')),
    fecha_separacion DATE,
    estado TEXT DEFAULT 'Juntos', -- Juntos, Separados
    variedad_objetivo TEXT,
    id_ubicacion INTEGER,

    FOREIGN KEY(id_macho) REFERENCES pajaros(id_ave),
    FOREIGN KEY(id_hembra) REFERENCES pajaros(id_ave),
    FOREIGN KEY(id_ubicacion) REFERENCES ubicaciones(id_ubicacion)
);

-- 6. NIDADAS
CREATE TABLE IF NOT EXISTS nidadas (
    id_nidada INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cruce INTEGER NOT NULL,
    numero_nidada INTEGER, -- 1, 2, 3...
    fecha_primer_huevo DATE,
    
    -- Contadores
    huevos_totales INTEGER DEFAULT 0,
    huevos_fertiles INTEGER DEFAULT 0,
    pollos_nacidos INTEGER DEFAULT 0,
    pollos_anillados INTEGER DEFAULT 0,
    
    estado TEXT DEFAULT 'Incubación', -- Puesta, Incubación, Cría, Finalizada

    FOREIGN KEY(id_cruce) REFERENCES cruces(id_cruce)
);

-- 7. MOVIMIENTOS (Económico / Historial)
CREATE TABLE IF NOT EXISTS movimientos (
    id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_ave INTEGER NOT NULL,
    tipo_evento TEXT NOT NULL CHECK(tipo_evento IN ('Compra', 'Venta', 'Cesión', 'Baja', 'Defunción')),
    fecha DATE DEFAULT (DATE('now')),
    id_contacto INTEGER,
    precio REAL DEFAULT 0,
    gastos_asociados REAL DEFAULT 0,
    detalles TEXT,

    FOREIGN KEY(id_ave) REFERENCES pajaros(id_ave),
    FOREIGN KEY(id_contacto) REFERENCES contactos(id_contacto)
);

-- DATOS INICIALES (ESPECIES)
INSERT OR IGNORE INTO especies (nombre_comun) VALUES ('Agapornis Roseicollis');
INSERT OR IGNORE INTO especies (nombre_comun) VALUES ('Agapornis Personatus');
INSERT OR IGNORE INTO especies (nombre_comun) VALUES ('Agapornis Fischeri');
INSERT OR IGNORE INTO especies (nombre_comun) VALUES ('Canario');

-- 8. RECETAS (Botiquín)
CREATE TABLE IF NOT EXISTS recetas (
    id_receta INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_receta TEXT NOT NULL,
    indicaciones TEXT,
    dosis TEXT,
    ingredientes TEXT -- JSON or Text description
);

-- 9. TRATAMIENTOS (Hospital/Historial)
CREATE TABLE IF NOT EXISTS tratamientos (
    id_tratamiento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_ave INTEGER NOT NULL,
    id_receta INTEGER,
    tipo TEXT CHECK(tipo IN ('Preventivo', 'Curativo', 'Emergencia')),
    fecha_inicio DATE DEFAULT (DATE('now')),
    fecha_fin DATE,
    sintomas TEXT,
    diagnostico TEXT,
    observaciones TEXT,
    
    estado TEXT DEFAULT 'Activo', -- Activo, Finalizado
    resultado TEXT, -- Curado, Baja, Crónico
    
    FOREIGN KEY(id_ave) REFERENCES pajaros(id_ave),
    FOREIGN KEY(id_receta) REFERENCES recetas(id_receta)
);

-- 10. DETALLE DE MUTACIONES POR PÁJARO (v2 - Motor Avanzado)
CREATE TABLE IF NOT EXISTS bird_mutations (
    id TEXT PRIMARY KEY,
    id_ave INTEGER NOT NULL,
    id_mutacion INTEGER NOT NULL,

    expresion TEXT CHECK(expresion IN ('Fenotipica','Genotipica')),
    genotipo TEXT CHECK(genotipo IN ('Homocigoto','Heterocigoto','Portador','Desconocido')),

    created_at TEXT DEFAULT (DATETIME('now')),
    updated_at TEXT DEFAULT (DATETIME('now')),
    deleted_at TEXT,

    FOREIGN KEY(id_ave) REFERENCES pajaros(id_ave),
    FOREIGN KEY(id_mutacion) REFERENCES mutaciones(id_mutacion)
);

-- 11. RAZA DE CANARIOS (v2)
CREATE TABLE IF NOT EXISTS canary_breeds (
    id TEXT PRIMARY KEY,
    id_especie INTEGER,
    nombre_raza TEXT,
    tipo TEXT,
    descripcion TEXT,
    FOREIGN KEY(id_especie) REFERENCES especies(id_especie)
);

-- 12. USUARIOS (SaaS preparation)
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    nombre TEXT,
    email TEXT,
    password_hash TEXT,
    created_at TEXT,
    updated_at TEXT,
    deleted_at TEXT
);
