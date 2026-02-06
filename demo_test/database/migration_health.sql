
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
