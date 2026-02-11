import sqlite3
import uuid
import re
import csv
import io

DB_PATH = 'database/aviario.db'

species_csv = """scientific_name,common_name,alt_common_names,continent,incubation_days,ringing_days,sexual_dimorphism,typical_clutch_size,mutation_common,tags,notes
Ara ararauna,Blue-and-yellow Macaw,Guacamayo azul y amarillo,America,85,90,yes,1-2,yes,macaw,"large parrot,requires large aviary"
Ara macao,Scarlet Macaw,Guacamayo rojo,America,80-85,90,yes,1-2,yes,macaw,large parrot
Ara chloropterus,Green-winged Macaw,Guacamayo verde,America,80-85,90,yes,1-2,yes,macaw,large parrot
Ara militaris,Military Macaw,Guacamayo militar,America,75-80,90,yes,1-2,yes,macaw,large parrot
Anodorhynchus hyacinthinus,Hyacinth Macaw,Guacamayo jacinto,America,85-90,100,yes,1-2,no,macaw,"very large,high care"
Primolius maracana,Blue-headed Macaw,Maracaná,America,75-80,90,yes,1-2,yes,macaw,medium parrot
Amazona aestiva,Blue-fronted Amazon,Amazona frentiazul,America,24-26,30,partial,2-5,yes,amazon,"parrot,good breeder in captivity"
Amazona amazonica,Orange-winged Amazon,Amazona alinaranja,America,24-26,30,partial,2-5,yes,amazon,parrot
Amazona ochrocephala,Yellow-crowned Amazon,Amazona coroniamarilla,America,24-26,30,partial,2-5,yes,amazon,parrot
Amazona farinosa,Mealy Amazon,Amazona harinosa,America,24-28,30,partial,2-5,yes,amazon,parrot
Amazona albifrons,White-fronted Amazon,Amazona frentiblanca,America,23-26,30,partial,2-5,yes,amazon,parrot
Aratinga solstitialis,Sun Conure,Conuro del sol,America,22-26,25,yes,2-4,yes,conure,small parrot
Aratinga jandaya,Jandaya Conure,Conuro jandaya,America,22-26,25,yes,2-4,yes,conure,small parrot
Eupsittula aurea,Peach-fronted Conure,Conuro cabeza durazno,America,22-26,25,yes,2-4,yes,conure
Psittacara mitratus,Mitred Conure,Conuro mitrado,America,22-26,25,yes,2-4,yes,conure
Pyrrhura molinae,Green-cheeked Conure,Cotorra mejillas verdes,America,23-27,25,partial,3-6,yes,conure,"small parrot,very common in aviculture"
Pyrrhura perlata,Maroon-bellied Conure,Pyrrhura perlada,America,23-27,25,partial,3-6,yes,conure
Pyrrhura frontalis,Red-fronted Conure,Pyrrhura frente roja,America,23-27,25,partial,3-6,yes,conure
Pionus menstruus,Blue-headed Pionus,Loro pionus cabeza azul,America,26-28,30,partial,2-4,no,pionus,medium parrot
Brotogeris jugularis,Orange-chinned Parakeet,Periquito barbinaranja,America,23-26,25,partial,3-6,yes,parakeet,small
Deroptyus accipitrinus,Hawk-headed Parrot,Loro cabeza de halcón,America,23-26,30,yes,2-4,no,parrot,distinctive crest
Psittacus erithacus,African Grey Parrot,Perico gris africano,Africa,28-30,60,partial,1-2,yes,grey parrot,highly intelligent
Psittacus timneh,Timneh African Grey,Gris timneh,Africa,28-30,60,partial,1-2,yes,grey parrot
Agapornis roseicollis,Peach-faced Lovebird,Agapornis cara rosada,Africa,21-23,25,yes,3-6,yes,lovebird,"finch-like parrot,very common in breeding"
Agapornis fischeri,Fischer's Lovebird,Agapornis de Fischer,Africa,21-23,25,yes,3-6,yes,lovebird
Agapornis personatus,Masked Lovebird,Agapornis enmascarado,Africa,21-23,25,yes,3-6,yes,lovebird
Agapornis nigrigenis,Black-cheeked Lovebird,Agapornis mejillas negras,Africa,21-23,25,yes,3-6,yes,lovebird
Agapornis lilianae,Lilian's Lovebird,Agapornis de Lilian,Africa,21-23,25,yes,3-6,yes,lovebird
Poicephalus senegalus,Senegal Parrot,Loro senegal,Africa,24-26,30,partial,2-4,yes,poicephalus
Poicephalus meyeri,Meyer's Parrot,Loro de Meyer,Africa,24-26,30,partial,2-4,no,poicephalus
Psittacula krameri,Ring-necked Parakeet,Cotorra de Kramer,Asia/Africa,18-22,21,yes,3-6,yes,parakeet,very widespread
Psittacula eupatria,Alexandrine Parakeet,Cotorra alejandrina,Asia,23-25,25,yes,2-4,yes,parakeet,large parakeet
Psittacula cyanocephala,Plum-headed Parakeet,Cotorra cabeza ciruela,Asia,21-24,25,yes,2-4,yes,parakeet
Psittacula alexandri,Red-breasted Parakeet,Cotorra bigotuda,Asia,21-24,25,yes,2-4,yes,parakeet
Psittinus cyanurus,Blue-rumped Parrot,Perruche cola azul,Asia,23-25,25,partial,2-4,no,parrot
Melopsittacus undulatus,Budgerigar,Periquito australiano,Australia/Oceania,18-21,25,yes,4-8,yes,budgie,finch-like,extremely common
Nymphicus hollandicus,Cockatiel,Ninfa,Australia/Oceania,18-21,25,yes,2-6,yes,cockatiel,very common in pet trade
Platycercus elegans,Crimson Rosella,Rosella carmesí,Australia,20-23,30,partial,4-6,no,rosella
Platycercus eximius,Eastern Rosella,Rosella oriental,Australia,20-23,30,partial,4-6,no,rosella
Neophema splendida,Scarlet-chested Parrot,Neophema espléndida,Australia,18-21,25,partial,4-6,no,parrotlet
Cacatua galerita,Sulphur-crested Cockatoo,Cacatúa galerita,Australia,25-28,40,yes,1-3,no,cockatoo,large noisy
Cacatua goffiniana,Goffin's Cockatoo,Cacatúa de Goffin,Australia,24-26,40,yes,1-3,no,cockatoo
Eolophus roseicapilla,Galah,Corella rosada,Australia,20-22,30,partial,2-4,no,galah
Erythrura gouldiae,Gouldian Finch,Diamante de Gould,Australia/Oceania,13-14,18,no,4-8,yes,finch,"highly valued,mutations common"
Taeniopygia guttata,Zebra Finch,Zebra finch,Australasia,12-14,18,no,4-8,yes,finch,"very common breeder (sometimes called ""mandarín"" in hobby contexts)"
Lonchura punctulata,Scaly-breasted Munia,Java sparrow/munia,Asia/Australasia,11-14,18,no,4-8,no,finch,aka spice finch variants
Lonchura striata domestica,Society Finch,Bengalese Finch,Asia,12-14,18,no,4-8,yes,finch,commonly used as foster
Serinus canaria,Domestic Canary,Canario,Europe/Africa,13-14,20,no,3-6,yes,canary,extremely common in aviculture
Chloris chloris,European Greenfinch,Verderón,Europe,12-14,20,partial,3-5,no,finch,kept by some breeders
Serinus serinus,European Serin,Verdecillo,Europe,12-14,20,partial,3-5,no,finch,less common but present in some aviaries
Carduelis carduelis,European Goldfinch,Jilguero,Europe,12-14,20,partial,3-5,no,finch,ornamental
Lonchura maja,Ricefield Finch,Mandarín? (regional names),Asia,11-14,18,no,4-8,no,finch,check local naming (alias)
Padda oryzivora,Java Sparrow,Paloma de Java/Amaddeo Asia/Oceania,12-14,18,no,3-6,no,finch,commonly bred"""

# Correcting CSV consistency manually in the string or using a smarter split
# Actually, I'll just use a more permissive split since I can't easily "quote" the raw text from the user's prompt perfectly
# I'll split by commas but join anything beyond index 9 into 'notes'

def extract_first_int(text):
    if not text: return 0
    match = re.search(r'\d+', text)
    return int(match.group()) if match else 0

def import_species():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Ensure columns exist in live DB
    try:
        cur.execute("ALTER TABLE especies ADD COLUMN dimorfismo_sexual TEXT")
        cur.execute("ALTER TABLE especies ADD COLUMN tamano_puesta TEXT")
        cur.execute("ALTER TABLE especies ADD COLUMN notas TEXT")
    except Exception as e:
        pass

    lines = species_csv.strip().split('\n')
    
    count = 0
    for line in lines[1:]:
        p = line.split(',')
        if len(p) < 6: continue
        
        sci_name = p[0]
        common_name_en = p[1]
        alt_name_es = p[2]
        continent = p[3]
        inc_days = extract_first_int(p[4])
        rin_days = extract_first_int(p[5])
        dimorphism = p[6]
        clutch_size = p[7]
        mutation_common = p[8].lower() == 'yes'
        tags = p[9]
        notes = ", ".join(p[10:]) if len(p) > 10 else ""
        
        # Primary key mapping
        nombre_comun = alt_name_es if alt_name_es else common_name_en
        first_tag = tags.split(',')[0] if tags else None
        
        # Generate UUID for the record
        u_id = str(uuid.uuid4())
        
        try:
            cur.execute("""
                INSERT INTO especies (
                    nombre_comun, nombre_cientifico, dias_incubacion, dias_anillado, 
                    continente, uuid, categoria, dimorfismo_sexual, tamano_puesta, notas, tiene_mutaciones
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(nombre_comun) DO UPDATE SET
                    nombre_cientifico = excluded.nombre_cientifico,
                    dias_incubacion = excluded.dias_incubacion,
                    dias_anillado = excluded.dias_anillado,
                    continente = excluded.continente,
                    categoria = excluded.categoria,
                    dimorfismo_sexual = excluded.dimorfismo_sexual,
                    tamano_puesta = excluded.tamano_puesta,
                    notas = excluded.notas,
                    tiene_mutaciones = excluded.tiene_mutaciones
            """, (nombre_comun, sci_name, inc_days, rin_days, continent, u_id, first_tag, dimorphism, clutch_size, notes, mutation_common))
            count += 1
        except Exception as e:
            print(f"Error importing {nombre_comun}: {e}")
            
    conn.commit()
    conn.close()
    print(f"Imported/Updated {count} species with full metadata.")

if __name__ == "__main__":
    import_species()
