import sys
import os
import json
import uuid

# Add current directory to path
sys.path.append(os.getcwd())

from app import create_app
from app.extensions import db
from app.models.bird import Pajaro
from app.models.genetics import Especie

app = create_app()

def test_genetics():
    print("\n--- Testing Genetics API ---")
    with app.test_client() as client:
        # Test Species
        resp = client.get('/api/v2/genetics/species')
        if resp.status_code == 200:
            print("[\u2713] GET /api/v2/genetics/species")
            data = resp.get_json()
            print(f"    Found {len(data)} species")
            if len(data) > 0:
                print(f"    First species: {data[0]['nombre_comun']}")
        else:
             print(f"[X] GET /api/v2/genetics/species FAILED: {resp.status_code}")

def test_birds():
    print("\n--- Testing Birds API ---")
    with app.test_client() as client:
        # 1. List Birds
        resp = client.get('/api/v2/birds/')
        if resp.status_code == 200:
            print("[\u2713] GET /api/v2/birds/")
            data = resp.get_json()
            print(f"    Found {len(data)} birds")
        else:
             print(f"[X] GET /api/v2/birds/ FAILED: {resp.status_code}")

        # 2. Create Bird (Simulated)
        # We need a valid species ID. Let's get one first.
        with app.app_context():
            species = Especie.query.first()
            if not species:
                print("[!] No species found, skipping create test")
                return
            species_id = species.id_especie
            
        new_bird = {
            'anilla': f'TEST-{uuid.uuid4().hex[:6]}',
            'id_especie': species_id,
            'estado': 'Activo',
            'sexo': 'M'
        }
        
        resp = client.post('/api/v2/birds/', json=new_bird)
        if resp.status_code == 201:
            print("[\u2713] POST /api/v2/birds/ (Create)")
            bird_data = resp.get_json()
            bird_id = bird_data['id_ave']
            print(f"    Created bird ID: {bird_id}")
            
            # 3. Get Details
            resp = client.get(f'/api/v2/birds/{bird_id}')
            if resp.status_code == 200:
                 print(f"[\u2713] GET /api/v2/birds/{bird_id}")
            else:
                 print(f"[X] GET /api/v2/birds/{bird_id} FAILED")
                 
            # 4. Soft Delete
            resp = client.delete(f'/api/v2/birds/{bird_id}')
            if resp.status_code == 200:
                print(f"[\u2713] DELETE /api/v2/birds/{bird_id}")
                
                # Verify it is soft deleted (deleted_at is set)
                with app.app_context():
                    b = Pajaro.query.get(bird_id)
                    if b.deleted_at:
                         print("    [\u2713] Bird.deleted_at is SET")
                    else:
                         print("    [X] Bird.deleted_at is NOT set")
            else:
                 print(f"[X] DELETE FAILED: {resp.status_code}")
                 
        else:
            print(f"[X] POST /api/v2/birds/ FAILED: {resp.status_code} - {resp.get_data(as_text=True)}")

if __name__ == '__main__':
    print("Starting Verification...")
    test_genetics()
    test_birds()
    print("\nVerification Complete.")
