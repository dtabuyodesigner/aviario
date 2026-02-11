-- ENRIQUECIMIENTO CANARIOS: CANARIAS DE CANTO Y POSTURA

-- 1. Backup de la tabla antigua
ALTER TABLE canary_breeds RENAME TO canary_breeds_old;

-- 2. TABLA RAZA DE CANARIOS (ESQUEMA SOLICITADO)
CREATE TABLE canary_breeds (
    uuid TEXT PRIMARY KEY,
    variedad_uuid TEXT,
    nombre TEXT,
    tipo TEXT,
    created_at TEXT,
    updated_at TEXT,
    deleted_at TEXT
);

-- 3. VARIEDADES CANTO Y POSTURA
INSERT INTO variedades VALUES
('var-canario-canto','species-canario','Canario de canto',CURRENT_TIMESTAMP,NULL,NULL),
('var-canario-postura','species-canario','Canario de postura',CURRENT_TIMESTAMP,NULL,NULL);

-- 4. CANARIOS DE CANTO
INSERT INTO canary_breeds (uuid, variedad_uuid, nombre, tipo, created_at) VALUES
('breed-harz','var-canario-canto','Harz Roller','Canto',CURRENT_TIMESTAMP),
('breed-malinois','var-canario-canto','Malinois','Canto',CURRENT_TIMESTAMP),
('breed-waterslager','var-canario-canto','Waterslager','Canto',CURRENT_TIMESTAMP),
('breed-timbrado','var-canario-canto','Timbrado español','Canto',CURRENT_TIMESTAMP);

-- 5. CANARIOS DE POSTURA
INSERT INTO canary_breeds (uuid, variedad_uuid, nombre, tipo, created_at) VALUES
('breed-gloster','var-canario-postura','Gloster','Postura',CURRENT_TIMESTAMP),
('breed-yorkshire','var-canario-postura','Yorkshire','Postura',CURRENT_TIMESTAMP),
('breed-border','var-canario-postura','Border','Postura',CURRENT_TIMESTAMP),
('breed-fife','var-canario-postura','Fife Fancy','Postura',CURRENT_TIMESTAMP),
('breed-lizard','var-canario-postura','Lizard','Postura',CURRENT_TIMESTAMP),
('breed-norwich','var-canario-postura','Norwich','Postura',CURRENT_TIMESTAMP),
('breed-lancashire','var-canario-postura','Lancashire','Postura',CURRENT_TIMESTAMP),
('breed-rizado-paris','var-canario-postura','Rizado parisino','Postura',CURRENT_TIMESTAMP),
('breed-padovano','var-canario-postura','Padovano','Postura',CURRENT_TIMESTAMP),
('breed-gibber','var-canario-postura','Gibber Italicus','Postura',CURRENT_TIMESTAMP),
('breed-scotch','var-canario-postura','Scotch Fancy','Postura',CURRENT_TIMESTAMP),
('breed-munich','var-canario-postura','Munich Fancy','Postura',CURRENT_TIMESTAMP),
('breed-bernois','var-canario-postura','Bernois','Postura',CURRENT_TIMESTAMP),
('breed-hoso','var-canario-postura','Hoso japonés','Postura',CURRENT_TIMESTAMP);
