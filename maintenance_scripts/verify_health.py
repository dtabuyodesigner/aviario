
import requests
import sys

BASE_URL = 'http://localhost:8080/api'

def verify_health():
    print("=== Testing Health Module API ===")

    # 1. Create Recipe
    recipe_data = {
        "nombre_receta": "Test Vitamin",
        "dosis": "1g/L",
        "indicaciones": "Daily",
        "ingredientes": "Vit A, Vit B"
    }
    
    r = requests.post(f"{BASE_URL}/recipes", json=recipe_data)
    if r.status_code != 201:
        print(f"[FAIL] Create Recipe: {r.status_code} {r.text}")
        return
    
    recipe_id = r.json()['id']
    print(f"[OK] Created Recipe ID: {recipe_id}")
    
    # 2. Get Recipes
    r = requests.get(f"{BASE_URL}/recipes")
    recipes = r.json()
    if any(x['id_receta'] == recipe_id for x in recipes):
        print(f"[OK] Recipe found in list. Total recipes: {len(recipes)}")
    else:
        print("[FAIL] Recipe not found in list")

    # 3. Create Bird (Need one for treatment)
    # Actually, let's just assume bird ID 1 exists or fetch one.
    birds = requests.get(f"{BASE_URL}/birds").json()
    if not birds:
        print("[WARN] No birds found to test treatment. Creating dummy bird...")
        b_res = requests.post(f"{BASE_URL}/birds", json={"anilla": "H-TEST-01", "especie": "Canario", "sexo": "M", "estado": "Activo"})
        if b_res.status_code == 201:
             bird_id = b_res.json()['id']
        else:
             print("Failed to create bird.")
             return
    else:
        bird_id = birds[0]['id_ave']

    # 4. Create Treatment
    treatment_data = {
        "id_ave": bird_id,
        "id_receta": recipe_id,
        "tipo": "Preventivo",
        "sintomas": "None (Test)",
        "observaciones": "Auto-test"
    }
    
    r = requests.post(f"{BASE_URL}/treatments", json=treatment_data)
    if r.status_code != 201:
        print(f"[FAIL] Create Treatment: {r.status_code} {r.text}")
        return
        
    treatment_id = r.json()['id']
    print(f"[OK] Created Treatment ID: {treatment_id}")
    
    # 5. Get Active Treatments
    r = requests.get(f"{BASE_URL}/treatments?active=true")
    active = r.json()
    if any(x['id_tratamiento'] == treatment_id for x in active):
         print(f"[OK] Treatment found in Active list.")
    else:
         print("[FAIL] Treatment NOT found in Active list.")
         
    # 6. Delete Test Data
    requests.delete(f"{BASE_URL}/treatments/{treatment_id}")
    requests.delete(f"{BASE_URL}/recipes/{recipe_id}")
    print("[OK] Cleaned up test data.")

    print("=== Health Verification Complete ===")

if __name__ == '__main__':
    verify_health()
