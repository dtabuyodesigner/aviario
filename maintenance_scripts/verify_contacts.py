
import requests
import sys

BASE_URL = 'http://localhost:8080/api/contacts'

def test_contacts_api():
    print("=== Testing Contacts API ===")

    # 1. READ (GET)
    try:
        r = requests.get(BASE_URL)
        if r.status_code == 200:
            contacts = r.json()
            print(f"[OK] GET /api/contacts returned {len(contacts)} contacts.")
            if len(contacts) < 5:
                print(f"[WARN] Expected at least 5 contacts (from seed), found {len(contacts)}")
        else:
            print(f"[FAIL] GET /api/contacts returned {r.status_code}")
            return
    except Exception as e:
        print(f"[FAIL] Connection error: {e}")
        return

    # 2. CREATE (POST)
    new_contact = {
        'tipo': 'Otro',
        'nombre_razon_social': 'Test Contact Auto',
        'telefono': '000-000-000'
    }
    contact_id = None
    try:
        r = requests.post(BASE_URL, json=new_contact)
        if r.status_code == 201:
            data = r.json()
            contact_id = data.get('id')
            print(f"[OK] POST /api/contacts created ID: {contact_id}")
        else:
            print(f"[FAIL] POST /api/contacts returned {r.status_code}: {r.text}")
            return
    except Exception as e:
        print(f"[FAIL] POST error: {e}")
        return

    if not contact_id:
        print("[FAIL] No ID returned from create.")
        return

    # 3. UPDATE (PUT)
    update_data = {
        'tipo': 'Otro',
        'nombre_razon_social': 'Test Contact Auto UPDATED',
        'telefono': '111-111-111'
    }
    try:
        r = requests.put(f"{BASE_URL}/{contact_id}", json=update_data)
        if r.status_code == 200:
            print(f"[OK] PUT /api/contacts/{contact_id} successful.")
        else:
            print(f"[FAIL] PUT /api/contacts/{contact_id} returned {r.status_code}: {r.text}")
    except Exception as e:
        print(f"[FAIL] PUT error: {e}")

    # Verify Update
    try:
        r = requests.get(BASE_URL)
        contacts = r.json()
        updated = next((c for c in contacts if c['id_contacto'] == contact_id), None)
        if updated and updated['nombre_razon_social'] == 'Test Contact Auto UPDATED':
            print("[OK] Verified update via GET.")
        else:
            print("[FAIL] Update verification failed.")
    except Exception as e:
        print(f"[FAIL] Get verification error: {e}")

    # 4. DELETE (DELETE)
    try:
        r = requests.delete(f"{BASE_URL}/{contact_id}")
        if r.status_code == 200:
            print(f"[OK] DELETE /api/contacts/{contact_id} successful.")
        else:
            print(f"[FAIL] DELETE /api/contacts/{contact_id} returned {r.status_code}: {r.text}")
    except Exception as e:
        print(f"[FAIL] DELETE error: {e}")

    # Verify Delete
    try:
        r = requests.get(BASE_URL)
        contacts = r.json()
        deleted = next((c for c in contacts if c['id_contacto'] == contact_id), None)
        if not deleted:
            print("[OK] Verified delete via GET (contact gone).")
        else:
            print("[FAIL] Contact still exists after delete.")
    except Exception as e:
        print(f"[FAIL] Delete verify error: {e}")

    print("=== Test Complete ===")

if __name__ == '__main__':
    test_contacts_api()
