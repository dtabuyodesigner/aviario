-- IMPORTACIÓN CATÁLOGO COMPLETO PERIQUITO AUSTRALIANO

-- 1. VARIEDAD
INSERT INTO variedades VALUES
('var-periquito','species-periquito','Melopsittacus undulatus',CURRENT_TIMESTAMP,NULL,NULL);

-- 2. MUTACIONES
INSERT INTO mutaciones VALUES
('mut-budgie-verde','Verde ancestral','Ninguna',NULL,1,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-azul','Azul','Autosómica recesiva','psitacina',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-dark','Dark factor','Autosómica dominante','estructura',1,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-violet','Violet factor','Autosómica dominante','estructura',1,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-grey','Grey factor','Autosómica dominante','estructura',1,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-spangle','Spangle','Autosómica dominante','patrón',1,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-lutino','Lutino','Ligada al sexo','ino',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-albino','Albino','Ligada al sexo','ino',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-opaline','Opalino','Ligada al sexo','patrón',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-cinnamon','Canela','Ligada al sexo','eumelanina',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-clearwing','Clearwing','Autosómica recesiva','estructura',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-greywing','Greywing','Autosómica recesiva','estructura',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-dilute','Dilute','Autosómica recesiva','dilución',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-pied-dominant','Dominant pied','Autosómica dominante','patrón',1,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-pied-recessive','Recessive pied','Autosómica recesiva','patrón',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-yellowface','Yellowface','Autosómica recesiva','facial',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-goldenface','Goldenface','Autosómica recesiva','facial',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-slate','Slate','Autosómica recesiva','estructura',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-anthracite','Anthracite','Autosómica dominante','estructura',1,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-fallow','Fallow','Autosómica recesiva','eumelanina',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-texas-clearbody','Texas clearbody','Ligada al sexo','estructura',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-budgie-european-yellowface','European yellowface','Autosómica recesiva','facial',0,CURRENT_TIMESTAMP,NULL,NULL);

-- 3. RELACIÓN VARIEDAD-MUTACIONES
INSERT INTO variedad_mutaciones VALUES
('vm-b1','var-periquito','mut-budgie-verde',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b2','var-periquito','mut-budgie-azul',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b3','var-periquito','mut-budgie-dark',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b4','var-periquito','mut-budgie-violet',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b5','var-periquito','mut-budgie-grey',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b6','var-periquito','mut-budgie-spangle',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b7','var-periquito','mut-budgie-lutino',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b8','var-periquito','mut-budgie-albino',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b9','var-periquito','mut-budgie-opaline',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b10','var-periquito','mut-budgie-cinnamon',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b11','var-periquito','mut-budgie-clearwing',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b12','var-periquito','mut-budgie-greywing',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b13','var-periquito','mut-budgie-dilute',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b14','var-periquito','mut-budgie-pied-dominant',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b15','var-periquito','mut-budgie-pied-recessive',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b16','var-periquito','mut-budgie-yellowface',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b17','var-periquito','mut-budgie-goldenface',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b18','var-periquito','mut-budgie-slate',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b19','var-periquito','mut-budgie-anthracite',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b20','var-periquito','mut-budgie-fallow',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b21','var-periquito','mut-budgie-texas-clearbody',CURRENT_TIMESTAMP,NULL,NULL),
('vm-b22','var-periquito','mut-budgie-european-yellowface',CURRENT_TIMESTAMP,NULL,NULL);
