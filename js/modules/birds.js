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
            const response = await fetch('/api/v2/birds/');
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
                (bird.variedad && bird.variedad.toLowerCase().includes(searchTerm.toLowerCase()));

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
                            <div style="font-size: 0.85rem; color: var(--text-secondary);">${bird.fecha_nacimiento || ''}</div>
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
                    <div>${bird.variedad || 'Ancestral'}</div>
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
                    <button class="btn btn-sm btn-edit" data-bird-id="${bird.uuid}" style="padding: 0.25rem 0.75rem; font-size: 0.875rem;">Ver</button>
                    <button class="btn btn-sm btn-delete" data-bird-id="${bird.uuid}" style="padding: 0.25rem 0.75rem; font-size: 0.875rem; background: #fee2e2; color: #991b1b; border: none; margin-left: 0.5rem;">Borrar</button>
                </td>
            `;
            tr.querySelector('.btn-edit').addEventListener('click', (e) => {
                e.stopPropagation();
                openBirdModal({ birdId: bird.uuid, onSave: fetchBirds });
            });
            tr.querySelector('.btn-delete').addEventListener('click', async (e) => {
                e.stopPropagation();
                if (confirm('¿Estás seguro de que deseas borrar este pájaro?')) {
                    try {
                        const res = await fetch(`/api/v2/birds/${bird.uuid}`, { method: 'DELETE' });
                        if (res.ok) fetchBirds();
                        else alert('Error al borrar');
                    } catch (err) {
                        console.error(err);
                    }
                }
            });
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
                        <input type="text" id="search-input" placeholder="Buscar por anilla, especie o variedad..." style="width: 100%; padding: 0.5rem 1rem; border: 1px solid var(--border-color); border-radius: var(--radius-md);">
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
                            <th style="padding: 0.75rem; text-align: left;">Variedad</th>
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
        try {
            const res = await fetch(`/api/v2/birds/${birdId}`);
            if (res.ok) {
                bird = await res.json();
            } else {
                console.error('Error loading bird:', await res.text());
                bird = {};
            }
        } catch (error) {
            console.error('Error fetching bird:', error);
            bird = {};
        }
    } else {
        bird = initialData;
    }

    // Load species list
    let loadedSpecies = [];
    try {
        const resSpec = await fetch('/api/v2/genetics/species');
        if (resSpec.ok) {
            loadedSpecies = await resSpec.json();
        }
    } catch (error) {
        console.error('Error fetching species:', error);
    }

    // Load all birds (for parent selectors)
    let allBirds = [];
    try {
        const resAll = await fetch('/api/v2/birds/');
        if (resAll.ok) {
            allBirds = await resAll.json();
        }
    } catch (error) {
        console.error('Error fetching birds:', error);
    }

    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 2000; padding: 1rem;';

    const content = document.createElement('div');
    content.style.cssText = 'background: white; border-radius: var(--radius-lg); max-width: 900px; width: 100%; max-height: 90vh; overflow-y: auto; box-shadow: var(--shadow-xl);';

    let selectedGenetica = bird.genetica || [];

    content.innerHTML = `
        <div style="position: sticky; top: 0; background: white; border-bottom: 1px solid var(--border-color); padding: 1.5rem; z-index: 10; display: flex; justify-content: space-between; align-items: center;">
            <h2 style="margin: 0;">${birdId ? 'Detalle Pájaro' : 'Registrar Pájaro'}</h2>
            <button id="close-modal" style="background:none; border:none; font-size:1.5rem; cursor:pointer;">&times;</button>
        </div>
        <form id="bird-form" style="padding: 1.5rem;">
            <input type="hidden" name="uuid" value="${bird.uuid || ''}">
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
                <!-- Column 1: Info Básica -->
                <div>
                    <fieldset style="border: 1px solid var(--border-color); padding: 1rem; border-radius: var(--radius-md); margin-bottom: 1.5rem;">
                        <legend style="font-weight: 600; padding: 0 0.5rem;">Información Básica</legend>
                        <div style="display: grid; gap: 1rem;">
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
                            <div>
                                <label>Estado</label>
                                <select name="estado" style="width:100%; padding:0.5rem; border:1px solid var(--border-color); border-radius:var(--radius-md);">
                                    <option value="Activo" ${bird.estado === 'Activo' ? 'selected' : ''}>Activo</option>
                                    <option value="Cedido" ${bird.estado === 'Cedido' ? 'selected' : ''}>Cedido</option>
                                    <option value="Vendido" ${bird.estado === 'Vendido' ? 'selected' : ''}>Vendido</option>
                                    <option value="Baja" ${bird.estado === 'Baja' ? 'selected' : ''}>Baja</option>
                                </select>
                            </div>
                        </div>
                    </fieldset>

                    <fieldset style="border: 1px solid var(--border-color); padding: 1rem; border-radius: var(--radius-md); margin-bottom: 1.5rem;">
                        <legend style="font-weight: 600; padding: 0 0.5rem;">Genealogía</legend>
                        <div style="display: grid; gap: 1rem;">
                            <div>
                                <label>Padre (UUID)</label>
                                <select name="padre_uuid" id="parent-male" style="width:100%; padding:0.5rem; border:1px solid var(--border-color); border-radius:var(--radius-md);">
                                    <option value="">Desconocido</option>
                                </select>
                            </div>
                            <div>
                                <label>Madre (UUID)</label>
                                <select name="madre_uuid" id="parent-female" style="width:100%; padding:0.5rem; border:1px solid var(--border-color); border-radius:var(--radius-md);">
                                    <option value="">Desconocido</option>
                                </select>
                            </div>
                        </div>
                    </fieldset>
                </div>

                <!-- Column 2: Especie y Genética -->
                <div>
                    <fieldset style="border: 1px solid var(--border-color); padding: 1rem; border-radius: var(--radius-md); margin-bottom: 1.5rem;">
                        <legend style="font-weight: 600; padding: 0 0.5rem;">Clasificación y Genética</legend>
                        <div style="display: grid; gap: 1rem;">
                            <div>
                                <label>Especie *</label>
                                <select id="species-select" required style="width:100%; padding:0.5rem; border:1px solid var(--border-color); border-radius:var(--radius-md);">
                                    <option value="">Seleccionar Especie...</option>
                                    ${loadedSpecies.map(s => `<option value="${s.uuid}" ${bird.especie === s.nombre_comun ? 'selected' : ''}>${s.nombre_comun}</option>`).join('')}
                                </select>
                            </div>
                            <div id="variety-container">
                                <label>Variedad *</label>
                                <select name="variety_uuid" id="variety-select" required style="width:100%; padding:0.5rem; border:1px solid var(--border-color); border-radius:var(--radius-md);">
                                    <option value="">Seleccionar Variedad...</option>
                                </select>
                            </div>
                            <div id="mutations-container" style="margin-top: 1rem;">
                                <label>Mutaciones (Genética)</label>
                                <div id="genetica-tags" style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.5rem;"></div>
                                <select id="mutation-select" style="width:100%; padding:0.5rem; border:1px solid var(--border-color); border-radius:var(--radius-md);">
                                    <option value="">Añadir Mutación...</option>
                                </select>
                            </div>
                        </div>
                    </fieldset>

                    <fieldset style="border: 1px solid var(--border-color); padding: 1rem; border-radius: var(--radius-md);">
                        <legend style="font-weight: 600; padding: 0 0.5rem;">Otras Opciones</legend>
                        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                            <label style="display: flex; gap: 0.5rem; align-items: center; cursor: pointer;">
                                <input type="checkbox" name="disponible_venta" ${Number(bird.disponible_venta) === 1 ? 'checked' : ''}> Disponible para Cesión
                            </label>
                            <label style="display: flex; gap: 0.5rem; align-items: center; cursor: pointer;">
                                <input type="checkbox" name="reservado" ${Number(bird.reservado) === 1 ? 'checked' : ''}> Reservado
                            </label>
                        </div>
                    </fieldset>
                </div>
            </div>

            <div style="margin-top: 1.5rem; display: flex; justify-content: flex-end; gap: 1rem; position: sticky; bottom: 0; background: white; padding-top: 1rem; border-top: 1px solid var(--border-color);">
                <button type="button" id="cancel-modal" class="btn">Cancelar</button>
                <button type="submit" class="btn btn-primary">Guardar</button>
            </div>
        </form>
    `;

    modal.appendChild(content);
    document.body.appendChild(modal);

    const form = content.querySelector('#bird-form');
    const speciesSelect = form.querySelector('#species-select');
    const varietySelect = form.querySelector('#variety-select');
    const mutationSelect = form.querySelector('#mutation-select');
    const geneticaTags = form.querySelector('#genetica-tags');

    const renderGeneticaTags = () => {
        geneticaTags.innerHTML = '';
        selectedGenetica.forEach((g, index) => {
            const tag = document.createElement('span');
            tag.style.cssText = 'background: #e0f2fe; color: #0369a1; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.85rem; display: flex; align-items: center; gap: 0.5rem;';
            tag.innerHTML = `${g.mutacion || g.mutacion_uuid} <span style="cursor: pointer; font-weight: bold; font-size: 1.1rem;">&times;</span>`;
            tag.querySelector('span').onclick = () => {
                selectedGenetica.splice(index, 1);
                renderGeneticaTags();
            };
            geneticaTags.appendChild(tag);
        });
    };

    const loadVarieties = async (speciesUuid) => {
        if (!speciesUuid) {
            varietySelect.innerHTML = '<option value="">Seleccionar Variedad...</option>';
            return;
        }
        const res = await fetch(`/api/v2/genetics/species/${speciesUuid}/varieties`);
        const varieties = await res.json();
        varietySelect.innerHTML = '<option value="">Seleccionar Variedad...</option>' +
            varieties.map(v => `<option value="${v.uuid}" ${bird.variety_uuid === v.uuid ? 'selected' : ''}>${v.nombre}</option>`).join('');

        if (bird.variety_uuid) {
            loadMutations(bird.variety_uuid);
        }
    };

    const loadMutations = async (varietyUuid) => {
        if (!varietyUuid) {
            mutationSelect.innerHTML = '<option value="">Añadir Mutación...</option>';
            return;
        }
        const res = await fetch(`/api/v2/genetics/varieties/${varietyUuid}/mutations`);
        const mutations = await res.json();
        mutationSelect.innerHTML = '<option value="">Añadir Mutación...</option>' +
            mutations.map(m => `<option value="${m.uuid}" data-name="${m.nombre}">${m.nombre}</option>`).join('');
    };

    const populateParents = () => {
        const maleBirds = allBirds.filter(b => b.sexo === 'M' && b.uuid !== bird.uuid);
        const femaleBirds = allBirds.filter(b => b.sexo === 'H' && b.uuid !== bird.uuid);

        const maleSelect = form.querySelector('#parent-male');
        const femaleSelect = form.querySelector('#parent-female');

        maleSelect.innerHTML = '<option value="">Desconocido</option>' +
            maleBirds.map(b => `<option value="${b.uuid}" ${bird.padre_uuid === b.uuid ? 'selected' : ''}>${b.anilla} (${b.especie || ''})</option>`).join('');
        femaleSelect.innerHTML = '<option value="">Desconocido</option>' +
            femaleBirds.map(b => `<option value="${b.uuid}" ${bird.madre_uuid === b.uuid ? 'selected' : ''}>${b.anilla} (${b.especie || ''})</option>`).join('');
    };

    speciesSelect.onchange = () => loadVarieties(speciesSelect.value);
    varietySelect.onchange = () => loadMutations(varietySelect.value);
    mutationSelect.onchange = (e) => {
        if (e.target.value) {
            const uuid = e.target.value;
            const name = e.target.selectedOptions[0].dataset.name;
            if (!selectedGenetica.find(g => g.mutacion_uuid === uuid)) {
                selectedGenetica.push({ mutacion_uuid: uuid, mutacion: name, expresion: 'Visual' });
                renderGeneticaTags();
            }
            mutationSelect.value = '';
        }
    };

    // Initialize
    if (speciesSelect.value) loadVarieties(speciesSelect.value);
    populateParents();
    renderGeneticaTags();

    form.onsubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Handle checkboxes
        data.disponible_venta = form.querySelector('[name="disponible_venta"]').checked ? 1 : 0;
        data.reservado = form.querySelector('[name="reservado"]').checked ? 1 : 0;

        // Add genetics
        data.genetica = selectedGenetica.map(g => ({
            mutacion_uuid: g.mutacion_uuid,
            expresion: g.expresion || 'Visual'
        }));

        const url = bird.uuid ? `/api/v2/birds/${bird.uuid}` : '/api/v2/birds/';
        const method = bird.uuid ? 'PUT' : 'POST';

        try {
            const res = await fetch(url, {
                method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (res.ok) {
                modal.remove();
                if (onSave) onSave();
            } else {
                const err = await res.json();
                alert('Error al guardar: ' + (err.error || 'Intente de nuevo'));
            }
        } catch (err) {
            console.error(err);
            alert('Error de conexión');
        }
    };

    content.querySelector('#close-modal').onclick = () => modal.remove();
    content.querySelector('#cancel-modal').onclick = () => modal.remove();
    modal.onclick = (e) => { if (e.target == modal) modal.remove(); };
}
