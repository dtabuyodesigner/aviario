import { db } from './core/db.js';
import { Router } from './core/router.js';
import { BirdsView } from './modules/birds.js?v=3';
import { ContactsView } from './modules/contacts.js?v=3';
import { BreedingView } from './modules/breeding.js?v=3';
import { HealthView } from './modules/health.js?v=3';
import { InventoryView } from './modules/inventory.js?v=3';
import { FinanceView } from './modules/finance.js?v=3';
import { CalendarView } from './modules/calendar.js?v=3';
import { GalleryView } from './modules/gallery.js?v=3';
import { SettingsView } from './modules/settings.js?v=3';
import { GeneticsView } from './modules/genetics.js?v=3';
import { LegalView } from './modules/legal.js?v=3';

// Dashboard View
const DashboardView = async () => {
    const div = document.createElement('div');
    div.className = 'module-dashboard';
    div.style.cssText = 'padding: 1.5rem;';

    // Fetch data
    let birds = [];
    try {
        birds = await db.getAll('birds');
    } catch (e) {
        console.error("Error loading birds:", e);
    }

    // Calculate statistics
    const activeBirds = birds.filter(b => b.estado === 'Activo' || !b.estado);
    const totalActive = activeBirds.length;
    const males = activeBirds.filter(b => b.sexo === 'M').length;
    const females = activeBirds.filter(b => b.sexo === 'H').length;
    const pending = activeBirds.filter(b => b.sexo === '?').length;
    const forSale = activeBirds.filter(b => b.disponible_venta).length;

    // By status
    const sold = birds.filter(b => b.estado === 'Vendido').length;
    const deceased = birds.filter(b => b.estado === 'Baja').length;
    const transferred = birds.filter(b => b.estado === 'Cedido').length;

    // By species
    const speciesCounts = {};
    activeBirds.forEach(b => {
        const sp = b.especie || 'Sin especificar';
        speciesCounts[sp] = (speciesCounts[sp] || 0) + 1;
    });
    const topSpecies = Object.entries(speciesCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);

    // By origin
    const ownBirds = activeBirds.filter(b => b.origen === 'Propio').length;
    const externalBirds = activeBirds.filter(b => b.origen === 'Externo').length;

    // Recent activity (last 10)
    const recentBirds = [...birds]
        .sort((a, b) => (b.id_ave || 0) - (a.id_ave || 0))
        .slice(0, 10);

    div.innerHTML = `
        <div style="margin-bottom: 2rem;">
            <h1 style="font-size: 2rem; color: var(--primary-color); margin: 0 0 0.5rem 0;">Dashboard</h1>
            <p style="color: var(--text-secondary); margin: 0;">Resumen general de tu aviario</p>
        </div>

        <!-- Stats Cards -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
            <!-- Total Active -->
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: var(--radius-lg); color: white; box-shadow: var(--shadow-md);">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">Ejemplares Activos</p>
                        <p style="margin: 0.5rem 0 0 0; font-size: 2.5rem; font-weight: 700;">${totalActive}</p>
                    </div>
                    <div style="font-size: 3rem; opacity: 0.3;">🐦</div>
                </div>
            </div>

            <!-- By Sex -->
            <div style="background: white; padding: 1.5rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border: 1px solid var(--border-color);">
                <p style="margin: 0 0 1rem 0; font-weight: 600; color: var(--text-primary);">Por Sexo</p>
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <div style="flex: 1; min-width: 60px;">
                        <p style="margin: 0; font-size: 0.75rem; color: var(--text-secondary);">Machos</p>
                        <p style="margin: 0.25rem 0 0 0; font-size: 1.5rem; font-weight: 700; color: #1e40af;">♂ ${males}</p>
                    </div>
                    <div style="flex: 1; min-width: 60px;">
                        <p style="margin: 0; font-size: 0.75rem; color: var(--text-secondary);">Hembras</p>
                        <p style="margin: 0.25rem 0 0 0; font-size: 1.5rem; font-weight: 700; color: #be185d;">♀ ${females}</p>
                    </div>
                    <div style="flex: 1; min-width: 60px;">
                        <p style="margin: 0; font-size: 0.75rem; color: var(--text-secondary);">Pendiente</p>
                        <p style="margin: 0.25rem 0 0 0; font-size: 1.5rem; font-weight: 700; color: #64748b;">? ${pending}</p>
                    </div>
                </div>
            </div>

            <!-- For Sale -->
            <div style="background: white; padding: 1.5rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border: 1px solid var(--border-color);">
                <p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);">Disponibles Cesión</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 2.5rem; font-weight: 700; color: #10b981;">${forSale}</p>
            </div>

            <!-- Status Summary -->
            <div style="background: white; padding: 1.5rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border: 1px solid var(--border-color);">
                <p style="margin: 0 0 1rem 0; font-weight: 600; color: var(--text-primary);">Estados</p>
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 0.85rem; color: var(--text-secondary);">Vendidos</span>
                        <span style="font-weight: 600; color: #1e40af;">${sold}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 0.85rem; color: var(--text-secondary);">Cedidos</span>
                        <span style="font-weight: 600; color: #92400e;">${transferred}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 0.85rem; color: var(--text-secondary);">Bajas</span>
                        <span style="font-weight: 600; color: #991b1b;">${deceased}</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Charts Section -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
            <!-- Species Distribution -->
            <div style="background: white; padding: 1.5rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border: 1px solid var(--border-color);">
                <h3 style="margin: 0 0 1rem 0; font-size: 1.1rem;">Distribución por Especie</h3>
                <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                    ${topSpecies.map(([species, count]) => {
        const percentage = totalActive > 0 ? (count / totalActive * 100).toFixed(1) : 0;
        return `
                            <div>
                                <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                                    <span style="font-size: 0.85rem; color: var(--text-primary);">${species}</span>
                                    <span style="font-size: 0.85rem; font-weight: 600; color: var(--primary-color);">${count} (${percentage}%)</span>
                                </div>
                                <div style="background: #f1f5f9; height: 8px; border-radius: 4px; overflow: hidden;">
                                    <div style="background: linear-gradient(90deg, var(--primary-color), var(--secondary-color)); height: 100%; width: ${percentage}%; transition: width 0.3s;"></div>
                                </div>
                            </div>
                        `;
    }).join('')}
                </div>
            </div>

            <!-- Origin Distribution -->
            <div style="background: white; padding: 1.5rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border: 1px solid var(--border-color);">
                <h3 style="margin: 0 0 1rem 0; font-size: 1.1rem;">Origen de Ejemplares</h3>
                <div style="display: flex; gap: 1rem; align-items: center; justify-content: center; height: 150px;">
                    <div style="text-align: center;">
                        <div style="width: 100px; height: 100px; border-radius: 50%; background: linear-gradient(135deg, #10b981, #059669); display: flex; align-items: center; justify-content: center; color: white; font-size: 2rem; font-weight: 700; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);">
                            ${ownBirds}
                        </div>
                        <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem; color: var(--text-secondary);">Propio</p>
                    </div>
                    <div style="text-align: center;">
                        <div style="width: 100px; height: 100px; border-radius: 50%; background: linear-gradient(135deg, #f59e0b, #d97706); display: flex; align-items: center; justify-content: center; color: white; font-size: 2rem; font-weight: 700; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);">
                            ${externalBirds}
                        </div>
                        <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem; color: var(--text-secondary);">Externo</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Quick Actions -->
        <div style="background: white; padding: 1.5rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border: 1px solid var(--border-color); margin-bottom: 2rem;">
            <h3 style="margin: 0 0 1rem 0; font-size: 1.1rem;">Accesos Rápidos</h3>
            <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                <a href="#/birds" class="btn btn-primary" style="text-decoration: none;">📋 Ver Inventario</a>
                <a href="#/contacts" class="btn" style="text-decoration: none; border: 1px solid var(--border-color);">👥 Gestionar Contactos</a>
                <a href="#/breeding" class="btn" style="text-decoration: none; border: 1px solid var(--border-color); background: var(--secondary-color); color: white;">🥚 Control de Cría</a>
            </div>
        </div>

        <!-- Recent Activity -->
        <div style="background: white; padding: 1.5rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border: 1px solid var(--border-color);">
            <h3 style="margin: 0 0 1rem 0; font-size: 1.1rem;">Actividad Reciente</h3>
            <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                ${recentBirds.length > 0 ? recentBirds.map(bird => `
                    <div style="display: flex; align-items: center; gap: 1rem; padding: 0.75rem; border-radius: var(--radius-md); background: #f9fafb; border: 1px solid var(--border-color);">
                        <div style="width: 40px; height: 40px; border-radius: 50%; overflow: hidden; background: #e5e7eb; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                            ${bird.foto_path ?
            `<img src="/${bird.foto_path}" style="width: 100%; height: 100%; object-fit: cover;">` :
            '<span style="font-size: 1.2rem;">🐦</span>'}
                        </div>
                        <div style="flex: 1; min-width: 0;">
                            <p style="margin: 0; font-weight: 600; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${bird.anilla}</p>
                            <p style="margin: 0; font-size: 0.85rem; color: var(--text-secondary);">${bird.especie || 'Sin especie'} • ${bird.sexo === 'M' ? 'Macho' : bird.sexo === 'H' ? 'Hembra' : 'Pendiente'}</p>
                        </div>
                        <a href="#/birds" style="text-decoration: none; color: var(--primary-color); font-size: 0.85rem; font-weight: 500; white-space: nowrap;">Ver →</a>
                    </div>
                `).join('') : '<p style="color: var(--text-secondary); text-align: center; padding: 2rem 0;">No hay ejemplares registrados aún.</p>'}
            </div>
        </div>

        <!-- Export Section -->
        <div style="background: white; padding: 1.5rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border: 1px solid var(--border-color); margin-top: 2rem;">
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.1rem;">Seguridad de Datos</h3>
            <p style="color: var(--text-secondary); margin: 0 0 1rem 0; font-size: 0.9rem;">Descarga una copia de seguridad de tu aviario.</p>
            <button id="btn-export-db" class="btn" style="border: 1px solid var(--border-color); background: white;">
                ⬇️ Descargar Base de Datos (.db)
            </button>
        </div>
    `;

    // Export Handler
    div.querySelector('#btn-export-db').addEventListener('click', async () => {
        try {
            const data = await db.exportDatabase();
            const blob = new Blob([data], { type: 'application/x-sqlite3' });
            const url = URL.createObjectURL(blob);

            const a = document.createElement('a');
            a.href = url;
            a.download = `aviario_backup_${new Date().toISOString().slice(0, 10)}.db`;
            a.click();

            URL.revokeObjectURL(url);
            alert("Base de datos .db descargada correctamente.");
        } catch (err) {
            console.error("Export failed", err);
            alert("Error al exportar datos: " + err.message);
        }
    });

    return div;
};

const initApp = async () => {
    console.log("Initializing Project Aviario...");

    // 1. Init Database
    try {
        await db.init();
    } catch (err) {
        console.error("Failed to initialize database:", err);
        alert("Error crítico: No se pudo abrir la base de datos.");
        return;
    }

    // 2. Init Router
    const mainView = document.getElementById('main-view');
    const routes = {
        '/dashboard': DashboardView,
        '/birds': BirdsView,
        '/contacts': ContactsView,

        '/breeding': BreedingView,
        '/health': HealthView,
        '/inventory': InventoryView,
        '/finance': FinanceView,
        '/calendar': CalendarView,
        '/gallery': GalleryView,
        '/genetics': GeneticsView,
        '/settings': SettingsView,
        '/legal': LegalView
    };

    const router = new Router(routes, mainView);
};

// Start
initApp();
