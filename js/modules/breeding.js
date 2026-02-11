
import { db } from '../core/db.js';

export const BreedingView = async () => {
    const container = document.createElement('div');
    container.className = 'module-breeding';

    container.innerHTML = `
        <div class="module-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
            <div>
                <h1 style="font-size: 1.8rem; color: var(--primary-color);">Cría y Reproducción</h1>
                <p style="color: var(--text-secondary);">Gestión de parejas y nidadas</p>
            </div>
            <button id="btn-new-pair" class="btn btn-primary" style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.2rem;">+</span> Nueva Pareja
            </button>
        </div>

        <!-- Pairs Grid -->
        <div id="pairs-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1.5rem;">
            <p style="grid-column: 1/-1; text-align: center; color: var(--text-secondary);">Cargando parejas...</p>
        </div>

        <!-- New Pair Modal -->
        <div id="modal-pair" class="modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; justify-content: center; align-items: center;">
            <div style="background: white; width: 90%; max-width: 600px; padding: 2rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-xl);">
                <h2 style="margin-top: 0; margin-bottom: 1.5rem; color: var(--text-primary);">Formar Nueva Pareja</h2>
                
                <form id="form-pair" style="display: flex; flex-direction: column; gap: 1.5rem;">
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <!-- Male Selector -->
                        <div>
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500; color: #1e40af;">Macho ♂</label>
                            <select id="select-male" required style="width: 100%; padding: 0.75rem; border: 1px solid var(--border-color); border-radius: var(--radius-sm);">
                                <option value="">Seleccionar Macho...</option>
                            </select>
                        </div>
                        <!-- Female Selector -->
                        <div>
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500; color: #be185d;">Hembra ♀</label>
                            <select id="select-female" required style="width: 100%; padding: 0.75rem; border: 1px solid var(--border-color); border-radius: var(--radius-sm);">
                                <option value="">Seleccionar Hembra...</option>
                            </select>
                        </div>
                    </div>

                    <!-- Hybrid Warning -->
                    <div id="hybrid-warning" style="display: none; padding: 0.75rem; background: #fff7ed; border: 1px solid #fdba74; border-radius: var(--radius-sm); color: #c2410c; font-size: 0.9rem;">
                        ⚠️ <strong>Alerta:</strong> Las especies no coinciden. ¿Confirmar hibridación?
                    </div>

                    <div class="form-group">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Variedad Objetivo / Línea</label>
                        <input type="text" id="objective" placeholder="Ej: Línea Verde Mosaico" style="width: 100%; padding: 0.75rem; border: 1px solid var(--border-color); border-radius: var(--radius-sm);">
                    </div>

                    <div class="form-group">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Ubicación (Jaula)</label>
                        <input type="text" id="location" placeholder="Ej: Jaula 1" style="width: 100%; padding: 0.75rem; border: 1px solid var(--border-color); border-radius: var(--radius-sm);">
                    </div>

                    <div class="form-group">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Fecha de Unión</label>
                        <input type="date" id="pairing-date" style="width: 100%; padding: 0.75rem; border: 1px solid var(--border-color); border-radius: var(--radius-sm);">
                    </div>

                    <div style="display: flex; justify-content: flex-end; gap: 1rem; margin-top: 0.5rem;">
                        <button type="button" id="btn-cancel-pair" class="btn" style="background: transparent; border: 1px solid var(--border-color);">Cancelar</button>
                        <button type="submit" id="btn-save-pair" class="btn btn-primary">Crear Pareja</button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Clutch Management Modal -->
        <div id="modal-clutch" class="modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1001; justify-content: center; align-items: center;">
            <div style="background: white; width: 90%; max-width: 700px; padding: 0; border-radius: var(--radius-lg); box-shadow: var(--shadow-xl); overflow: hidden; display: flex; flex-direction: column; max-height: 90vh;">
                <div style="padding: 1.5rem; background: var(--primary-color); color: white; display: flex; justify-content: space-between; align-items: center;">
                    <h2 style="margin: 0; font-size: 1.25rem;">Gestión de Nidadas</h2>
                    <button class="btn-close-clutch" style="background: none; border: none; color: white; font-size: 1.5rem; cursor: pointer;">&times;</button>
                </div>
                
                <div style="padding: 1.5rem; overflow-y: auto;">
                    <button id="btn-add-clutch" class="btn btn-sm" style="margin-bottom: 1rem; background: #e0e7ff; color: #1e40af; border: none;">+ Nueva Puesta (Siguiente)</button>
                    
                    <div id="clutches-container" style="display: flex; flex-direction: column; gap: 1.5rem;">
                        <!-- Clutches injected here -->
                    </div>
                </div>
            </div>
        </div>
    `;

    // State & Logic
    const grid = container.querySelector('#pairs-grid');
    const modal = container.querySelector('#modal-pair');
    const form = container.querySelector('#form-pair');
    const maleSelect = container.querySelector('#select-male');
    const femaleSelect = container.querySelector('#select-female');
    const warning = container.querySelector('#hybrid-warning');
    const pairStatusWarning = document.createElement('div');
    pairStatusWarning.style.cssText = "display: none; padding: 0.75rem; margin-top: 1rem; border-radius: var(--radius-sm); font-size: 0.9rem;";
    container.querySelector('#form-pair').insertBefore(pairStatusWarning, container.querySelector('.form-group')); // Insert before objective field

    let birds = [];
    let currentPairs = []; // Store loaded pairs for validation
    let incubationParams = []; // Store incubation reference data
    let editingPairId = null; // State for editing

    const loadData = async () => {
        try {
            // Load Pairs
            const resPairs = await fetch('/api/pairs');
            currentPairs = await resPairs.json(); // Store in wider scope

            // Load Birds for Selectors
            const resBirds = await fetch('/api/birds');
            birds = await resBirds.json();

            // Load Incubation Params
            const resInc = await fetch('/api/incubation-parameters');
            if (resInc.ok) incubationParams = await resInc.json();

            renderPairs(currentPairs);
            populateSelectors(birds);
        } catch (e) {
            console.error(e);
            grid.innerHTML = '<p style="color: red;">Error al cargar datos.</p>';
        }
    };

    const renderPairs = (pairs) => {
        grid.innerHTML = '';
        if (pairs.length === 0) {
            grid.innerHTML = `
                <div style="grid-column: 1/-1; text-align: center; padding: 3rem; background: #f8fafc; border-radius: var(--radius-lg); border: 2px dashed var(--border-color);">
                    <p style="color: var(--text-secondary);">No hay parejas formadas.</p>
                </div>
            `;
            return;
        }

        pairs.forEach(p => {
            const card = document.createElement('div');
            card.className = 'pair-card';
            card.style.cssText = `
                background: white; 
                padding: 0; 
                border-radius: var(--radius-lg); 
                box-shadow: var(--shadow-sm); 
                border: 1px solid var(--border-color);
                overflow: hidden;
            `;

            // Helper to render avatar
            const renderAvatar = (label, anilla, photo) => {
                if (photo) {
                    return `
                        <div style="width: 80px; height: 80px; margin: 0 auto; border-radius: 50%; overflow: hidden; border: 3px solid white; box-shadow: var(--shadow-md);">
                            <img src="/${photo}" style="width: 100%; height: 100%; object-fit: cover;">
                        </div>
                     `;
                }
                return `<div style="font-size: 2.5rem;">🐦</div>`;
            };

            card.innerHTML = `
                <div style="padding: 1rem; background: #f8fafc; border-bottom: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; color: var(--text-primary);">Pareja #${p.id_cruce}</span>
                    <span style="background: #dbeafe; color: #1e40af; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">${p.estado}</span>
                </div>
                <div style="padding: 1.5rem; display: flex; justify-content: space-between; align-items: center;">
                    <div style="text-align: center; flex: 1;">
                        ${renderAvatar('Macho', p.macho_anilla, p.macho_foto)} 
                        
                        <p style="margin: 0.5rem 0 0; font-weight: 600; color: #1e40af;">${p.macho_anilla || '?'}</p>
                        <p style="margin: 0; font-size: 0.8rem; color: var(--text-secondary);">Macho</p>
                    </div>
                    <div style="font-size: 1.5rem; color: var(--text-secondary); text-align: center;">
                        <div>❤️</div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 0.2rem;">${p.fecha_union || ''}</div>
                    </div>
                    <div style="text-align: center; flex: 1;">
                         ${renderAvatar('Hembra', p.hembra_anilla, p.hembra_foto)}
                         <p style="margin: 0.5rem 0 0; font-weight: 600; color: #be185d;">${p.hembra_anilla || '?'}</p>
                         <p style="margin: 0; font-size: 0.8rem; color: var(--text-secondary);">Hembra</p>
                    </div>
                </div>
                <div style="padding: 1rem; border-top: 1px solid var(--border-color); display: flex; gap: 0.5rem;">
                    <button class="btn btn-sm btn-manage" data-id="${p.id_cruce}" style="flex: 2; border: 1px solid var(--border-color); background: #eff6ff; color: #1d4ed8;">Gestionar Nidadas →</button>
                    <button class="btn btn-sm btn-edit-pair" data-id="${p.id_cruce}" style="flex: 1; border: 1px solid var(--border-color);" title="Editar">✏️</button>
                    <button class="btn btn-sm btn-delete-pair" data-id="${p.id_cruce}" style="flex: 1; border: 1px solid var(--border-color); color: #ef4444;" title="Eliminar">🗑️</button>
                </div>
            `;
            grid.appendChild(card);
        });

        // Add listeners to buttons
        container.querySelectorAll('.btn-manage').forEach(btn => {
            btn.addEventListener('click', (e) => openClutchModal(btn.getAttribute('data-id')));
        });

        container.querySelectorAll('.btn-delete-pair').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                if (confirm('¿Seguro que quieres eliminar esta pareja? Se borrarán también sus nidadas.')) {
                    const id = btn.getAttribute('data-id');
                    try {
                        const res = await fetch(`/api/pairs/${id}`, { method: 'DELETE' });
                        if (res.ok) loadData();
                        else alert('Error eliminando pareja');
                    } catch (e) { console.error(e); }
                }
            });
        });

        container.querySelectorAll('.btn-edit-pair').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const id = btn.getAttribute('data-id');
                const p = pairs.find(x => x.id_cruce == id);
                if (p) openPairModal(p);
            });
        });
    };

    // Clutch Elements
    const modalClutch = container.querySelector('#modal-clutch');
    const clutchesContainer = container.querySelector('#clutches-container');
    const btnCloseClutch = container.querySelector('.btn-close-clutch');
    const btnAddClutch = container.querySelector('#btn-add-clutch');

    let currentPairId = null;

    // CLUTCH LOGIC
    const openClutchModal = async (pairId) => {
        currentPairId = pairId;
        modalClutch.style.display = 'flex';
        await renderClutches(pairId);
    };

    const renderClutches = async (pairId) => {
        clutchesContainer.innerHTML = 'Cargando...';
        try {
            const res = await fetch(`/api/pairs/${pairId}/clutches`);
            const clutches = await res.json();

            // Determine Species & Incubation Days
            let daysIncubation = 13; // Fallback
            let speciesInfo = null;

            const pair = currentPairs.find(p => p.id_cruce == pairId);
            if (pair) {
                // Find male bird to get species (assume Same species pair, or use Hybrid logic later)
                const male = birds.find(b => b.id_ave == pair.id_macho);
                if (male) {
                    const spName = male.especie;

                    // Find in params (Loose match)
                    // E.g. "Agapornis Roseicollis" matches "Agapornis (inseparables)"? 
                    // Logic: Check if Param Name contains First word of Bird Species? 
                    // Or hardcode mapping.
                    // The user list was specific. "Agapornis (inseparables)"

                    const match = incubationParams.find(p => {
                        const pName = p.especie.toLowerCase();
                        const bName = spName.toLowerCase();
                        // Check exact or partial
                        if (pName === bName) return true;
                        if (pName.includes(bName)) return true; // Param: "Canario doméstico", Bird: "Canario" -> Match? No, p includes b.
                        if (bName.includes('agapornis') && pName.includes('agapornis')) return true;
                        if (bName.includes('canario') && pName.includes('canario')) return true;
                        if (bName.includes('gould') && pName.includes('gould')) return true;
                        if (bName.includes('ninfa') && pName.includes('ninfa')) return true;
                        return false;
                    });

                    if (match) {
                        speciesInfo = match;
                        // Parse days: "21 - 23" -> 22, "18" -> 18
                        const d = match.dias_incubacion.replace(' días', ''); // clean just in case
                        if (d.includes('-')) {
                            const parts = d.split('-').map(x => parseInt(x.trim()));
                            daysIncubation = Math.round((parts[0] + parts[1]) / 2);
                        } else {
                            daysIncubation = parseInt(d);
                        }
                    }
                }
            }

            clutchesContainer.innerHTML = '';

            if (clutches.length === 0) {
                clutchesContainer.innerHTML = '<p>No hay puestas registradas.</p>';
                return;
            }

            clutches.forEach(c => {
                const div = document.createElement('div');
                div.style.cssText = `
                    border: 1px solid var(--border-color);
                    border-radius: var(--radius-md);
                    padding: 1rem;
                    background: #f8fafc;
                `;

                // Calculate Hatch Date
                const start = new Date(c.fecha_primer_huevo || Date.now());
                const hatch = new Date(start);
                hatch.setDate(start.getDate() + daysIncubation);
                const hatchStr = hatch.toLocaleDateString();

                div.innerHTML = `
                    <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                        <span style="font-weight: 700; color: var(--primary-color);">
                            Puesta #${c.numero_nidada} <span style="font-weight: 400; color: #64748b; font-size: 0.9rem;">(${c.estado})</span>
                            <button class="btn-delete-clutch" data-id="${c.id_nidada}" style="border:none; background:none; cursor:pointer; color:#ef4444; margin-left:0.5rem;">🗑️</button>
                        </span>
                        <div style="text-align: right; display: flex; flex-direction: column; gap: 0.25rem; align-items: flex-end;">
                             <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <label style="font-size: 0.85rem; font-weight: 500;">Inicio (Puesta):</label>
                                <input type="date" class="input-date-clutch" data-id="${c.id_nidada}" value="${c.fecha_primer_huevo || ''}" style="border: 1px solid var(--border-color); border-radius: 4px; padding: 2px 5px; font-size: 0.85rem;">
                             </div>
                             <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <label style="font-size: 0.85rem; font-weight: 500;">Eclosión (Real):</label>
                                <input type="date" class="input-hatch-clutch" data-id="${c.id_nidada}" value="${c.fecha_nacimiento || ''}" style="border: 1px solid var(--border-color); border-radius: 4px; padding: 2px 5px; font-size: 0.85rem;">
                             </div>
                             <span style="font-size: 0.8rem; color: var(--text-secondary);">Prevista (~${daysIncubation}d): <strong>${hatchStr}</strong></span>
                             ${speciesInfo ? `<span style="font-size: 0.75rem; color: #64748b;">${speciesInfo.especie} (${speciesInfo.temperatura_incubacion}°C / ${speciesInfo.humedad_incubacion}%)</span>` : ''}
                        </div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
                        <!-- Huevos -->
                        <div class="stat-box">
                            <label>🥚 Huevos</label>
                            <div class="counter-control">
                                <button class="btn-dec" data-id="${c.id_nidada}" data-field="huevos_totales">-</button>
                                <span>${c.huevos_totales || 0}</span>
                                <button class="btn-inc" data-id="${c.id_nidada}" data-field="huevos_totales">+</button>
                            </div>
                        </div>
                        <!-- Fértiles -->
                        <div class="stat-box">
                            <label>🔦 Fértiles</label>
                            <div class="counter-control">
                                <button class="btn-dec" data-id="${c.id_nidada}" data-field="huevos_fertiles">-</button>
                                <span>${c.huevos_fertiles || 0}</span>
                                <button class="btn-inc" data-id="${c.id_nidada}" data-field="huevos_fertiles">+</button>
                            </div>
                        </div>
                        <!-- Nacidos -->
                        <div class="stat-box">
                            <label>🐣 Nacidos</label>
                            <div class="counter-control">
                                <button class="btn-dec" data-id="${c.id_nidada}" data-field="pollos_nacidos">-</button>
                                <span>${c.pollos_nacidos || 0}</span>
                                <button class="btn-inc" data-id="${c.id_nidada}" data-field="pollos_nacidos">+</button>
                            </div>
                        </div>
                        <!-- Anillados -->
                        <div class="stat-box">
                            <label>💍 Anillados</label>
                            <div class="counter-control">
                                <button class="btn-dec" data-id="${c.id_nidada}" data-field="pollos_anillados">-</button>
                                <span>${c.pollos_anillados || 0}</span>
                                <button class="btn-inc" data-id="${c.id_nidada}" data-field="pollos_anillados">+</button>
                            </div>
                        </div>
                    </div>
                `;
                clutchesContainer.appendChild(div);

                // API Helper
                const saveClutchData = async (id, payload) => {
                    try {
                        await fetch(`/api/clutches/${id}`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(payload)
                        });
                        // Update local object to reflect changes without full re-render if possible, but re-render is safer for derived values
                        // actually we can just update 'c' object in memory?
                        Object.assign(c, payload);
                        if (payload.fecha_primer_huevo) renderClutches(pairId); // Re-render for calculation
                    } catch (e) {
                        console.error(e);
                    }
                };

                // Date Change Listeners
                const dateInput = div.querySelector('.input-date-clutch');
                dateInput.addEventListener('change', (e) => {
                    saveClutchData(c.id_nidada, { fecha_primer_huevo: e.target.value });
                });

                const hatchInput = div.querySelector('.input-hatch-clutch');
                hatchInput.addEventListener('change', (e) => {
                    saveClutchData(c.id_nidada, { fecha_nacimiento: e.target.value });
                });

                // Bind Logic for counters
                const updateStat = (field, delta) => {
                    const currentVal = c[field] || 0;
                    const newVal = Math.max(0, currentVal + delta);

                    if (field === 'huevos_fertiles') {
                        const totalEggs = c.huevos_totales || 0;
                        if (newVal > totalEggs) {
                            alert(`Error: No puede haber más huevos fértiles (${newVal}) que totales (${totalEggs}).`);
                            return;
                        }
                    }

                    // Automatic bird registration on incrementing "Anillados"
                    if (field === 'pollos_anillados' && delta > 0) {
                        if (confirm('¿Desea registrar este nuevo pájaro anillado en el sistema?')) {

                            // Determine Species Logic
                            const male = birds.find(b => b.id_ave == pair.id_macho);
                            const female = birds.find(b => b.id_ave == pair.id_hembra);
                            let speciesIdToUse = null;

                            // If both parents are same species, use it.
                            if (male && female && male.id_especie === female.id_especie) {
                                speciesIdToUse = male.id_especie;
                            }
                            // Fallback: If not same, we leave it null for User to decide (Hybrid or explicit choice)
                            // Or default to male's if we wanted. But user said "si es puro o híbrido", implies checking.

                            const birthDate = c.fecha_nacimiento || new Date().toISOString().split('T')[0];

                            import('./birds.js').then(module => {
                                module.openBirdModal({
                                    initialData: {
                                        fecha_nacimiento: birthDate,
                                        padre_uuid: pair.id_macho,
                                        madre_uuid: pair.id_hembra,
                                        id_especie: speciesIdToUse,
                                        estado: 'Activo'
                                    },
                                    onSave: () => {
                                        // Once saved, we update the counter in the clutch
                                        saveClutchData(c.id_nidada, { [field]: newVal });
                                        // Update UI immediately
                                        div.querySelector(`span`).textContent = newVal; // This selector is too broad, but re-render comes next
                                        renderClutches(pairId);
                                    }
                                });
                            });
                            return; // Don't save immediately, wait for modal
                        }
                    }

                    saveClutchData(c.id_nidada, { [field]: newVal });
                    // Visual update
                    const box = div.querySelector(`button[data-field="${field}"]`).parentNode.querySelector('span');
                    if (box) box.textContent = newVal;
                };

                div.querySelectorAll('.btn-dec').forEach(b => {
                    b.onclick = () => updateStat(b.dataset.field, -1);
                });
                div.querySelectorAll('.btn-inc').forEach(b => {
                    b.onclick = () => updateStat(b.dataset.field, 1);
                });

                div.querySelector('.btn-delete-clutch').onclick = async () => {
                    if (confirm('¿Eliminar esta nidada?')) {
                        await fetch(`/api/clutches/${c.id_nidada}`, { method: 'DELETE' });
                        renderClutches(pairId);
                    }
                };
            });
        } catch (e) {
            clutchesContainer.innerHTML = 'Error cargando nidadas.';
        }
    };

    btnAddClutch.addEventListener('click', async () => {
        if (!currentPairId) return;
        const count = clutchesContainer.children.length + 1;

        try {
            await fetch('/api/clutches', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    id_cruce: currentPairId,
                    numero_nidada: count,
                    estado: 'Puesta',
                    fecha_primer_huevo: new Date().toISOString().split('T')[0]
                })
            });
            renderClutches(currentPairId);
        } catch (e) {
            alert("Error creando nueva puesta");
        }
    });

    btnCloseClutch.addEventListener('click', () => {
        modalClutch.style.display = 'none';
        currentPairId = null;
    });

    // Styles for counters
    const style = document.createElement('style');
    style.innerHTML = `
        .stat-box label { display: block; font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.25rem; }
        .counter-control { display: flex; align-items: center; gap: 0.5rem; background: white; border: 1px solid var(--border-color); border-radius: 4px; padding: 0.25rem; }
        .counter-control button { width: 24px; height: 24px; border: none; background: #e2e8f0; border-radius: 4px; cursor: pointer; font-weight: bold; }
        .counter-control span { flex: 1; text-align: center; font-weight: 600; }
    `;
    container.appendChild(style);

    const populateSelectors = (allBirds) => {
        const males = allBirds.filter(b => b.sexo === 'M' && b.estado === 'Activo');
        const females = allBirds.filter(b => b.sexo === 'H' && b.estado === 'Activo');

        maleSelect.innerHTML = '<option value="">Seleccionar Macho...</option>';
        femaleSelect.innerHTML = '<option value="">Seleccionar Hembra...</option>';

        males.forEach(m => {
            maleSelect.innerHTML += `<option value="${m.id_ave}" data-species="${m.especie}">${m.anilla} - ${m.especie}</option>`;
        });
        females.forEach(f => {
            femaleSelect.innerHTML += `<option value="${f.id_ave}" data-species="${f.especie}">${f.anilla} - ${f.especie}</option>`;
        });
    };

    // Hybrid Check
    const checkHybrid = () => {
        const m = maleSelect.options[maleSelect.selectedIndex];
        const f = femaleSelect.options[femaleSelect.selectedIndex];

        if (m.value && f.value) {
            const speciesM = m.getAttribute('data-species');
            const speciesF = f.getAttribute('data-species');
            warning.style.display = (speciesM !== speciesF) ? 'block' : 'none';
        } else {
            warning.style.display = 'none';
        }
    };

    // Pairing Status Check (Concurrent / Polygamy)
    const checkPairingStatus = () => {
        const idM = maleSelect.value;
        const idF = femaleSelect.value;

        pairStatusWarning.style.display = 'none';

        if (!idM && !idF) return;

        // Helper to check if bird is in an active pair
        // Active = Status NOT in ['Separados', 'Finalizada', 'Baja', 'Vendido']? 
        // Based on app logic, 'estado' is 'Juntos' or 'Separados'. 'Puesta', 'Incubación' etc are Clutch statuses.
        // But the Pair status is usually what we check. 
        // Let's assume 'Juntos' means they are together.

        const isBusy = (birdId) => {
            return currentPairs.find(p =>
                (p.id_macho == birdId || p.id_hembra == birdId) &&
                p.estado !== 'Separados' && p.estado !== 'Finalizada' && // Check if pair is closed
                p.id_cruce != editingPairId // Ignore self when editing
            );
        };

        const activeM = idM ? isBusy(idM) : null;
        const activeF = idF ? isBusy(idF) : null;

        if (activeF) {
            pairStatusWarning.className = '';
            pairStatusWarning.style.display = 'block';
            pairStatusWarning.style.background = '#fef2f2';
            pairStatusWarning.style.border = '1px solid #fca5a5';
            pairStatusWarning.style.color = '#991b1b';
            pairStatusWarning.innerHTML = `⛔ <strong>Alerta:</strong> La hembra seleccionada ya tiene una pareja activa (Pareja #${activeF.id_cruce}).`;
        } else if (activeM) {
            pairStatusWarning.className = '';
            pairStatusWarning.style.display = 'block';
            pairStatusWarning.style.background = '#fffbeb';
            pairStatusWarning.style.border = '1px solid #fcd34d';
            pairStatusWarning.style.color = '#92400e';
            pairStatusWarning.innerHTML = `⚠️ <strong>Aviso:</strong> El macho seleccionado ya tiene una pareja activa (Pareja #${activeM.id_cruce}). Se permite poligamia.`;
        }
    };

    maleSelect.addEventListener('change', checkPairingStatus);
    femaleSelect.addEventListener('change', checkPairingStatus);

    maleSelect.addEventListener('change', checkHybrid);
    femaleSelect.addEventListener('change', checkHybrid);

    // ACTIONS
    const openPairModal = (pair = null) => {
        modal.style.display = 'flex';
        form.reset();
        container.querySelector('#pairing-date').value = new Date().toISOString().split('T')[0];

        if (pair) {
            editingPairId = pair.id_cruce;
            container.querySelector('h2').textContent = "Editar Pareja";
            container.querySelector('#btn-save-pair').textContent = "Guardar Cambios";

            // Set values
            maleSelect.value = pair.id_macho;
            femaleSelect.value = pair.id_hembra;
            container.querySelector('#objective').value = pair.variedad_objetivo || '';
            container.querySelector('#location').value = pair.id_ubicacion || ''; // Text input
            container.querySelector('#pairing-date').value = pair.fecha_union || new Date().toISOString().split('T')[0];
        } else {
            editingPairId = null;
            container.querySelector('h2').textContent = "Formar Nueva Pareja";
            container.querySelector('#btn-save-pair').textContent = "Crear Pareja";
        }
    };

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            id_macho: maleSelect.value,
            id_hembra: femaleSelect.value,
            variedad_objetivo: container.querySelector('#objective').value,
            id_ubicacion: container.querySelector('#location').value,
            fecha_union: container.querySelector('#pairing-date').value
        };

        try {
            let res;
            if (editingPairId) {
                // UPDATE
                res = await fetch(`/api/pairs/${editingPairId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            } else {
                // CREATE
                res = await fetch('/api/pairs', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            }

            if (res.ok) {
                modal.style.display = 'none';
                form.reset();
                loadData();
                if (!editingPairId) alert("¡Pareja formada!");
            } else {
                throw new Error('Error saving pair');
            }
        } catch (err) {
            alert("Error: " + err.message);
        }
    });

    container.querySelector('#btn-new-pair').addEventListener('click', () => openPairModal(null));

    container.querySelector('#btn-cancel-pair').addEventListener('click', () => {
        modal.style.display = 'none';
        form.reset();
    });
    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.style.display = 'none';
        // Also check clutch modal
        const modalClutch = container.querySelector('#modal-clutch');
        if (e.target === modalClutch) modalClutch.style.display = 'none';
    });

    loadData();
    return container;
};

