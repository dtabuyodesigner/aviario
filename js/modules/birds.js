import { db } from '../core/db.js';

export const BirdsView = async () => {
    const container = document.createElement('div');
    container.className = 'module-birds';
    container.style.cssText = 'padding: 1.5rem; max-width: 1400px; margin: 0 auto;';

    let allBirds = [];
    let filteredBirds = [];
    let currentFilter = 'all';
    let searchTerm = '';

    async function fetchBirds() {
        try {
            const response = await fetch('/api/birds');
            allBirds = await response.json();
            applyFilters();
        } catch (error) {
            console.error('Error loading birds:', error);
        }
    }

    function applyFilters() {
        filteredBirds = allBirds.filter(bird => {
            let statusMatch = currentFilter === 'all';
            if (currentFilter === 'active') statusMatch = bird.estado === 'Activo';
            if (currentFilter === 'inactive') statusMatch = bird.estado !== 'Activo';
            if (currentFilter === 'disponible') statusMatch = Number(bird.disponible_venta) === 1;
            if (currentFilter === 'reservado') statusMatch = Number(bird.reservado) === 1;

            const searchMatch = !searchTerm ||
                (bird.anilla && bird.anilla.toLowerCase().includes(searchTerm.toLowerCase())) ||
                (bird.especie && bird.especie.toLowerCase().includes(searchTerm.toLowerCase())) ||
                (bird.mutacion_visual && bird.mutacion_visual.toLowerCase().includes(searchTerm.toLowerCase())) ||
                (bird.portador_de && bird.portador_de.toLowerCase().includes(searchTerm.toLowerCase()));

            return statusMatch && searchMatch;
        });
        renderBirdList();
    }

    function renderBirdList() {
        const tbody = container.querySelector('#birds-tbody');
        if (!tbody) return;
        tbody.innerHTML = '';

        if (filteredBirds.length === 0) {
            tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; padding: 2rem; color: var(--text-secondary);">No se encontraron pájaros</td></tr>`;
            return;
        }

        filteredBirds.forEach(bird => {
            const tr = document.createElement('tr');
            tr.style.cssText = 'cursor: pointer; transition: background 0.2s; border-bottom: 1px solid var(--border-color);';
            tr.onmouseenter = () => tr.style.background = '#f9fafb';
            tr.onmouseleave = () => tr.style.background = '';

            tr.innerHTML = `
                <td style="padding: 0.75rem;">
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <div style="width: 40px; height: 40px; border-radius: 50%; overflow: hidden; background: #e5e7eb; flex-shrink: 0;">
                            ${bird.foto_path ? `<img src="/${bird.foto_path}" style="width: 100%; height: 100%; object-fit: cover;">` : '<div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem;">🐦</div>'}
                        </div>
                        <div>
                            <div style="font-weight: 600; color: var(--text-primary);">${bird.anilla || 'Sin anilla'}</div>
                            <div style="font-size: 0.85rem; color: var(--text-secondary);">${bird.fecha_nacimiento || bird.anio_nacimiento || ''}</div>
                        </div>
                    </div>
                </td>
                <td style="padding: 0.75rem;">${bird.especie || '-'}</td>
                <td style="padding: 0.75rem;">
                    <span style="display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 500; 
                                 ${bird.sexo === 'M' ? 'background: #dbeafe; color: #1e40af;' : bird.sexo === 'H' ? 'background: #fce7f3; color: #be185d;' : 'background: #f1f5f9; color: #64748b;'}">
                        ${bird.sexo === 'M' ? '♂ Macho' : bird.sexo === 'H' ? '♀ Hembra' : '? Pendiente'}
                    </span>
                </td>
                <td style="padding: 0.75rem;">
                    <div>${bird.mutacion_visual || 'Ancestral'}</div>
                    ${bird.portador_de ? `<div style="font-size: 0.75rem; color: var(--text-secondary);">/ Port.: ${bird.portador_de}</div>` : ''}
                </td>
                <td style="padding: 0.75rem;">
                    <span style="display: inline-block; padding: 4px 10px; border-radius: 4px; font-size: 0.8rem; font-weight: 500;
                                 ${bird.estado === 'Activo' ? 'background: #d1fae5; color: #065f46;' : bird.estado === 'Vendido' ? 'background: #dbeafe; color: #1e40af;' : bird.estado === 'Cedido' ? 'background: #fef3c7; color: #92400e;' : 'background: #fee2e2; color: #991b1b;'}">
                        ${bird.estado || 'Activo'}
                    </span>
                </td>
                <td style="padding: 0.75rem;">
                    <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                        ${Number(bird.disponible_venta) === 1 ? '<span style="background: #16a34a; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 500;">DISPONIBLE</span>' : ''}
                        ${Number(bird.reservado) === 1 ? '<span style="background: #eab308; color: black; padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 500;">RESERVADO</span>' : ''}
                    </div>
                </td>
                <td style="padding: 0.75rem;">
                    <button class="btn btn-sm btn-edit" data-bird-id="${bird.id_ave}" style="padding: 0.25rem 0.75rem; font-size: 0.875rem;">Ver</button>
                </td>
            `;
            tr.querySelector('.btn-edit').addEventListener('click', () => openBirdModal({ birdId: bird.id_ave, onSave: fetchBirds }));
            tbody.appendChild(tr);
        });
    }

    container.innerHTML = `
        <div style="margin-bottom: 2rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div>
                    <h1 style="font-size: 2rem; color: var(--primary-color); margin: 0 0 0.5rem 0;">Mis Pájaros</h1>
                    <p style="color: var(--text-secondary); margin: 0;">Gestiona tu inventario de aves</p>
                </div>
                <button id="new-bird-btn" class="btn btn-primary" style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 1.2rem;">+</span> Nuevo Pájaro
                </button>
            </div>
            <div style="background: white; padding: 1rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border: 1px solid var(--border-color); margin-bottom: 1rem;">
                <div style="display: flex; gap: 1rem; flex-wrap: wrap; align-items: center;">
                    <div style="flex: 1; min-width: 250px;">
                        <input type="text" id="search-input" placeholder="Buscar por anilla, especie o mutación..." style="width: 100%; padding: 0.5rem 1rem; border: 1px solid var(--border-color); border-radius: var(--radius-md);">
                    </div>
                    <div style="display: flex; gap: 0.5rem;">
                        <button class="filter-btn active" data-filter="all" style="padding: 0.5rem 1rem; border: 1px solid var(--border-color); border-radius: var(--radius-md); cursor: pointer;">Todos</button>
                        <button class="filter-btn" data-filter="active" style="padding: 0.5rem 1rem; border: 1px solid var(--border-color); border-radius: var(--radius-md); cursor: pointer;">Activos</button>
                        <button class="filter-btn" data-filter="inactive" style="padding: 0.5rem 1rem; border: 1px solid var(--border-color); border-radius: var(--radius-md); cursor: pointer;">Histórico</button>
                        <button class="filter-btn" data-filter="disponible" style="padding: 0.5rem 1rem; border: 1px solid var(--border-color); border-radius: var(--radius-md); cursor: pointer;">Disponibles</button>
                        <button class="filter-btn" data-filter="reservado" style="padding: 0.5rem 1rem; border: 1px solid var(--border-color); border-radius: var(--radius-md); cursor: pointer;">Reservados</button>
                    </div>
                </div>
            </div>
            <div style="background: white; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border: 1px solid var(--border-color); overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse;">
                    <thead style="background: #f9fafb; border-bottom: 2px solid var(--border-color);">
                        <tr>
                            <th style="padding: 0.75rem; text-align: left;">Pájaro</th>
                            <th style="padding: 0.75rem; text-align: left;">Especie</th>
                            <th style="padding: 0.75rem; text-align: left;">Sexo</th>
                            <th style="padding: 0.75rem; text-align: left;">Mutación</th>
                            <th style="padding: 0.75rem; text-align: left;">Estado</th>
                            <th style="padding: 0.75rem; text-align: left;">Disponibilidad</th>
                            <th style="padding: 0.75rem; text-align: left;">Acciones</th>
                        </tr>
                    </thead>
                    <tbody id="birds-tbody"></tbody>
                </table>
            </div>
        </div>
    `;

    container.querySelector('#search-input').addEventListener('input', (e) => {
        searchTerm = e.target.value;
        applyFilters();
    });

    container.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            currentFilter = btn.dataset.filter;
            container.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            applyFilters();
        });
    });

    container.querySelector('#new-bird-btn').addEventListener('click', () => openBirdModal({ onSave: fetchBirds }));

    await fetchBirds();
    return container;
};

export async function openBirdModal({ birdId = null, initialData = {}, onSave = null } = {}) {
    let bird = {};
    if (birdId) {
        const res = await fetch('/api/birds');
        const all = await res.json();
        bird = all.find(b => b.id_ave == birdId || b.uuid == birdId) || {};
    } else {
        bird = initialData;
    }

    const resSpec = await fetch('/api/species');
    const loadedSpecies = await resSpec.json();
    const resAll = await fetch('/api/birds');
    const allBirds = await resAll.json();

    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 2000; padding: 1rem;';

    const content = document.createElement('div');
    content.style.cssText = 'background: white; border-radius: var(--radius-lg); max-width: 900px; width: 100%; max-height: 90vh; overflow-y: auto; box-shadow: var(--shadow-xl);';

    let selectedVisual = bird.mutacion_visual ? bird.mutacion_visual.split(',').map(s => s.trim()).filter(s => s) : [];
    let selectedCarrier = bird.portador_de ? bird.portador_de.split(',').map(s => s.trim()).filter(s => s) : [];

    content.innerHTML = `
        <div style="position: sticky; top: 0; background: white; border-bottom: 1px solid var(--border-color); padding: 1.5rem; z-index: 10; display: flex; justify-content: space-between; align-items: center;">
            <h2 style="margin: 0;">${birdId ? 'Editar Pájaro' : 'Registrar Pájaro'}</h2>
            <button id="close-modal" style="background:none; border:none; font-size:1.5rem; cursor:pointer;">&times;</button>
        </div>
        <form id="bird-form" style="padding: 1.5rem;">
            <input type="hidden" name="id_ave" value="${bird.id_ave || ''}">
            <fieldset style="border: 1px solid var(--border-color); padding: 1rem; border-radius: var(--radius-md); margin-bottom: 1.5rem;">
                <legend style="font-weight: 600; padding: 0 0.5rem;">Información Básica</legend>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                    <div>
                        <label>Anilla *</label>
                        <input type="text" name="anilla" value="${bird.anilla || ''}" required style="width:100%; padding:0.5rem; border:1px solid var(--border-color); border-radius:var(--radius-md);">
                    </div>
                    <div>
                        <label>Fecha de Nacimiento</label>
                        <input type="date" name="fecha_nacimiento" value="${bird.fecha_nacimiento || ''}" style="width:100%; padding:0.5rem; border:1px solid var(--border-color); border-radius:var(--radius-md);">
                    </div>
                    <div>
                        <label>Sexo</label>
                        <select name="sexo" style="width:100%; padding:0.5rem; border:1px solid var(--border-color); border-radius:var(--radius-md);">
                            <option value="?" ${bird.sexo === '?' ? 'selected' : ''}>Pendiente</option>
                            <option value="M" ${bird.sexo === 'M' ? 'selected' : ''}>Macho</option>
                            <option value="H" ${bird.sexo === 'H' ? 'selected' : ''}>Hembra</option>
                        </select>
                    </div>
                </div>
            </fieldset>

            <fieldset style="border: 1px solid var(--border-color); padding: 1rem; border-radius: var(--radius-md); margin-bottom: 1.5rem;">
                <legend style="font-weight: 600; padding: 0 0.5rem;">Genética y Especie</legend>
                <div style="display: grid; gap: 1rem;">
                    <div style="grid-column: span 2;">
                        <label>Especie *</label>
                        <select name="id_especie" id="species-select" required style="width:100%; padding:0.5rem; border:1px solid var(--border-color); border-radius:var(--radius-md);">
                            <option value="">Seleccionar...</option>
                            ${loadedSpecies.map(s => `<option value="${s.id_especie}" ${bird.id_especie === s.id_especie ? 'selected' : ''}>${s.nombre_comun}</option>`).join('')}
                        </select>
                    </div>
                    <div id="mutations-section">
                        <label>Mutación Visual</label>
                        <div id="visual-tags" style="display:flex; flex-wrap:wrap; gap:0.5rem; margin-bottom:0.5rem;"></div>
                        <select id="visual-select" style="width:100%; padding:0.5rem; border:1px solid var(--border-color); border-radius:var(--radius-md);">
                            <option value="">Añadir mutación...</option>
                        </select>
                        <input type="hidden" name="mutacion_visual" id="hidden-visual" value="${bird.mutacion_visual || ''}">
                        
                        <label style="display:block; margin-top:1rem;">Portador de</label>
                        <div id="carrier-tags" style="display:flex; flex-wrap:wrap; gap:0.5rem; margin-bottom:0.5rem;"></div>
                        <select id="carrier-select" style="width:100%; padding:0.5rem; border:1px solid var(--border-color); border-radius:var(--radius-md);">
                            <option value="">Añadir mutación...</option>
                        </select>
                        <input type="hidden" name="portador_de" id="hidden-carrier" value="${bird.portador_de || ''}">
                    </div>
                </div>
            </fieldset>

            <fieldset style="border: 1px solid var(--border-color); padding: 1rem; border-radius: var(--radius-md); margin-bottom: 1.5rem;">
                <legend style="font-weight: 600; padding: 0 0.5rem;">Estado y Disponibilidad</legend>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                    <div>
                        <label>Estado</label>
                        <select name="estado" style="width:100%; padding:0.5rem; border:1px solid var(--border-color); border-radius:var(--radius-md);">
                            <option value="Activo" ${bird.estado === 'Activo' ? 'selected' : ''}>Activo</option>
                            <option value="Cedido" ${bird.estado === 'Cedido' ? 'selected' : ''}>Cedido</option>
                            <option value="Vendido" ${bird.estado === 'Vendido' ? 'selected' : ''}>Vendido</option>
                            <option value="Baja" ${bird.estado === 'Baja' ? 'selected' : ''}>Baja</option>
                        </select>
                    </div>
                    <div>
                        <label style="display: flex; gap: 0.5rem; align-items: center; cursor: pointer;">
                            <input type="checkbox" name="disponible_venta" ${Number(bird.disponible_venta) === 1 ? 'checked' : ''}> Disponible para Cesión
                        </label>
                    </div>
                    <div>
                        <label style="display: flex; gap: 0.5rem; align-items: center; cursor: pointer;">
                            <input type="checkbox" name="reservado" ${Number(bird.reservado) === 1 ? 'checked' : ''}> Reservado
                        </label>
                    </div>
                </div>
            </fieldset>

            <fieldset style="border: 1px solid var(--border-color); padding: 1rem; border-radius: var(--radius-md); margin-bottom: 1.5rem;">
                <legend style="font-weight: 600; padding: 0 0.5rem;">Genealogía</legend>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                    <div>
                        <label>Padre (Macho)</label>
                        <select name="padre_uuid" id="parent-male" style="width:100%; padding:0.5rem; border:1px solid var(--border-color); border-radius:var(--radius-md);">
                            <option value="">Desconocido</option>
                        </select>
                    </div>
                    <div>
                        <label>Madre (Hembra)</label>
                        <select name="parent-female" id="parent-female" style="width:100%; padding:0.5rem; border:1px solid var(--border-color); border-radius:var(--radius-md);">
                            <option value="">Desconocido</option>
                        </select>
                    </div>
                </div>
            </fieldset>
            <div style="display: flex; justify-content: space-between; gap: 1rem;">
                <div>
                   ${bird.uuid ? `<button type="button" id="btn-cert" class="btn" style="background: #0ea5e9; color: white;">📄 Certificado (PDF)</button>` : ''}
                </div>
                <div style="display: flex; gap: 1rem;">
                    <button type="button" id="cancel-modal" class="btn">Cancelar</button>
                    <button type="submit" class="btn btn-primary">Guardar</button>
                </div>
            </div>
        </form>
    `;

    modal.appendChild(content);
    document.body.appendChild(modal);

    const form = content.querySelector('#bird-form');
    const speciesSelect = form.querySelector('#species-select');
    const visualSelect = form.querySelector('#visual-select');
    const carrierSelect = form.querySelector('#carrier-select');
    const maleSelect = form.querySelector('#parent-male');
    const femaleSelect = form.querySelector('#parent-female');

    const renderTags = (containerId, list, hiddenId, type) => {
        const container = form.querySelector(containerId);
        container.innerHTML = '';
        list.forEach(item => {
            const tag = document.createElement('span');
            tag.style.cssText = `background:#e0f2fe; color:#0369a1; padding:0.25rem 0.5rem; border-radius:4px; font-size:0.85rem; display:flex; align-items:center; gap:0.25rem;`;
            tag.innerHTML = `${item} <span style="cursor:pointer; font-weight:bold;">&times;</span>`;
            tag.querySelector('span').onclick = () => {
                const idx = list.indexOf(item);
                if (idx > -1) list.splice(idx, 1);
                renderTags(containerId, list, hiddenId, type);
            };
            container.appendChild(tag);
        });
        form.querySelector(hiddenId).value = list.join(', ');
    };

    // Helper to group and sort mutations
    const groupAndSortMutations = (mutations) => {
        // Preferred Order
        const order = [
            "Serie base",
            "Base",
            "Factor Oscuro",
            "Ligadas al sexo", "Ligadas al Sexo",
            "Diluciones",
            "Alas y Patrones", "Patrones",
            "Factores Faciales",
            "Avanzadas",
            "Mutaciones raras o avanzadas",
            "Mutaciones raras"
        ];

        // Grouping
        const groups = {};
        mutations.forEach(m => {
            const group = m.subgrupo || 'Otros';
            if (!groups[group]) groups[group] = [];
            groups[group].push(m);
        });

        // Sorting keys
        const sortedKeys = Object.keys(groups).sort((a, b) => {
            const idxA = order.indexOf(a);
            const idxB = order.indexOf(b);

            // Handle "Otros" to be last
            if (a === 'Otros') return 1;
            if (b === 'Otros') return -1;

            if (idxA !== -1 && idxB !== -1) return idxA - idxB;
            if (idxA !== -1) return -1;
            if (idxB !== -1) return 1;
            return a.localeCompare(b);
        });

        // Generate HTML
        let html = '';
        sortedKeys.forEach(key => {
            if (key === 'Otros' && sortedKeys.length === 1) {
                // If only 'Otros' exists (e.g. Canaries), don't show optgroup label
                html += groups[key].map(m => `<option value="${m.nombre}">${m.nombre}</option>`).join('');
            } else if (key === 'Otros') {
                html += `<optgroup label="Otros">`;
                html += groups[key].map(m => `<option value="${m.nombre}">${m.nombre}</option>`).join('');
                html += `</optgroup>`;
            } else {
                html += `<optgroup label="${key}">`;
                html += groups[key].map(m => `<option value="${m.nombre}">${m.nombre}</option>`).join('');
                html += `</optgroup>`;
            }
        });

        return html;
    };

    const loadMutations = async () => {
        const id = speciesSelect.value;
        const sp = loadedSpecies.find(s => s.id_especie == id);

        // Clear previous dynamic fields
        const varietyContainer = form.querySelector('#variety-section');
        if (varietyContainer) varietyContainer.remove();

        visualSelect.innerHTML = '<option value="">Añadir mutación...</option>';
        carrierSelect.innerHTML = '<option value="">Añadir mutación...</option>';

        if (!sp) return;

        // 1. Check for Varieties (Sub-types like Canary Color, Posture, Song)
        let varieties = await db.getVarieties(sp.uuid || sp.id_especie); // Fallback to id if uuid missing in object

        if (varieties && varieties.length > 0) {
            // Create Variety Selector
            let varDiv = document.createElement('div');
            varDiv.id = 'variety-section';
            varDiv.style.marginBottom = '1rem';
            varDiv.innerHTML = `
                <label>Tipo / Variedad</label>
                <select id="variety-select" name="variety_uuid" style="width:100%; padding:0.5rem; border:1px solid var(--border-color); border-radius:var(--radius-md);">
                    <option value="">Seleccionar Tipo...</option>
                    ${varieties.map(v => `<option value="${v.uuid}" ${bird.variety_uuid == v.uuid ? 'selected' : ''}>${v.nombre}</option>`).join('')}
                </select>
            `;

            // Insert after species select
            speciesSelect.parentNode.parentNode.insertBefore(varDiv, speciesSelect.parentNode.nextSibling);

            const varSelect = varDiv.querySelector('#variety-select');

            // Logic when Variety is selected
            const onVarietyChange = async () => {
                const varId = varSelect.value;
                if (!varId) return;

                const selectedVar = varieties.find(v => v.uuid == varId);

                // Clear again to avoid duplicates
                visualSelect.innerHTML = '<option value="">Añadir mutación...</option>';

                // 2. Load Mutations (mostly for Color)
                const muts = await db.getMutations(null, varId);
                if (muts && muts.length > 0) {
                    visualSelect.innerHTML += groupAndSortMutations(muts);
                } else if (sp.nombre_comun.toLowerCase() === 'canario' && !selectedVar.nombre.toLowerCase().includes('color')) {
                    // 3. If no mutations and it's Posture/Song, check Breeds
                    const breeds = await db.getBreeds(varId);
                    if (breeds && breeds.length > 0) {
                        // We might need a separate Breed selector or reuse visualSelect if simplified
                        // User asked for "Types -> Mutations", but Posture has Breeds.
                        // Let's populate the 'mutacion_visual' field with Breeds for display consistency or add a Breed field?
                        // Current schema puts breeds in 'mutacion_visual' text often, strictly speaking it's a phenotype.
                        // Let's reuse visual select but label it appropriately if we could, 
                        // but simpler to just load them into the select.
                        visualSelect.innerHTML += breeds.map(b => `<option value="${b.nombre}">${b.nombre}</option>`).join('');
                        // Disable carriers for breeds
                        carrierSelect.disabled = true;
                    }
                }
                carrierSelect.innerHTML = visualSelect.innerHTML;
                if (!carrierSelect.disabled) carrierSelect.disabled = false;
            };

            varSelect.addEventListener('change', onVarietyChange);

            // Trigger if existing bird has variety
            if (bird.variety_uuid) await onVarietyChange();

        } else {
            // No varieties, standard mutation load
            console.log('Fetching standard mutations for:', sp.nombre_comun);
            try {
                const muts = await db.getMutations(sp.nombre_comun);
                visualSelect.innerHTML += groupAndSortMutations(muts);
                carrierSelect.innerHTML = visualSelect.innerHTML;
            } catch (err) {
                console.error(err);
            }
        }
    };

    const populateParents = () => {
        const id = parseInt(speciesSelect.value);
        if (!id) return;
        console.log('Populating parents for Species ID:', id);

        // Debug filtering
        const potentialFemales = allBirds.filter(b => b.id_especie == id && b.sexo == 'H');
        console.log('Potential Mothers found:', potentialFemales.length, potentialFemales);

        const males = allBirds.filter(b => b.id_especie == id && b.sexo == 'M' && (bird.id_ave ? b.id_ave != bird.id_ave : true));
        const females = allBirds.filter(b => b.id_especie == id && b.sexo == 'H' && (bird.id_ave ? b.id_ave != bird.id_ave : true));

        maleSelect.innerHTML = '<option value="">Desconocido</option>' + males.map(m => `<option value="${m.uuid}" ${bird.padre_uuid == m.uuid ? 'selected' : ''}>${m.anilla} (${m.estado})</option>`).join('');
        femaleSelect.innerHTML = '<option value="">Desconocido</option>' + females.map(f => `<option value="${f.uuid}" ${bird.madre_uuid == f.uuid ? 'selected' : ''}>${f.anilla} (${f.estado})</option>`).join('');
    };

    speciesSelect.onchange = () => { loadMutations(); populateParents(); };
    visualSelect.onchange = (e) => { if (e.target.value && !selectedVisual.includes(e.target.value)) { selectedVisual.push(e.target.value); renderTags('#visual-tags', selectedVisual, '#hidden-visual', 'visual'); } e.target.value = ''; };
    carrierSelect.onchange = (e) => { if (e.target.value && !selectedCarrier.includes(e.target.value)) { selectedCarrier.push(e.target.value); renderTags('#carrier-tags', selectedCarrier, '#hidden-carrier', 'carrier'); } e.target.value = ''; };

    // Initial Load
    if (bird.id_especie) {
        loadMutations();
        populateParents();
    }

    renderTags('#visual-tags', selectedVisual, '#hidden-visual', 'visual');
    renderTags('#carrier-tags', selectedCarrier, '#hidden-carrier', 'carrier');

    form.onsubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const url = bird.id_ave ? `/api/birds/${bird.id_ave}` : '/api/birds';
        const method = bird.id_ave ? 'PUT' : 'POST';
        const res = await fetch(url, { method, body: formData });
        if (res.ok) { modal.remove(); if (onSave) onSave(); }
        else { const err = await res.json(); alert(err.error || 'Error'); }
    };

    const btnCert = content.querySelector('#btn-cert');
    if (btnCert) {
        btnCert.onclick = () => {
            window.open(`/api/birds/${bird.uuid}/certificate`, '_blank');
        };
    }

    content.querySelector('#close-modal').onclick = () => modal.remove();
    content.querySelector('#cancel-modal').onclick = () => modal.remove();
    modal.onclick = (e) => { if (e.target == modal) modal.remove(); };
}
