-- IMPORTACIÓN CANARIO DE COLOR

-- 1. VARIEDAD
INSERT INTO variedades VALUES
('var-canario-color','species-canario','Canario de color',CURRENT_TIMESTAMP,NULL,NULL);

-- 2. MUTACIONES
INSERT INTO mutaciones VALUES
('mut-can-negro','Negro','Base melánica','melanina',1,CURRENT_TIMESTAMP,NULL,NULL),
('mut-can-bronce','Bronce','Base melánica','melanina',1,CURRENT_TIMESTAMP,NULL,NULL),
('mut-can-agata','Ágata','Ligada al sexo','melanina',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-can-isabela','Isabela','Ligada al sexo','melanina',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-can-opal','Ópalo','Autosómica recesiva','estructura',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-can-satine','Satiné','Ligada al sexo','melanina',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-can-pastel','Pastel','Autosómica recesiva','dilución',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-can-topacio','Topacio','Autosómica recesiva','estructura',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-can-onyx','Onyx','Autosómica recesiva','estructura',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-can-eumo','Eumo','Autosómica recesiva','estructura',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-can-feo','Feo','Autosómica recesiva','estructura',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-can-cobalto','Cobalto','Autosómica recesiva','estructura',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-can-rojo','Rojo','Lipocrómico','lipocromo',1,CURRENT_TIMESTAMP,NULL,NULL),
('mut-can-amarillo','Amarillo','Lipocrómico','lipocromo',1,CURRENT_TIMESTAMP,NULL,NULL),
('mut-can-blanco-dom','Blanco dominante','Autosómica dominante','lipocromo',1,CURRENT_TIMESTAMP,NULL,NULL),
('mut-can-blanco-rec','Blanco recesivo','Autosómica recesiva','lipocromo',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-can-marfil','Marfil','Ligada al sexo','lipocromo',0,CURRENT_TIMESTAMP,NULL,NULL),
('mut-can-mosaico','Mosaico','Poligénica','distribución',0,CURRENT_TIMESTAMP,NULL,NULL);

-- 3. RELACIÓN VARIEDAD-MUTACIONES
INSERT INTO variedad_mutaciones VALUES
('vm-c1','var-canario-color','mut-can-negro',CURRENT_TIMESTAMP,NULL,NULL),
('vm-c2','var-canario-color','mut-can-bronce',CURRENT_TIMESTAMP,NULL,NULL),
('vm-c3','var-canario-color','mut-can-agata',CURRENT_TIMESTAMP,NULL,NULL),
('vm-c4','var-canario-color','mut-can-isabela',CURRENT_TIMESTAMP,NULL,NULL),
('vm-c5','var-canario-color','mut-can-opal',CURRENT_TIMESTAMP,NULL,NULL),
('vm-c6','var-canario-color','mut-can-satine',CURRENT_TIMESTAMP,NULL,NULL),
('vm-c7','var-canario-color','mut-can-pastel',CURRENT_TIMESTAMP,NULL,NULL),
('vm-c8','var-canario-color','mut-can-topacio',CURRENT_TIMESTAMP,NULL,NULL),
('vm-c9','var-canario-color','mut-can-onyx',CURRENT_TIMESTAMP,NULL,NULL),
('vm-c10','var-canario-color','mut-can-eumo',CURRENT_TIMESTAMP,NULL,NULL),
('vm-c11','var-canario-color','mut-can-feo',CURRENT_TIMESTAMP,NULL,NULL),
('vm-c12','var-canario-color','mut-can-cobalto',CURRENT_TIMESTAMP,NULL,NULL),
('vm-c13','var-canario-color','mut-can-rojo',CURRENT_TIMESTAMP,NULL,NULL),
('vm-c14','var-canario-color','mut-can-amarillo',CURRENT_TIMESTAMP,NULL,NULL),
('vm-c15','var-canario-color','mut-can-blanco-dom',CURRENT_TIMESTAMP,NULL,NULL),
('vm-c16','var-canario-color','mut-can-blanco-rec',CURRENT_TIMESTAMP,NULL,NULL),
('vm-c17','var-canario-color','mut-can-marfil',CURRENT_TIMESTAMP,NULL,NULL),
('vm-c18','var-canario-color','mut-can-mosaico',CURRENT_TIMESTAMP,NULL,NULL);
