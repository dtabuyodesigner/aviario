/**
 * Database Service using SQL.js (SQLite via WebAssembly)
 * Persists the binary .db file into IndexedDB for "Auto-Save"
 */

const SQL_JS_URL = 'https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/sql-wasm.js';
const DB_STORE_NAME = 'sqlite_store';
const DB_KEY = 'aviario.db';

class DatabaseService {
    constructor() {
        this.db = null; // The SQL.js Database instance
        this.SQL = null; // The SQL engine
    }

    async init() {
        if (this.db) return;

        // 1. Load SQL.js
        if (!window.initSqlJs) {
            await this._loadScript(SQL_JS_URL);
        }

        this.SQL = await window.initSqlJs({
            // locateFile: file => `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/${file}`
            locateFile: file => `js/lib/${file}`
        });

        // 2. Try load existing DB from storage
        const savedDb = await this._loadFromStorage();

        if (savedDb) {
            this.db = new this.SQL.Database(new Uint8Array(savedDb));
            console.log("Database loaded from persistent storage.");
        } else {
            this.db = new this.SQL.Database();
            console.log("New database created.");
            await this._initSchema();
        }
    }

    async _loadScript(url) {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = url;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    async _initSchema() {
        // Fetch schema.sql content (assuming it's served or we hardcode it for now to avoid fetch issues with file://)
        // For 'file://' protocol, executing fetch might fail due to CORS. 
        // We will hardcode a minimal schema loader or try fetch if running on server.
        // Let's rely on the hardcoded minimal schema first for robustness, or fetch relative.

        const schema = `
            CREATE TABLE IF NOT EXISTS pajaros (
                id_ave INTEGER PRIMARY KEY AUTOINCREMENT,
                anilla TEXT UNIQUE,
                especie TEXT,
                mutacion_visual TEXT,
                sexo TEXT,
                anio INTEGER,
                estado TEXT DEFAULT 'Activo'
            );
            CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY);
            CREATE TABLE IF NOT EXISTS pairs (id INTEGER PRIMARY KEY);
            CREATE TABLE IF NOT EXISTS clutches (id INTEGER PRIMARY KEY);
        `;

        this.db.run(schema);
        await this._saveToStorage();
    }

    // --- Persistence (IndexedDB to store the binary file) ---

    async _saveToStorage() {
        const data = this.db.export();
        const request = indexedDB.open(DB_STORE_NAME, 1);

        return new Promise((resolve, reject) => {
            request.onupgradeneeded = (e) => {
                e.target.result.createObjectStore('files');
            };
            request.onsuccess = (e) => {
                const db = e.target.result;
                const tx = db.transaction(['files'], 'readwrite');
                tx.objectStore('files').put(data, DB_KEY);
                tx.oncomplete = () => resolve();
            };
            request.onerror = (e) => reject(e);
        });
    }

    async _loadFromStorage() {
        const request = indexedDB.open(DB_STORE_NAME, 1);

        return new Promise((resolve, reject) => {
            request.onupgradeneeded = (e) => {
                e.target.result.createObjectStore('files');
            };
            request.onsuccess = (e) => {
                const db = e.target.result;
                const tx = db.transaction(['files'], 'readonly');
                const req = tx.objectStore('files').get(DB_KEY);
                req.onsuccess = () => resolve(req.result);
                req.onerror = () => resolve(null); // Not found is fine
            };
            request.onerror = (e) => {
                console.warn("Storage error", e);
                resolve(null);
            };
        });
    }

    // --- Public API (Compatible-ish with previous API) ---

    async getAll(table) {
        // Map table names if necessary? No, we used 'birds' but schema uses 'pajaros' maybe?
        // Let's normalize.
        const tableName = table === 'birds' ? 'pajaros' : table;

        try {
            const res = this.db.exec(`SELECT * FROM ${tableName}`);
            if (!res.length) return [];

            const columns = res[0].columns;
            const values = res[0].values;

            return values.map(row => {
                const obj = {};
                columns.forEach((col, i) => obj[col] = row[i]);
                return obj;
            });
        } catch (e) {
            console.warn(`Error querying ${tableName}:`, e);
            return [];
        }
    }

    async add(table, data) {
        const tableName = table === 'birds' ? 'pajaros' : table;

        const keys = Object.keys(data);
        const placeholders = keys.map(() => '?').join(',');
        const values = Object.values(data);

        const sql = `INSERT INTO ${tableName} (${keys.join(',')}) VALUES (${placeholders})`;
        this.db.run(sql, values);

        await this._saveToStorage(); // Auto-save after write
    }

    async run(sql, params = []) {
        this.db.run(sql, params);
        await this._saveToStorage();
    }

    async exportDatabase() {
        // Returns the binary array for download
        return this.db.export();
    }
}

export const db = new DatabaseService();
