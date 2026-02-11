-- MIGRACIÓN DE TABLAS DE GENÉTICA
-- 1. Backup de la tabla antigua si existe y tiene el esquema antiguo
ALTER TABLE mutaciones RENAME TO mutaciones_old;

-- 2. TABLAS (UUID – EJECUTA UNA SOLA VEZ)
CREATE TABLE IF NOT EXISTS variedades (
    uuid TEXT PRIMARY KEY,
    especie_uuid TEXT NOT NULL,
    nombre TEXT NOT NULL,
    created_at TEXT,
    updated_at TEXT,
    deleted_at TEXT
);

CREATE TABLE IF NOT EXISTS mutaciones (
    uuid TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    tipo_herencia TEXT,
    locus TEXT,
    dominante INTEGER,
    created_at TEXT,
    updated_at TEXT,
    deleted_at TEXT
);

CREATE TABLE IF NOT EXISTS variedad_mutaciones (
    uuid TEXT PRIMARY KEY,
    variedad_uuid TEXT NOT NULL,
    mutacion_uuid TEXT NOT NULL,
    created_at TEXT,
    updated_at TEXT,
    deleted_at TEXT
);

-- 3. AGAPORNIS (TODOS LOS IMPORTANTES)
-- VARIEDADES
INSERT INTO variedades VALUES
('var-roseicollis','species-agapornis','Agapornis roseicollis',CURRENT_TIMESTAMP,NULL,NULL),
('var-fischeri','species-agapornis','Agapornis fischeri',CURRENT_TIMESTAMP,NULL,NULL),
('var-personatus','species-agapornis','Agapornis personatus',CURRENT_TIMESTAMP,NULL,NULL);

-- MUTACIONES COMUNES AGAPORNIS
INSERT INTO mutaciones VALUES
('mut-verde','Verde ancestral','Ninguna',NULL,1,CURRENT_TIMESTAMP,NULL,NULL),
('mut-azul','Azul','Autosómica recesiva','psitacina',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-lutino','Lutino','Ligada al sexo','ino',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-albino','Albino','Ligada al sexo','ino',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-opalino','Opalino','Ligada al sexo','patrón',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-canela','Canela','Ligada al sexo','eumelanina',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-pastel','Pastel','Autosómica recesiva','dilución',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-pied','Pied','Autosómica dominante','patrón',1,CURRENT_TIMESTAMP,NULL,NULL);

-- ROSEICOLLIS ⇄ MUTACIONES (COMPLETO)
INSERT INTO variedad_mutaciones VALUES
('vm-r1','var-roseicollis','mut-verde',CURRENT_TIMESTAMP,NULL,NULL),
('vm-r2','var-roseicollis','mut-azul',CURRENT_TIMESTAMP,NULL,NULL),
('vm-r3','var-roseicollis','mut-lutino',CURRENT_TIMESTAMP,NULL,NULL),
('vm-r4','var-roseicollis','mut-albino',CURRENT_TIMESTAMP,NULL,NULL),
('vm-r5','var-roseicollis','mut-opalino',CURRENT_TIMESTAMP,NULL,NULL),
('vm-r6','var-roseicollis','mut-canela',CURRENT_TIMESTAMP,NULL,NULL),
('vm-r7','var-roseicollis','mut-pastel',CURRENT_TIMESTAMP,NULL,NULL),
('vm-r8','var-roseicollis','mut-pied',CURRENT_TIMESTAMP,NULL,NULL);

-- FISCHERI ⇄ MUTACIONES
INSERT INTO variedad_mutaciones VALUES
('vm-f1','var-fischeri','mut-verde',CURRENT_TIMESTAMP,NULL,NULL),
('vm-f2','var-fischeri','mut-azul',CURRENT_TIMESTAMP,NULL,NULL),
('vm-f3','var-fischeri','mut-lutino',CURRENT_TIMESTAMP,NULL,NULL),
('vm-f4','var-fischeri','mut-albino',CURRENT_TIMESTAMP,NULL,NULL),
('vm-f5','var-fischeri','mut-opalino',CURRENT_TIMESTAMP,NULL,NULL),
('vm-f6','var-fischeri','mut-canela',CURRENT_TIMESTAMP,NULL,NULL);

-- PERSONATUS ⇄ MUTACIONES
INSERT INTO variedad_mutaciones VALUES
('vm-p1','var-personatus','mut-verde',CURRENT_TIMESTAMP,NULL,NULL),
('vm-p2','var-personatus','mut-azul',CURRENT_TIMESTAMP,NULL,NULL),
('vm-p3','var-personatus','mut-lutino',CURRENT_TIMESTAMP,NULL,NULL),
('vm-p4','var-personatus','mut-albino',CURRENT_TIMESTAMP,NULL,NULL),
('vm-p5','var-personatus','mut-opalino',CURRENT_TIMESTAMP,NULL,NULL);

-- 4. PERIQUITO AUSTRALIANO (COMPLETO)
INSERT INTO mutaciones VALUES
('mut-spangle','Spangle','Autosómica dominante','patrón',1,CURRENT_TIMESTAMP,NULL,NULL),
('mut-ino','Ino','Ligada al sexo','ino',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-arcoiris','Arcoíris','Combinada','múltiple',0,CURRENT_TIMESTAMP,NULL,NULL);

-- 5. NINFA (COMPLETO)
INSERT INTO mutaciones VALUES
('mut-perlado','Perlado','Ligada al sexo','patrón',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-carablanca','Cara blanca','Autosómica recesiva','psitacina',0,CURRENT_TIMESTAMP,NULL,NULL);

-- 6. CANARIOS (BLOQUE PROFESIONAL)
-- MUTACIONES CANARIOS
INSERT INTO mutaciones VALUES
('mut-agata','Ágata','Ligada al sexo','eumelanina',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-isabela','Isabela','Ligada al sexo','eumelanina',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-opalo','Ópalo','Autosómica recesiva','estructura',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-satine','Satiné','Ligada al sexo','eumelanina',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-pastel-can','Pastel','Autosómica recesiva','dilución',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-blanco-dom','Blanco dominante','Autosómica dominante','lipocromo',1,CURRENT_TIMESTAMP,NULL,NULL),
('mut-blanco-rec','Blanco recesivo','Autosómica recesiva','lipocromo',0,CURRENT_TIMESTAMP,NULL,NULL);

-- CATALOGO COMPLETO NINFA
INSERT INTO mutaciones VALUES
('mut-ninfa-gris','Gris ancestral','Ninguna',NULL,1,CURRENT_TIMESTAMP,NULL,NULL),
('mut-ninfa-lutino','Lutino','Ligada al sexo','ino',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-ninfa-albino','Albino','Ligada al sexo','ino',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-ninfa-perlado','Perlado','Ligada al sexo','patrón',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-ninfa-canela','Canela','Ligada al sexo','eumelanina',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-ninfa-carablanca','Cara blanca','Autosómica recesiva','psitacina',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-ninfa-plateado','Plateado','Autosómica recesiva','estructura',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-ninfa-pastel','Pastel','Autosómica recesiva','dilución',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-ninfa-pied','Pied','Autosómica dominante','patrón',1,CURRENT_TIMESTAMP,NULL,NULL),
('mut-ninfa-pearled-cinnamon','Perlado canela','Combinada','múltiple',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-ninfa-lutino-pied','Lutino pied','Combinada','múltiple',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-ninfa-whiteface-pied','Cara blanca pied','Combinada','múltiple',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-ninfa-albino-perlado','Albino perlado','Combinada','múltiple',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-ninfa-fallow','Fallow','Autosómica recesiva','eumelanina',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-ninfa-silver','Silver','Autosómica recesiva','estructura',0,CURRENT_TIMESTAMP,NULL,NULL);

-- ENLAZAR MUTACIONES A NINFA
INSERT INTO variedades VALUES
('var-ninfa','species-ninfa','Nymphicus hollandicus',CURRENT_TIMESTAMP,NULL,NULL);

-- RELACION VARIADES --- MUTACIONES(NINFES)
INSERT INTO variedad_mutaciones VALUES
('vm-n1','var-ninfa','mut-ninfa-gris',CURRENT_TIMESTAMP,NULL,NULL),
('vm-n2','var-ninfa','mut-ninfa-lutino',CURRENT_TIMESTAMP,NULL,NULL),
('vm-n3','var-ninfa','mut-ninfa-albino',CURRENT_TIMESTAMP,NULL,NULL),
('vm-n4','var-ninfa','mut-ninfa-perlado',CURRENT_TIMESTAMP,NULL,NULL),
('vm-n5','var-ninfa','mut-ninfa-canela',CURRENT_TIMESTAMP,NULL,NULL),
('vm-n6','var-ninfa','mut-ninfa-carablanca',CURRENT_TIMESTAMP,NULL,NULL),
('vm-n7','var-ninfa','mut-ninfa-plateado',CURRENT_TIMESTAMP,NULL,NULL),
('vm-n8','var-ninfa','mut-ninfa-pastel',CURRENT_TIMESTAMP,NULL,NULL),
('vm-n9','var-ninfa','mut-ninfa-pied',CURRENT_TIMESTAMP,NULL,NULL),
('vm-n10','var-ninfa','mut-ninfa-pearled-cinnamon',CURRENT_TIMESTAMP,NULL,NULL),
('vm-n11','var-ninfa','mut-ninfa-lutino-pied',CURRENT_TIMESTAMP,NULL,NULL),
('vm-n12','var-ninfa','mut-ninfa-whiteface-pied',CURRENT_TIMESTAMP,NULL,NULL),
('vm-n13','var-ninfa','mut-ninfa-albino-perlado',CURRENT_TIMESTAMP,NULL,NULL),
('vm-n14','var-ninfa','mut-ninfa-fallow',CURRENT_TIMESTAMP,NULL,NULL),
('vm-n15','var-ninfa','mut-ninfa-silver',CURRENT_TIMESTAMP,NULL,NULL);
