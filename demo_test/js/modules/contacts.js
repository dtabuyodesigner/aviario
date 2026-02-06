import { db } from '../core/db.js';


export const ContactsView = async () => {
    const container = document.createElement('div');
    container.className = 'module-contacts';

    // 1. Initial Render (Structure)
    container.innerHTML = `
        <div class="module-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
            <div>
                <h1 style="font-size: 1.8rem; color: var(--primary-color);">Contactos</h1>
                <p style="color: var(--text-secondary);">Agenda de criadores, veterinarios y clientes</p>
            </div>
            <button id="btn-add-contact" class="btn btn-primary" style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.2rem;">+</span> Nuevo Contacto
            </button>
        </div>

        <!-- Filters -->
        <div class="filter-bar" style="margin-bottom: 2rem; display: flex; gap: 1rem; flex-wrap: wrap;">
             <button class="filter-chip active" data-filter="all">Todos</button>
             <button class="filter-chip" data-filter="Criador">Criadores</button>
             <button class="filter-chip" data-filter="Veterinario">Veterinarios</button>
             <button class="filter-chip" data-filter="Comprador">Compradores</button>
             <button class="filter-chip" data-filter="Otro">Otros</button>
        </div>

        <!-- Contacts Grid -->
        <div id="contacts-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem;">
            <!-- Loading -->
            <p style="grid-column: 1/-1; text-align: center; color: var(--text-secondary);">Cargando agenda...</p>
        </div>

        <!-- Modal -->
        <div id="modal-contact" class="modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; justify-content: center; align-items: center;">
            <div style="background: white; width: 90%; max-width: 500px; padding: 2rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-xl);">
                <h2 id="modal-title" style="margin-top: 0; margin-bottom: 1.5rem; color: var(--text-primary);">Nuevo Contacto</h2>
                
                <form id="form-contact" style="display: flex; flex-direction: column; gap: 1rem;">
                    <input type="hidden" id="contact-id">
                    
                    <div class="form-group">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Tipo *</label>
                        <select id="tipo" required style="width: 100%; padding: 0.75rem; border: 1px solid var(--border-color); border-radius: var(--radius-sm);">
                            <option value="Criador">Criador</option>
                            <option value="Veterinario">Veterinario</option>
                            <option value="Comprador">Comprador</option>
                            <option value="Vendedor">Vendedor</option>
                            <option value="Otro">Otro</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Nombre / Razón Social *</label>
                        <input type="text" id="nombre" required style="width: 100%; padding: 0.75rem; border: 1px solid var(--border-color); border-radius: var(--radius-sm);">
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <div class="form-group">
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">DNI / CIF</label>
                            <input type="text" id="dni" style="width: 100%; padding: 0.75rem; border: 1px solid var(--border-color); border-radius: var(--radius-sm);">
                        </div>
                        <div class="form-group">
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Nº Criador</label>
                            <input type="text" id="cn" style="width: 100%; padding: 0.75rem; border: 1px solid var(--border-color); border-radius: var(--radius-sm);">
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                         <div class="form-group">
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Teléfono</label>
                            <input type="tel" id="telefono" style="width: 100%; padding: 0.75rem; border: 1px solid var(--border-color); border-radius: var(--radius-sm);">
                        </div>
                         <div class="form-group">
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Email</label>
                            <input type="email" id="email" style="width: 100%; padding: 0.75rem; border: 1px solid var(--border-color); border-radius: var(--radius-sm);">
                        </div>
                    </div>

                    <div class="form-group">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Dirección</label>
                        <textarea id="direccion" rows="2" style="width: 100%; padding: 0.75rem; border: 1px solid var(--border-color); border-radius: var(--radius-sm); font-family: inherit;"></textarea>
                    </div>

                    <div style="display: flex; justify-content: flex-end; gap: 1rem; margin-top: 1rem;">
                        <button type="button" id="btn-cancel" class="btn" style="background: transparent; border: 1px solid var(--border-color);">Cancelar</button>
                        <button type="submit" class="btn btn-primary">Guardar</button>
                    </div>
                </form>
            </div>
        </div>
    `;

    // 2. State & Logic
    let contacts = [];
    const grid = container.querySelector('#contacts-grid');
    const modal = container.querySelector('#modal-contact');
    const form = container.querySelector('#form-contact');

    // Load Data
    const loadContacts = async () => {
        try {
            const response = await fetch('/api/contacts');
            if (response.ok) {
                contacts = await response.json();
                renderContacts('all');
            }
        } catch (e) {
            console.error("Error loading contacts", e);
            grid.innerHTML = '<p style="color: red;">Error al cargar contactos.</p>';
        }
    };

    // Render Grid
    const renderContacts = (filterType) => {
        grid.innerHTML = '';

        const filtered = filterType === 'all'
            ? contacts
            : contacts.filter(c => c.tipo === filterType);

        if (filtered.length === 0) {
            grid.innerHTML = `
                <div style="grid-column: 1/-1; text-align: center; padding: 3rem; background: #f8fafc; border-radius: var(--radius-lg); border: 2px dashed var(--border-color);">
                    <p style="color: var(--text-secondary); margin-bottom: 1rem;">No se encontraron contactos.</p>
                    ${filterType === 'all' ? '<button id="btn-empty-add" class="btn btn-primary">Añadir el primero</button>' : ''}
                </div>
            `;
            if (filterType === 'all') {
                container.querySelector('#btn-empty-add')?.addEventListener('click', openModalNew);
            }
            return;
        }

        filtered.forEach(c => {
            const card = document.createElement('div');
            card.className = 'contact-card';
            card.style.cssText = `
                background: white; 
                padding: 1.5rem; 
                border-radius: var(--radius-lg); 
                box-shadow: var(--shadow-sm); 
                border: 1px solid var(--border-color);
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
                position: relative;
                transition: transform 0.2s, box-shadow 0.2s;
            `;

            // Badge color based on type
            let badgeColor = '#64748b';
            if (c.tipo === 'Criador') badgeColor = '#10b981';
            if (c.tipo === 'Veterinario') badgeColor = '#ef4444';
            if (c.tipo === 'Comprador') badgeColor = '#3b82f6';

            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                    <span style="background: ${badgeColor}; color: white; padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.75rem; font-weight: 600;">${c.tipo}</span>
                    <div style="display: flex; gap: 0.5rem;">
                        <button class="btn-edit-contact" data-id="${c.id_contacto}" style="background: none; border: none; cursor: pointer; font-size: 1.1rem;" title="Editar">✏️</button>
                        <button class="btn-del-contact" data-id="${c.id_contacto}" style="background: none; border: none; cursor: pointer; font-size: 1.1rem;" title="Borrar">🗑️</button>
                    </div>
                </div>
                
                <h3 style="margin: 0; font-size: 1.1rem; color: var(--text-primary);">${c.nombre_razon_social}</h3>
                
                ${c.n_criador ? `<p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);">CN: <strong>${c.n_criador}</strong></p>` : ''}
                
                <div style="margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid #f1f5f9; font-size: 0.9rem;">
                    ${c.telefono ? `<p style="margin: 0.25rem 0;">📞 ${c.telefono}</p>` : ''}
                    ${c.email ? `<p style="margin: 0.25rem 0;">✉️ ${c.email}</p>` : ''}
                    ${c.direccion ? `<p style="margin: 0.25rem 0; color: var(--text-secondary); font-style: italic;">📍 ${c.direccion}</p>` : ''}
                </div>
            `;

            // Hover effect
            card.onmouseenter = () => { card.style.transform = 'translateY(-2px)'; card.style.boxShadow = 'var(--shadow-md)'; };
            card.onmouseleave = () => { card.style.transform = 'none'; card.style.boxShadow = 'var(--shadow-sm)'; };

            grid.appendChild(card);
        });

        // Event Delegation for Edit/Delete
        grid.querySelectorAll('.btn-edit-contact').forEach(btn => {
            btn.addEventListener('click', (e) => openModalEdit(e.target.dataset.id));
        });
        grid.querySelectorAll('.btn-del-contact').forEach(btn => {
            btn.addEventListener('click', (e) => deleteContact(e.target.dataset.id));
        });
    };

    // Modal Actions
    const openModalNew = () => {
        form.reset();
        container.querySelector('#contact-id').value = '';
        container.querySelector('#modal-title').textContent = 'Nuevo Contacto';
        modal.style.display = 'flex';
    };

    const openModalEdit = (id) => {
        const contact = contacts.find(c => c.id_contacto == id);
        if (!contact) return;

        container.querySelector('#contact-id').value = contact.id_contacto;
        container.querySelector('#tipo').value = contact.tipo;
        container.querySelector('#nombre').value = contact.nombre_razon_social;
        container.querySelector('#dni').value = contact.dni_cif || '';
        container.querySelector('#cn').value = contact.n_criador || '';
        container.querySelector('#telefono').value = contact.telefono || '';
        container.querySelector('#email').value = contact.email || '';
        container.querySelector('#direccion').value = contact.direccion || '';

        container.querySelector('#modal-title').textContent = 'Editar Contacto';
        modal.style.display = 'flex';
    };

    const closeModal = () => {
        modal.style.display = 'none';
        form.reset();
    };

    // Form Submit
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = container.querySelector('#contact-id').value;
        const data = {
            tipo: container.querySelector('#tipo').value,
            nombre_razon_social: container.querySelector('#nombre').value,
            dni_cif: container.querySelector('#dni').value,
            n_criador: container.querySelector('#cn').value,
            telefono: container.querySelector('#telefono').value,
            email: container.querySelector('#email').value,
            direccion: container.querySelector('#direccion').value
        };

        try {
            if (id) {
                // Update
                const res = await fetch(`/api/contacts/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (!res.ok) throw new Error('Error updating');
            } else {
                // Create
                const res = await fetch('/api/contacts', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (!res.ok) throw new Error('Error creating');
            }
            closeModal();
            loadContacts(); // Reload list
        } catch (err) {
            alert("Error al guardar: " + err.message);
        }
    });

    // Delete Action
    const deleteContact = async (id) => {
        if (!confirm('¿Seguro que quieres borrar este contacto?')) return;

        try {
            const res = await fetch(`/api/contacts/${id}`, { method: 'DELETE' });
            if (res.ok) {
                loadContacts();
            } else {
                alert("No se pudo borrar el contacto.");
            }
        } catch (err) {
            console.error(err);
        }
    };

    // Event Listeners
    container.querySelector('#btn-add-contact').addEventListener('click', openModalNew);
    container.querySelector('#btn-cancel').addEventListener('click', closeModal);

    // Close modal on outside click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });

    // Filters
    container.querySelectorAll('.filter-chip').forEach(chip => {
        chip.addEventListener('click', (e) => {
            // Remove active class
            container.querySelectorAll('.filter-chip').forEach(c => {
                c.style.background = 'transparent';
                c.style.color = 'var(--text-secondary)';
                c.style.borderColor = 'var(--border-color)';
            });
            // Add active style to clicked
            e.target.style.background = 'var(--primary-color)';
            e.target.style.color = 'white';
            e.target.style.borderColor = 'var(--primary-color)';

            renderContacts(e.target.dataset.filter);
        });
    });

    // Set initial filter style
    const initialChip = container.querySelector('.filter-chip[data-filter="all"]');
    if (initialChip) {
        initialChip.style.background = 'var(--primary-color)';
        initialChip.style.color = 'white';
        initialChip.style.borderColor = 'var(--primary-color)';
    }

    // Init
    loadContacts();

    return container;
};

