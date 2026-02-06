
import { db } from '../core/db.js';

export const LegalView = async () => {
    const div = document.createElement('div');
    div.className = 'module-legal';

    div.innerHTML = `
        <div style="margin-bottom: 2rem;">
            <h1 style="color: var(--primary-color);">📄 Cesión de Animales</h1>
            <p style="color: var(--text-secondary);">Genera documentos de cesión para tus ejemplares.</p>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
            <!-- Form -->
            <div style="background: white; padding: 2rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border: 1px solid var(--border-color);">
                <h2 style="margin-top: 0; color: var(--primary-color); border-bottom: 2px solid #f1f5f9; padding-bottom: 1rem; margin-bottom: 1.5rem;">📝 Datos de la Cesión</h2>
                
                <div style="display: grid; gap: 1rem;">
                     <!-- Cedente (Read-only) -->
                    <div>
                         <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Cedente (Tú)</label>
                         <input id="legal-cedente" type="text" class="form-input" style="width: 100%; background: #f8fafc;" disabled value="Cargando datos...">
                         <a href="#/settings" style="font-size: 0.85rem; color: var(--primary-color);">Editar mis datos en Ajustes</a>
                    </div>

                    <!-- Cesionario -->
                    <div>
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Cesionario (Adquirente)</label>
                        <select id="legal-cesionario" class="form-input" style="width: 100%;">
                            <option value="">-- Seleccionar Contacto --</option>
                        </select>
                         <a href="#/contacts" style="font-size: 0.85rem; color: var(--primary-color);">Crear nuevo contacto</a>
                    </div>

                    <!-- Fecha y Lugar -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <div>
                             <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Fecha</label>
                             <input id="legal-fecha" type="date" class="form-input" style="width: 100%;">
                        </div>
                        <div>
                             <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Lugar (Ciudad)</label>
                             <input id="legal-lugar" type="text" class="form-input" style="width: 100%;" placeholder="Ej: Madrid">
                        </div>
                    </div>
                </div>
            </div>

            <!-- Birds Selection -->
            <div style="background: white; padding: 2rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border: 1px solid var(--border-color);">
                <h2 style="margin-top: 0; color: var(--primary-color); border-bottom: 2px solid #f1f5f9; padding-bottom: 1rem; margin-bottom: 1.5rem;">🐦 Ejemplares a Ceder</h2>
                <p style="color: var(--text-secondary); margin-bottom: 1rem;">Selecciona los pájaros que incluirá el documento.</p>

                <div style="height: 300px; overflow-y: auto; border: 1px solid var(--border-color); border-radius: var(--radius-md);">
                    <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
                        <thead style="background: #f8fafc; position: sticky; top: 0;">
                            <tr>
                                <th style="padding: 0.75rem; text-align: left;"><input type="checkbox" id="check-all" style="cursor: pointer;"></th>
                                <th style="padding: 0.75rem; text-align: left;">Anilla</th>
                                <th style="padding: 0.75rem; text-align: left;">Especie</th>
                                <th style="padding: 0.75rem; text-align: left;">Año</th>
                            </tr>
                        </thead>
                        <tbody id="legal-birds-list">
                            <!-- Populated dynamically -->
                        </tbody>
                    </table>
                </div>
                
                <div style="margin-top: 0.5rem; display: flex; align-items: center; gap: 0.5rem;">
                     <input type="checkbox" id="filter-sale" checked> 
                     <label for="filter-sale" style="font-size: 0.9rem; color: var(--text-primary); cursor: pointer;">Mostrar solo disponibles para cesión</label>
                </div>

                <div style="margin-top: 1rem; text-align: right;">
                    <span id="selected-count" style="margin-right: 1rem; color: var(--text-secondary); font-weight: 500;">0 seleccionados</span>
                    <button id="btn-generate-doc" class="btn btn-primary">📄 Generar Documento</button>
                </div>
            </div>
        </div>
    `;

    // Initialize State
    let config = {};
    let activeBirds = [];
    const selectedBirdIds = new Set();
    let currentVisibleBirds = [];

    // Render Function
    const renderBirds = () => {
        const tbody = div.querySelector('#legal-birds-list');
        tbody.innerHTML = '';

        const filterSale = div.querySelector('#filter-sale').checked;
        currentVisibleBirds = activeBirds.filter(b => !filterSale || b.disponible_venta);

        currentVisibleBirds.forEach(b => {
            const tr = document.createElement('tr');
            tr.style.borderBottom = '1px solid #f1f5f9';
            tr.innerHTML = `
                <td style="padding: 0.75rem;"><input type="checkbox" class="bird-check" value="${b.id_ave}" ${selectedBirdIds.has(b.id_ave) ? 'checked' : ''}></td>
                <td style="padding: 0.75rem; font-weight: 500;">${b.anilla}</td>
                <td style="padding: 0.75rem;">
                    ${b.especie}<br>
                    <span style="font-size: 0.8rem; color: var(--text-secondary);">${b.mutacion_visual || ''}</span>
                </td>
                <td style="padding: 0.75rem;">${b.anio_nacimiento}</td>
            `;
            tbody.appendChild(tr);
        });

        // Update count based on intersection of Selected & Visible
        updateCounter();

        // Update check-all state
        const allVisibleSelected = currentVisibleBirds.length > 0 && currentVisibleBirds.every(b => selectedBirdIds.has(b.id_ave));
        div.querySelector('#check-all').checked = allVisibleSelected;
    };

    const updateCounter = () => {
        // Count only selected birds that are currently visible
        const visibleSelectedCount = currentVisibleBirds.filter(b => selectedBirdIds.has(b.id_ave)).length;
        div.querySelector('#selected-count').textContent = `${visibleSelectedCount} seleccionados`;
    };

    try {
        // Load Data
        const [configData, contacts, birds] = await Promise.all([
            fetch('/api/config').then(r => r.json()),
            db.getAll('contacts'),
            db.getAll('birds')
        ]);
        config = configData;

        // Populate Cedente
        const inputCedente = div.querySelector('#legal-cedente');
        inputCedente.value = `${config.nombre_criador || ''} - ${config.n_criador_nacional || ''} (DNI ${config.dni || ''})`;

        // Populate Date/Place
        div.querySelector('#legal-fecha').valueAsDate = new Date();
        if (config.direccion_poblacion) {
            div.querySelector('#legal-lugar').value = config.direccion_poblacion;
        }

        // Active Birds
        activeBirds = birds.filter(b => b.estado === 'Activo');

        const selContacts = div.querySelector('#legal-cesionario');
        contacts.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c.id_contacto;
            opt.textContent = `${c.nombre_razon_social} (${c.dni_cif || 'Sin DNI'})`;
            selContacts.appendChild(opt);
        });

        renderBirds();

    } catch (e) {
        console.error("Error loading legal module data", e);
        div.innerHTML += `<p class="error">Error al cargar datos: ${e.message}</p>`;
    }

    // Event Listeners
    div.querySelector('#filter-sale').addEventListener('change', renderBirds);

    div.querySelector('#check-all').addEventListener('change', (e) => {
        const isChecked = e.target.checked;
        const checks = div.querySelectorAll('.bird-check');

        checks.forEach(c => c.checked = isChecked);

        // Update Set based on VISIBLE birds only
        currentVisibleBirds.forEach(b => {
            if (isChecked) selectedBirdIds.add(b.id_ave);
            else selectedBirdIds.delete(b.id_ave);
        });

        updateCounter();
    });

    div.querySelector('#legal-birds-list').addEventListener('change', (e) => {
        if (e.target.classList.contains('bird-check')) {
            const id = parseInt(e.target.value);
            if (e.target.checked) selectedBirdIds.add(id);
            else selectedBirdIds.delete(id);

            updateCounter();

            // Uncheck "all" if one is unchecked (simple logic)
            if (!e.target.checked) div.querySelector('#check-all').checked = false;
        }
    });

    div.querySelector('#btn-generate-doc').onclick = async () => {
        const cesionarioId = div.querySelector('#legal-cesionario').value;
        if (!cesionarioId) return alert("Por favor seleccione un Cesionario (Adquirente).");
        if (selectedBirdIds.size === 0) return alert("Seleccione al menos un pájaro.");

        const cesionario = (await db.getAll('contacts')).find(c => c.id_contacto == cesionarioId);

        // Filter birds: Must be SELECTED AND VISIBLE (respecting the filter)
        const filterSale = div.querySelector('#filter-sale').checked;
        const visibleBirds = activeBirds.filter(b => !filterSale || b.disponible_venta);
        const birdsToInclude = visibleBirds.filter(b => selectedBirdIds.has(b.id_ave));

        if (birdsToInclude.length === 0) return alert("No hay pájaros seleccionados visibles para incluir.");

        const fecha = div.querySelector('#legal-fecha').value;
        const lugar = div.querySelector('#legal-lugar').value;

        generatePDF(config, cesionario, birdsToInclude, fecha, lugar);
    };

    return div;
};

const generatePDF = (cedente, cesionario, birds, fecha, lugar) => {
    // Basic HTML Template for Print
    const win = window.open('', '_blank');
    const birdRows = birds.map(b => `
        <tr>
            <td style="border: 1px solid #000; padding: 5px;">${b.especie || ''}</td>
            <td style="border: 1px solid #000; padding: 5px;">${b.mutacion_visual || ''}</td>
            <td style="border: 1px solid #000; padding: 5px;">${b.anilla}</td>
            <td style="border: 1px solid #000; padding: 5px;">${b.sexo}</td>
            <td style="border: 1px solid #000; padding: 5px;">${b.anio_nacimiento}</td>
        </tr>
    `).join('');

    // Format date in spanish (e.g. 5 de Febrero de 2024)
    const dateObj = new Date(fecha);
    const dateFormatted = dateObj.toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' });

    const html = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Cesión de Aves</title>
            <style>
                body { font-family: 'Times New Roman', serif; padding: 40px; }
                h1 { text-align: center; font-size: 18px; text-transform: uppercase; margin-bottom: 30px; }
                .section { margin-bottom: 20px; }
                .label { font-weight: bold; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 12px; }
                .signature-box { display: flex; justify-content: space-between; margin-top: 50px; }
                .sign { width: 45%; border-top: 1px solid #000; text-align: center; padding-top: 10px; }
            </style>
        </head>
        <body>
            <h1>Documento de Cesión de Aves</h1>
            
            <div class="section">
                <!-- Ensure Lugar and Fecha are rendered -->
                <p>En <strong>${lugar || '_____________'}</strong>, a ${dateFormatted}</p>
            </div>

            <div class="section" style="border: 1px solid #ccc; padding: 10px;">
                <p><strong>CEDENTE (Criador):</strong></p>
                <p>${cedente.nombre_criador}</p>
                <p>DNI: ${cedente.dni || ''} - N.º Criador: ${cedente.n_criador_nacional || ''}</p>
                <p>
                    ${cedente.direccion_calle || cedente.direccion || ''}<br>
                    ${cedente.direccion_cp || ''} ${cedente.direccion_poblacion || ''} (${cedente.direccion_provincia || ''})
                </p>
            </div>

            <div class="section" style="border: 1px solid #ccc; padding: 10px;">
                <p><strong>CESIONARIO (Adquirente):</strong></p>
                <p>${cesionario.nombre_razon_social}</p>
                <p>DNI: ${cesionario.dni_cif || ''} - N.º Registro: ${cesionario.n_criador || ''}</p>
                <p>${cesionario.direccion || ''}</p>
            </div>

            <p>EL CEDENTE declara ceder al CESIONARIO los ejemplares descritos a continuación, nacidos en cautividad:</p>

            <table>
                <thead>
                    <tr>
                        <th style="border: 1px solid #000; background: #eee;">Especie</th>
                        <th style="border: 1px solid #000; background: #eee;">Mutación</th>
                        <th style="border: 1px solid #000; background: #eee;">Anilla</th>
                        <th style="border: 1px solid #000; background: #eee;">Sexo</th>
                        <th style="border: 1px solid #000; background: #eee;">Año</th>
                    </tr>
                </thead>
                <tbody>
                    ${birdRows}
                </tbody>
            </table>

            <p style="font-size: 10px; margin-top: 20px;">
                Las aves cedidas proceden de cría en cautividad y cumplen con l normativa vigente. 
                El cesionario asume la responsabilidad del mantenimiento y bienestar de los animales desde la fecha de esta cesión.
            </p>

            <div class="signature-box" style="margin-top: 100px;">
                <div class="sign">Fdo. EL CEDENTE</div>
                <div class="sign">Fdo. EL CESIONARIO</div>
            </div>

             <script>
                window.onload = function() { window.print(); }
            </script>
        </body>
        </html>
    `;

    win.document.write(html);
    win.document.close();
};
