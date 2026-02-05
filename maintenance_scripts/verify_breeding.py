
import requests
import sys

BASE_URL = 'http://localhost:8080/api'

def test_breeding():
    print("=== Testing Breeding API ===")

    # 1. Verify we have some birds (needed for pair)
    try:
        birds = requests.get(f"{BASE_URL}/birds").json()
        if len(birds) < 2:
            print("[SKIP] Not enough birds to test pairing. Skipping.")
            return
        males = [b for b in birds if b['sexo'] == 'M']
        females = [b for b in birds if b['sexo'] == 'H']
        
        if not males or not females:
             print("[SKIP] Need at least 1 Male and 1 Female. Skipping.")
             return
             
        male_id = males[0]['id_ave']
        female_id = females[0]['id_ave']
    except Exception as e:
        print(f"[FAIL] Error fetching birds: {e}")
        return

    # 2. CREATE PAIR
    pair_data = {
        'id_macho': male_id,
        'id_hembra': female_id,
        'variedad_objetivo': 'Test Line',
        'id_ubicacion': None # Optional
    }
    
    pair_id = None
    try:
        r = requests.post(f"{BASE_URL}/pairs", json=pair_data)
        if r.status_code == 201:
            data = r.json()
            pair_id = data.get('id')
            print(f"[OK] Created Pair ID: {pair_id}")
            print(f"     Message: {data.get('message')}")
        else:
            print(f"[FAIL] Create Pair failed: {r.text}")
            return
    except Exception as e:
        print(f"[FAIL] Post Pair error: {e}")
        return

    # 3. VERIFY AUTO-CLUTCH (Regla 1)
    try:
        r = requests.get(f"{BASE_URL}/pairs/{pair_id}/clutches")
        clutches = r.json()
        if len(clutches) > 0:
             print(f"[OK] Automation Success: Found {len(clutches)} clutch(es) for new pair.")
             print(f"     Clutch #1 Status: {clutches[0]['estado']}")
        else:
             print("[FAIL] Automation Failed: No clutch created automatically.")
    except Exception as e:
         print(f"[FAIL] Get Clutches error: {e}")

    # 4. UPDATE CLUTCH (Add Eggs)
    try:
        clutch_id = clutches[0]['id_nidada']
        r = requests.put(f"{BASE_URL}/clutches/{clutch_id}", json={'huevos_totales': 4, 'huevos_fertiles': 3})
        if r.status_code == 200:
            print(f"[OK] Updated Clutch {clutch_id} (Added eggs).")
        else:
            print(f"[FAIL] Update Clutch failed: {r.text}")
    except Exception as e:
        print(f"[FAIL] Update Clutch error: {e}")

    # 5. CLEANUP
    try:
        r = requests.delete(f"{BASE_URL}/pairs/{pair_id}")
        if r.status_code == 200:
            print(f"[OK] Cleanup: Deleted Pair {pair_id} and its clutches.")
        else:
            print(f"[WARN] Cleanup failed: {r.text}")
    except Exception as e:
        print(f"[FAIL] Delete error: {e}")

    print("=== Breeding Test Complete ===")

if __name__ == '__main__':
    test_breeding()
