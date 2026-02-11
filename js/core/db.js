/**
 * Database Service (API Client)
 * Connects to Python/Flask Backend
 */

class DatabaseService {
    constructor() {
        this.baseUrl = '/api/v2';
    }

    async init() {
        console.log("API Service ready.");
        // No local initialization needed for API mode
    }

    async getAll(table) {
        // v2 endpoints
        if (table === 'birds') table = 'birds';
        // Logic remains similar if endpoints match table names
        // /api/v2/birds works.

        try {
            const response = await fetch(`${this.baseUrl}/${table}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (e) {
            console.error("API Error fetching " + table, e);
            return [];
        }
    }

    async add(table, data) {
        if (table === 'pajaros' || table === 'birds') table = 'birds';

        try {
            const response = await fetch(`${this.baseUrl}/${table}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.error || 'API Error');
            }

            return await response.json();
        } catch (e) {
            console.error("API Error adding to " + table, e);
            throw e;
        }
    }

    async update(table, id, data) {
        if (table === 'pajaros' || table === 'birds') table = 'birds';
        try {
            const response = await fetch(`${this.baseUrl}/${table}/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.error || 'API Error');
            }
            return await response.json();
        } catch (e) {
            console.error("API Error updating " + table, e);
            throw e;
        }
    }

    async delete(table, id) {
        if (table === 'pajaros' || table === 'birds') table = 'birds';
        try {
            const response = await fetch(`${this.baseUrl}/${table}/${id}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.error || 'API Error');
            }
            return await response.json();
        } catch (e) {
            console.error("API Error deleting " + table, e);
            throw e;
        }
    }


    async getVarieties(speciesUuid) {
        try {
            // v2: /api/v2/genetics/varieties?species_uuid=...
            // Note: baseUrl is /api/v2. genetics endpoints are under /genetics prefix.
            // So url should be /api/v2/genetics/varieties
            const url = speciesUuid ? `${this.baseUrl}/genetics/varieties?species_uuid=${speciesUuid}` : `${this.baseUrl}/genetics/varieties`;
            const response = await fetch(url);
            if (!response.ok) return [];
            return await response.json();
        } catch (e) {
            console.error("Error fetching varieties", e);
            return [];
        }
    }

    async getMutations(species, variety_uuid) {
        try {
            let url = `${this.baseUrl}/genetics/mutations`;
            if (variety_uuid) {
                url += `?variety_uuid=${variety_uuid}`;
            } else if (species) {
                url += `?species=${encodeURIComponent(species)}`;
            }
            const response = await fetch(url);
            if (!response.ok) return [];
            return await response.json();
        } catch (e) {
            console.error("Error fetching mutations", e);
            return [];
        }
    }

    async getBreeds(variety_uuid) {
        try {
            // canary_breeds not implemented in v2 config yet!
            // assuming legacy fallback or need to find new endpoint.
            // For now, let's point to /api/v2/genetics/canary_breeds if I implement it, or keep it legacy?
            // User requirement: "All frontend we have".
            // I haven't implemented canary_breeds in v2.
            // I should implement it or route to legacy?
            // But legacy is app.py which is not running if I run run.py?
            // Actually app.py IS legacy code but run.py uses new app factory.
            // Unless I reimplement canary_breeds in v2, it won't work.
            // I will implement stub or reuse genetics?
            // Canary breeds essentially are varieties or mutations in some contexts?
            // In legacy schema `canary_breeds` is a table.

            // I'll leave it pointing to /api/canary_breeds (legacy) for now? No, run.py runs on 8000.
            // If I don't implement it, it 404s.
            // I should implement it quickly in genetics API.

            const url = variety_uuid ? `${this.baseUrl}/genetics/canary_breeds?variety_uuid=${variety_uuid}` : `${this.baseUrl}/genetics/canary_breeds`;
            const response = await fetch(url);
            if (!response.ok) return [];
            return await response.json();
        } catch (e) {
            console.error("Error fetching breeds", e);
            return [];
        }
    }

    // Stub for now
    async exportDatabase() {
        alert("La exportación ahora se realiza copiando el archivo 'aviario.db'");
        return {};
    }
}

export const db = new DatabaseService();
