import sqlite3
import os

DB_PATH = 'aviario.db'

def seed_incubation():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Create table
    print("Creating table 'parametros_incubacion'...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS parametros_incubacion (
            id_parametro INTEGER PRIMARY KEY AUTOINCREMENT,
            especie TEXT NOT NULL,
            dias_incubacion TEXT,
            temperatura_incubacion TEXT,
            humedad_incubacion TEXT
        )
    """)

    # 2. Data
    data = [
        ("Periquito australiano", "18", "37,2 - 37,5", "50 - 55"),
        ("Agapornis (inseparables)", "21 - 23", "37,2 - 37,5", "50 - 60"),
        ("Cotorra ninfa (carolina)", "18 - 21", "37,2 - 37,5", "50 - 55"),
        ("Cotorra argentina (monje)", "24 - 28", "37,2 - 37,5", "55 - 60"),
        ("Yaco (gris africano)", "28 - 30", "37,2 - 37,4", "55 - 60"),
        ("Amazonas (todas aprox.)", "24 - 29", "37,2 - 37,4", "55 - 60"),
        ("Eclectus", "26 - 28", "37,2 - 37,4", "55 - 65"),
        ("Pionus", "26 - 28", "37,2 - 37,4", "55 - 60"),
        ("Caique (Pionites)", "24 - 27", "37,2 - 37,5", "55 - 60"),
        ("Guacamayo pequeño", "24 - 26", "37,1 - 37,4", "55 - 60"),
        ("Guacamayo grande", "26 - 28", "37,1 - 37,4", "60 - 65"),
        ("Cacatúa pequeña", "24 - 26", "37,2 - 37,4", "55 - 60"),
        ("Cacatúa grande", "27 - 30", "37,2 - 37,4", "60 - 65"),
        ("Lori / Lorikeet", "23 - 26", "37,2 - 37,5", "55 - 60"),
        ("Rosella", "19 - 22", "37,2 - 37,5", "50 - 55"),
        ("Platycercus (rosellas varias)", "20 - 22", "37,2 - 37,5", "50 - 55"),
        ("Neophema (bourke, turquesa, etc.)", "18 - 20", "37,2 - 37,5", "50 - 55"),
        ("Kakariki", "19 - 21", "37,2 - 37,5", "50 - 55"),
        ("Canario doméstico", "13 - 14", "37,4 - 37,6", "50 - 55"),
        ("Diamante mandarín", "13 - 15", "37,4 - 37,6", "50 - 55"),
        ("Diamante de Gould", "14 - 16", "37,4 - 37,6", "55 - 60"),
        ("Isabelita del Japón", "13 - 15", "37,4 - 37,6", "50 - 55"),
        ("Diamante papagayo", "14 - 15", "37,4 - 37,6", "50 - 55"),
        ("Diamante de cola larga", "14 - 16", "37,4 - 37,6", "50 - 55"),
        ("Diamante bichenow", "13 - 15", "37,4 - 37,6", "50 - 55"),
        ("Estrilda común", "12 - 14", "37,4 - 37,6", "50 - 55"),
        ("Padda o gorrión de Java", "17 - 18", "37,3 - 37,5", "55 - 60"),
        ("Jilguero europeo", "13 - 14", "37,4 - 37,6", "50 - 55"),
        ("Verderón", "13 - 14", "37,4 - 37,6", "50 - 55"),
        ("Lúgano", "13 - 14", "37,4 - 37,6", "50 - 55"),
        ("Camachuelo común", "13 - 14", "37,4 - 37,6", "50 - 55"),
        ("Cardenalito de Venezuela", "13 - 14", "37,4 - 37,6", "50 - 55"),
        ("Pinzón vulgar", "13 - 14", "37,4 - 37,6", "50 - 55")
    ]

    # 3. Insert Data (Clear first to avoid dupes)
    print("Seeding data...")
    cur.execute("DELETE FROM parametros_incubacion")
    
    cur.executemany("""
        INSERT INTO parametros_incubacion (especie, dias_incubacion, temperatura_incubacion, humedad_incubacion)
        VALUES (?, ?, ?, ?)
    """, data)

    conn.commit()
    print(f"Inserted {cur.rowcount} incubation parameters.")
    conn.close()

if __name__ == '__main__':
    seed_incubation()
