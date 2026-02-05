
import requests
import sys

BASE_URL = 'http://localhost:8080/api/contacts'

def test_duplicates():
    print("=== Testing Duplicate Checks ===")

    # 1. Create Base Contact
    contact1 = {
        'tipo': 'Otro',
        'nombre_razon_social': 'Original Contact',
        'telefono': '999-888-777',
        'email': 'unique@email.com'
    }
    
    # Clean up if exists from prev run (optional but good practice)
    # Getting list to find ID to delete would be better, but assuming clean state or append
    
    r = requests.post(BASE_URL, json=contact1)
    if r.status_code == 201:
        id1 = r.json()['id']
        print(f"[OK] Created Base Contact (ID: {id1})")
    elif r.status_code == 409:
        print("[INFO] Base contact already exists, continuing...")
    else:
        print(f"[FAIL] Creating base contact failed: {r.text}")
        return

    # 2. Try Duplicate Phone
    contact2 = {
        'tipo': 'Otro',
        'nombre_razon_social': 'Duplicate Phone Guy',
        'telefono': '999-888-777', # Same phone
        'email': 'other@email.com'
    }
    r = requests.post(BASE_URL, json=contact2)
    if r.status_code == 409:
        print(f"[OK] Duplicate Phone blocked: {r.json()['error']}")
    else:
        print(f"[FAIL] Duplicate Phone NOT blocked! Status: {r.status_code}")

    # 3. Try Duplicate Email
    contact3 = {
        'tipo': 'Otro',
        'nombre_razon_social': 'Duplicate Email Guy',
        'telefono': '111-222-333',
        'email': 'unique@email.com' # Same email
    }
    r = requests.post(BASE_URL, json=contact3)
    if r.status_code == 409:
        print(f"[OK] Duplicate Email blocked: {r.json()['error']}")
    else:
        print(f"[FAIL] Duplicate Email NOT blocked! Status: {r.status_code}")

    # 4. Try Self-Update (Should NOT block)
    # Updating name but keeping same phone/email
    update_data = {
        'tipo': 'Otro',
        'nombre_razon_social': 'Original Contact Renamed',
        'telefono': '999-888-777',
        'email': 'unique@email.com'
    }
    # We need the ID from step 1. If we skipped create because it existed, this test might fail if we don't fetch ID.
    # For now assume step 1 succeeded or we skip.
    if 'id1' in locals():
        r = requests.put(f"{BASE_URL}/{id1}", json=update_data)
        if r.status_code == 200:
            print("[OK] Self-update allowed (as expected)")
        else:
            print(f"[FAIL] Self-update blocked! Status: {r.status_code}")
            
        # Cleanup
        requests.delete(f"{BASE_URL}/{id1}")
        print("[INFO] Cleanup done")

    print("=== Test Complete ===")

if __name__ == '__main__':
    test_duplicates()
