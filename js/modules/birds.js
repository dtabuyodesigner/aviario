export const BirdsView = async () => {
    const container = document.createElement('div');
    container.className = 'module-birds';
    container.style.cssText = 'padding: 1.5rem; max-width: 1400px; margin: 0 auto;';

    // State
    let allBirds = [];
    let filteredBirds = [];
    let currentFilter = 'all';
    let searchTerm = '';
    let loadedContacts = [];

    // Fetch initial data
    async function fetchBirds() {
        try {
            const response = await fetch('/api/birds');
            allBirds = await response.json();
            applyFilters();
        } catch (error) {
            console.error('Error loading birds:', error);
        }
    }

    async function fetchContacts() {
        try {
            const response = await fetch('/api/contacts');
            loadedContacts = await response.json();
        } catch (error) {
            console.error('Error loading contacts:', error);
        }
    }

    function applyFilters() {
        filteredBirds = allBirds.filter(bird => {
            // Filter by status
            const statusMatch = currentFilter === 'all' ||
                (currentFilter === 'active' && bird.estado === 'Activo') ||
                (currentFilter === 'inactive' && bird.estado !== 'Activo');

            // Filter by search term
            const searchMatch = !searchTerm ||
                (bird.anilla && bird.anilla.toLowerCase().includes(searchTerm.toLowerCase())) ||
                (bird.especie && bird.especie.toLowerCase().includes(searchTerm.toLowerCase())) ||
                (bird.mutacion_visual && bird.mutacion_visual.toLowerCase().includes(searchTerm.toLowerCase()));

            return statusMatch && searchMatch;
        });

        renderBirdList();
    }

    function renderBirdList() {
        const tbody = container.querySelector('#birds-tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        if (filteredBirds.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" style="text-align: center; padding: 2rem; color: var(--text-secondary);">
                        No se encontraron pájaros
                    </td>
                </tr>
            `;
            return;
        }

        filteredBirds.forEach(bird => {
            const disponible = Number(bird.disponible_venta) === 1;
            const reservado = Number(bird.reservado) === 1;

            const tr = document.createElement('tr');
            tr.style.cssText = 'cursor: pointer; transition: background 0.2s;';
            tr.onmouseenter = () => tr.style.background = '#f9fafb';
            tr.onmouseleave = () => tr.style.background = '';

            tr.innerHTML = `
                <td style="padding: 0.75rem;">
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <div style="width: 40px; height: 40px; border-radius: 50%; overflow: hidden; background: #e5e7eb; flex-shrink: 0;">
                            ${bird.foto_path ?
                    `<img src="/${bird.foto_path}" style="width: 100%; height: 100%; object-fit: cover;">` :
                    '<div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem;">🐦</div>'}
                        </div>
                        <div>
                            <div style="font-weight: 600; color: var(--text-primary);">${bird.anilla || 'Sin anilla'}</div>
                            <div style="font-size: 0.85rem; color: var(--text-secondary);">${bird.anio_nacimiento || ''}</div>
                        </div>
                    </div>
                </td>
                <td style="padding: 0.75rem;">${bird.especie || '-'}</td>
                <td style="padding: 0.75rem;">
                    <span style="display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 500; 
                                 ${bird.sexo === 'M' ? 'background: #dbeafe; color: #1e40af;' :
                    bird.sexo === 'H' ? 'background: #fce7f3; color: #be185d;' :
                        'background: #f1f5f9; color: #64748b;'}">
                        ${bird.sexo === 'M' ? '♂ Macho' : bird.sexo === 'H' ? '♀ Hembra' : '? Pendiente'}
                    </span>
                </td>
                <td style="padding: 0.75rem;">${bird.mutacion_visual || '-'}</td>
                <td style="padding: 0.75rem;">
                    <span style="display: inline-block; padding: 4px 10px; border-radius: 4px; font-size: 0.8rem; font-weight: 500;
                                 ${bird.estado === 'Activo' ? 'background: #d1fae5; color: #065f46;' :
                    bird.estado === 'Vendido' ? 'background: #dbeafe; color: #1e40af;' :
                        bird.estado === 'Cedido' ? 'background: #fef3c7; color: #92400e;' :
                            'background: #fee2e2; color: #991b1b;'}">
                        ${bird.estado || 'Activo'}
                    </span>
                </td>
                <td style="padding: 0.75rem;">
                    <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                        ${disponible ? '<span style="background: #16a34a; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 500;">DISPONIBLE</span>' : ''}
                        ${reservado ? '<span style="background: #eab308; color: black; padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 500;">RESERVADO</span>' : ''}
                    </div>
                </td>
                <td style="padding: 0.75rem;">
                    <button class="btn btn-sm" onclick="event.stopPropagation();" data-bird-id="${bird.id_ave}" style="padding: 0.25rem 0.75rem; font-size: 0.875rem;">
                        Ver
                    </button>
                </td>
            `;

            tr.querySelector('button').addEventListener('click', () => openBirdModal(bird.id_ave));
            tbody.appendChild(tr);
        });
    }

    async function openBirdModal(birdId) {
        const bird = birdId ? allBirds.find(b => b.id_ave === birdId) : {};
        // if (!bird && birdId) return; // Only return if ID provided but not found

        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            padding: 1rem;
        `;

        const modalContent = document.createElement('div');
        modalContent.style.cssText = `
            background: white;
            border-radius: var(--radius-lg);
            max-width: 900px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        `;

        modalContent.innerHTML = `
            <div style="position: sticky; top: 0; background: white; border-bottom: 1px solid var(--border-color); padding: 1.5rem; z-index: 10;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h2 style="margin: 0; font-size: 1.5rem; color: var(--text-primary);">Detalles del Pájaro</h2>
                    <button id="close-modal-btn" class="btn" style="background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--text-secondary);">×</button>
                </div>
            </div>
            
            <form id="bird-form" style="padding: 1.5rem;">
                <input type="hidden" name="id_ave" value="${bird.id_ave || ''}">
                
                <!-- Información Básica -->
                <fieldset style="border: 1px solid var(--border-color); padding: 1rem; border-radius: var(--radius-md); margin-bottom: 1.5rem;">
                    <legend style="font-weight: 600; padding: 0 0.5rem;">Información Básica</legend>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                        <div>
                            <label style="display: block; margin-bottom: 0.25rem; font-weight: 500;">Anilla *</label>
                            <input type="text" name="anilla" value="${bird.anilla || ''}" required 
                                   style="width: 100%; padding: 0.5rem; border: 1px solid var(--border-color); border-radius: var(--radius-md);">
                        </div>
                        <div>
                            <label style="display: block; margin-bottom: 0.25rem; font-weight: 500;">Año Nacimiento</label>
                            <input type="number" name="anio_nacimiento" value="${bird.anio_nacimiento || ''}" 
                                   style="width: 100%; padding: 0.5rem; border: 1px solid var(--border-color); border-radius: var(--radius-md);">
                        </div>
                        <div>
                            <label style="display: block; margin-bottom: 0.25rem; font-weight: 500;">Sexo</label>
                            <select name="sexo" style="width: 100%; padding: 0.5rem; border: 1px solid var(--border-color); border-radius: var(--radius-md);">
                                <option value="?" ${bird.sexo === '?' ? 'selected' : ''}>Pendiente</option>
                                <option value="M" ${bird.sexo === 'M' ? 'selected' : ''}>Macho</option>
                                <option value="H" ${bird.sexo === 'H' ? 'selected' : ''}>Hembra</option>
                            </select>
                        </div>
                    </div>
                </fieldset>

                <!-- Estado y Disponibilidad -->
                <fieldset style="border: 1px solid var(--border-color); padding: 1rem; border-radius: var(--radius-md); margin-bottom: 1.5rem;">
                    <legend style="font-weight: 600; padding: 0 0.5rem;">Estado y Disponibilidad</legend>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                        <div>
                            <label style="display: block; margin-bottom: 0.25rem; font-weight: 500;">Estado</label>
                            <select name="estado" style="width: 100%; padding: 0.5rem; border: 1px solid var(--border-color); border-radius: var(--radius-md);">
                                <option value="Activo" ${bird.estado === 'Activo' ? 'selected' : ''}>Activo</option>
                                <option value="Cedido" ${bird.estado === 'Cedido' ? 'selected' : ''}>Cedido</option>
                                <option value="Vendido" ${bird.estado === 'Vendido' ? 'selected' : ''}>Vendido</option>
                                <option value="Baja" ${bird.estado === 'Baja' ? 'selected' : ''}>Baja</option>
                            </select>
                        </div>
                        <div>
                            <label style="display: flex; gap: 0.5rem; align-items: center; cursor: pointer;">
                                <input type="checkbox" name="disponible_venta" ${Number(bird.disponible_venta) === 1 ? 'checked' : ''}>
                                <span style="font-weight: 500;">Disponible para Cesión</span>
                            </label>
                        </div>
                        <div>
                            <label style="display: flex; gap: 0.5rem; align-items: center; cursor: pointer;">
                                <input type="checkbox" name="reservado" ${Number(bird.reservado) === 1 ? 'checked' : ''}>
                                <span style="font-weight: 500;">Reservado</span>
                            </label>
                        </div>
                        <div>
                            <label style="display: block; margin-bottom: 0.25rem; font-weight: 500;">Precio (€)</label>
                            <input type="number" name="precio" step="0.01" min="0" value="${bird.precio || ''}" placeholder="0.00"
                                   style="width: 200px; padding: 0.5rem; border: 1px solid var(--border-color); border-radius: var(--radius-md);">
                        </div>
                    </div>
                </fieldset>

                <!-- Genética -->
                <fieldset style="border: 1px solid var(--border-color); padding: 1rem; border-radius: var(--radius-md); margin-bottom: 1.5rem;">
                    <legend style="font-weight: 600; padding: 0 0.5rem;">Genética</legend>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                        <div style="grid-column: span 2;">
                            <label style="display: block; margin-bottom: 0.25rem; font-weight: 500;">Especie *</label>
                            <select name="especie" required style="width: 100%; padding: 0.5rem; border: 1px solid var(--border-color); border-radius: var(--radius-md);">
                                <option value="">Seleccionar...</option>
                                <option value="Agapornis Roseicollis" ${bird.especie === 'Agapornis Roseicollis' ? 'selected' : ''}>Agapornis Roseicollis</option>
                                <option value="Agapornis Personatus" ${bird.especie === 'Agapornis Personatus' ? 'selected' : ''}>Agapornis Personatus</option>
                                <option value="Agapornis Fischeri" ${bird.especie === 'Agapornis Fischeri' ? 'selected' : ''}>Agapornis Fischeri</option>
                                <option value="Canario de Color" ${bird.especie === 'Canario de Color' ? 'selected' : ''}>Canario de Color</option>
                                <option value="Canario de Postura" ${bird.especie === 'Canario de Postura' ? 'selected' : ''}>Canario de Postura</option>
                                <option value="Canario de Canto" ${bird.especie === 'Canario de Canto' ? 'selected' : ''}>Canario de Canto</option>
                                <option value="Diamante de Gould" ${bird.especie === 'Diamante de Gould' ? 'selected' : ''}>Diamante de Gould</option>
                                <option value="Ninfas" ${bird.especie === 'Ninfas' ? 'selected' : ''}>Ninfas</option>
                            </select>
                        </div>
                        <div style="grid-column: span 2;">
                            <label style="display: block; margin-bottom: 0.25rem; font-weight: 500;">Mutación Visual</label>
                            <input type="text" name="mutacion_visual" value="${bird.mutacion_visual || ''}"
                                   style="width: 100%; padding: 0.5rem; border: 1px solid var(--border-color); border-radius: var(--radius-md);">
                        </div>
                        <div style="grid-column: span 2;">
                            <label style="display: block; margin-bottom: 0.25rem; font-weight: 500;">Portador de</label>
                            <input type="text" name="portador_de" value="${bird.portador_de || ''}"
                                   style="width: 100%; padding: 0.5rem; border: 1px solid var(--border-color); border-radius: var(--radius-md);">
                        </div>
                    </div>
                </fieldset>

                <!-- Observaciones -->
                <fieldset style="border: 1px solid var(--border-color); padding: 1rem; border-radius: var(--radius-md); margin-bottom: 1.5rem;">
                    <legend style="font-weight: 600; padding: 0 0.5rem;">Observaciones</legend>
                    <textarea name="observaciones" rows="4" style="width: 100%; padding: 0.5rem; border: 1px solid var(--border-color); border-radius: var(--radius-md); resize: vertical;">${bird.observaciones || ''}</textarea>
                </fieldset>

                <!-- Buttons -->
                <div style="display: flex; gap: 1rem; justify-content: flex-end; padding-top: 1rem; border-top: 1px solid var(--border-color);">
                    <button type="button" id="cancel-btn" class="btn" style="background: white; border: 1px solid var(--border-color);">Cancelar</button>
                    <button type="submit" class="btn btn-primary">Guardar Cambios</button>
                </div>
            </form>
        `;

        modal.appendChild(modalContent);
        document.body.appendChild(modal);

        // Form logic
        const form = modalContent.querySelector('#bird-form');
        const estadoSelect = form.querySelector('[name="estado"]');
        const chkDisponible = form.querySelector('[name="disponible_venta"]');
        const chkReservado = form.querySelector('[name="reservado"]');

        // Estado change handler
        function updateCheckboxStates() {
            if (estadoSelect.value !== 'Activo') {
                chkDisponible.checked = false;
                chkReservado.checked = false;
                chkDisponible.disabled = true;
                chkReservado.disabled = true;
            } else {
                chkDisponible.disabled = chkReservado.checked;
                chkReservado.disabled = false;
            }
        }

        // Mutual exclusion logic
        chkReservado.addEventListener('change', () => {
            if (chkReservado.checked) {
                chkDisponible.checked = false;
                chkDisponible.disabled = true;
            } else {
                if (estadoSelect.value === 'Activo') {
                    chkDisponible.disabled = false;
                }
            }
        });

        chkDisponible.addEventListener('change', () => {
            if (chkDisponible.checked) {
                chkReservado.checked = false;
            }
        });

        estadoSelect.addEventListener('change', updateCheckboxStates);
        updateCheckboxStates();

        // Form submit
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = new FormData(form);

            // Ensure checkbox values are always sent
            formData.set('disponible_venta', chkDisponible.checked ? '1' : '0');
            formData.set('reservado', chkReservado.checked ? '1' : '0');

            try {
                // Determine if Create or Update
                const url = bird.id_ave ? `/api/birds/${bird.id_ave}` : '/api/birds';
                const method = bird.id_ave ? 'PUT' : 'POST';

                const response = await fetch(url, {
                    method: method,
                    body: formData
                });

                if (response.ok) {
                    modal.remove();
                    await fetchBirds();
                } else {
                    const err = await response.json();
                    alert('Error: ' + (err.error || 'Error al guardar'));
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error de conexión');
            }
        });

        // Close handlers
        modalContent.querySelector('#close-modal-btn').addEventListener('click', () => modal.remove());
        modalContent.querySelector('#cancel-btn').addEventListener('click', () => modal.remove());
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.remove();
        });
    }

    // Initial HTML
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

            <!-- Filters -->
            <div style="background: white; padding: 1rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border: 1px solid var(--border-color); margin-bottom: 1rem;">
                <div style="display: flex; gap: 1rem; flex-wrap: wrap; align-items: center;">
                    <div style="flex: 1; min-width: 250px;">
                        <input type="text" id="search-input" placeholder="Buscar por anilla, especie o mutación..." 
                               style="width: 100%; padding: 0.5rem 1rem; border: 1px solid var(--border-color); border-radius: var(--radius-md);">
                    </div>
                    <div style="display: flex; gap: 0.5rem;">
                        <button class="filter-btn" data-filter="all" style="padding: 0.5rem 1rem; border: 1px solid var(--border-color); border-radius: var(--radius-md); background: var(--primary-color); color: white; cursor: pointer;">
                            Todos
                        </button>
                        <button class="filter-btn" data-filter="active" style="padding: 0.5rem 1rem; border: 1px solid var(--border-color); border-radius: var(--radius-md); background: white; cursor: pointer;">
                            Activos
                        </button>
                        <button class="filter-btn" data-filter="inactive" style="padding: 0.5rem 1rem; border: 1px solid var(--border-color); border-radius: var(--radius-md); background: white; cursor: pointer;">
                            Histórico
                        </button>
                    </div>
                </div>
            </div>

            <!-- Table -->
            <div style="background: white; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border: 1px solid var(--border-color); overflow: hidden;">
                <table style="width: 100%; border-collapse: collapse;">
                    <thead style="background: #f9fafb; border-bottom: 2px solid var(--border-color);">
                        <tr>
                            <th style="padding: 0.75rem; text-align: left; font-weight: 600; color: var(--text-primary);">Pájaro</th>
                            <th style="padding: 0.75rem; text-align: left; font-weight: 600; color: var(--text-primary);">Especie</th>
                            <th style="padding: 0.75rem; text-align: left; font-weight: 600; color: var(--text-primary);">Sexo</th>
                            <th style="padding: 0.75rem; text-align: left; font-weight: 600; color: var(--text-primary);">Mutación</th>
                            <th style="padding: 0.75rem; text-align: left; font-weight: 600; color: var(--text-primary);">Estado</th>
                            <th style="padding: 0.75rem; text-align: left; font-weight: 600; color: var(--text-primary);">Disponibilidad</th>
                            <th style="padding: 0.75rem; text-align: left; font-weight: 600; color: var(--text-primary);">Acciones</th>
                        </tr>
                    </thead>
                    <tbody id="birds-tbody"></tbody>
                </table>
            </div>
        </div>
    `;

    // Event listeners
    container.querySelector('#search-input').addEventListener('input', (e) => {
        searchTerm = e.target.value;
        applyFilters();
    });

    container.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            currentFilter = btn.dataset.filter;

            // Update button styles
            container.querySelectorAll('.filter-btn').forEach(b => {
                b.style.background = 'white';
                b.style.color = 'var(--text-primary)';
            });
            btn.style.background = 'var(--primary-color)';
            btn.style.color = 'white';

            applyFilters();
        });
    });

    container.querySelector('#new-bird-btn').addEventListener('click', () => {
        openBirdModal(null); // Pass null for new bird
    });

    // Initial load
    await fetchContacts();
    await fetchBirds();

    return container;
};
