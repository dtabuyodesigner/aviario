/**
 * Database Service (API Client)
 * Connects to Python/Flask Backend
 */

class DatabaseService {
    constructor() {
        this.baseUrl = '/api';
    }

    async init() {
        console.log("API Service ready.");
        // No local initialization needed for API mode
    }

    async getAll(table) {
        if (table === 'birds') table = 'birds'; // Endpoint is /api/birds

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


    async getMutations(species) {
        if (!species) return [];
        try {
            const response = await fetch(`${this.baseUrl}/mutations?species=${encodeURIComponent(species)}`);
            if (!response.ok) return [];
            return await response.json();
        } catch (e) {
            console.error("Error fetching mutations", e);
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
