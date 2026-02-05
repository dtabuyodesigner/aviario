
export const SettingsView = async () => {
    const div = document.createElement('div');
    div.className = 'module-settings';

    div.innerHTML = `
        <div style="margin-bottom: 2rem;">
            <h1 style="color: var(--primary-color);">⚙️ Configuración y Sistema</h1>
            <p style="color: var(--text-secondary);">Selecciona una herramienta para administrar tu aviario.</p>
        </div>

        <!-- System Hub Grid -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
            
            <!-- Button: Profile -->
            <div id="btn-open-profile" style="background: white; padding: 2rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border: 1px solid var(--border-color); cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">👤</div>
                <h3 style="margin: 0; color: var(--text-primary);">Perfil Criador</h3>
                <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.5rem;">Datos personales, dirección y logo.</p>
            </div>

            <!-- Button: Backup -->
            <div id="btn-open-backup" style="background: white; padding: 2rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border: 1px solid var(--border-color); cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">📦</div>
                <h3 style="margin: 0; color: var(--text-primary);">Copia de Seguridad</h3>
                <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.5rem;">Exportar base de datos.</p>
            </div>

            <!-- Button: Restore -->
            <div id="btn-open-restore" style="background: white; padding: 2rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border: 1px solid var(--border-color); cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">⚠️</div>
                <h3 style="margin: 0; color: var(--text-primary);">Restaurar Datos</h3>
                <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.5rem;">Recuperar desde archivo.</p>
            </div>

             <!-- Button: Manual (Placeholder) -->
            <div style="background: #f1f5f9; padding: 2rem; border-radius: var(--radius-lg); border: 1px dashed var(--border-color); text-align: center; opacity: 0.7;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">📘</div>
                <h3 style="margin: 0; color: var(--text-secondary);">Manual de Uso</h3>
                <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.5rem;">Próximamente...</p>
            </div>
        </div>

        <div style="margin-top: 3rem; text-align: center; color: var(--text-secondary); font-size: 0.85rem;">
            <p>AviarioManager v1.0.0 &bull; Base de Datos SQLite3</p>
        </div>


        <!-- MODAL: Profile -->
        <div id="modal-profile" class="modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; justify-content: center; align-items: center;">
            <div style="background: white; padding: 2rem; border-radius: var(--radius-lg); width: 90%; max-width: 600px; max-height: 90vh; overflow-y: auto; position: relative;">
                <button class="btn-close-modal" style="position: absolute; top: 1rem; right: 1rem; background: none; border: none; font-size: 1.5rem; cursor: pointer;">&times;</button>
                <h2 style="margin-top: 0; margin-bottom: 1.5rem; color: var(--primary-color);">Editar Perfil de Criador</h2>
                
                <div style="display: grid; gap: 1rem;">
                    <div>
                        <label style="display: block; margin-bottom: 0.5rem; color: var(--text-secondary); font-size: 0.85rem; font-weight: 500;">Nombre / Razón Social</label>
                        <input id="conf-name" type="text" class="form-input" style="width: 100%; font-weight: 600;">
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                         <div>
                            <label style="display: block; margin-bottom: 0.5rem; color: var(--text-secondary); font-size: 0.85rem; font-weight: 500;">N.º Criador</label>
                            <input id="conf-cn" type="text" class="form-input" style="width: 100%;">
                        </div>
                         <div>
                            <label style="display: block; margin-bottom: 0.5rem; color: var(--text-secondary); font-size: 0.85rem; font-weight: 500;">DNI / NIF</label>
                            <input id="conf-dni" type="text" class="form-input" style="width: 100%;">
                        </div>
                    </div>
                     <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                         <div>
                            <label style="display: block; margin-bottom: 0.5rem; color: var(--text-secondary); font-size: 0.85rem; font-weight: 500;">Teléfono</label>
                            <input id="conf-phone" type="text" class="form-input" style="width: 100%;">
                        </div>
                         <div>
                            <label style="display: block; margin-bottom: 0.5rem; color: var(--text-secondary); font-size: 0.85rem; font-weight: 500;">Email</label>
                            <input id="conf-email" type="email" class="form-input" style="width: 100%;">
                        </div>
                    </div>
                    
                    <div style="background: #f8fafc; padding: 1rem; border-radius: var(--radius-md); border: 1px dashed var(--border-color);">
                        <label style="display: block; margin-bottom: 0.5rem; color: var(--text-primary); font-weight: 600;">Dirección</label>
                        <input id="conf-street" type="text" class="form-input" placeholder="Calle..." style="width: 100%; margin-bottom: 0.5rem;">
                        <div style="display: grid; grid-template-columns: 80px 1fr 1fr; gap: 0.5rem;">
                            <input id="conf-cp" type="text" class="form-input" placeholder="CP">
                            <input id="conf-town" type="text" class="form-input" placeholder="Población">
                            <input id="conf-province" type="text" class="form-input" placeholder="Provincia">
                        </div>
                    </div>

                    <div>
                            <label style="display: block; margin-bottom: 0.5rem; color: var(--text-secondary); font-size: 0.85rem; font-weight: 500;">URL Logo</label>
                            <input id="conf-logo" type="text" class="form-input" placeholder="https://..." style="width: 100%;">
                    </div>

                    <button id="btn-save-config" class="btn btn-primary" style="margin-top: 1rem;">💾 Guardar Cambios</button>
                </div>
            </div>
        </div>

        <!-- MODAL: Backup -->
        <div id="modal-backup" class="modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; justify-content: center; align-items: center;">
            <div style="background: white; padding: 2rem; border-radius: var(--radius-lg); width: 90%; max-width: 400px; text-align: center; position: relative;">
                <button class="btn-close-modal" style="position: absolute; top: 1rem; right: 1rem; background: none; border: none; font-size: 1.5rem; cursor: pointer;">&times;</button>
                <div style="font-size: 3rem; margin-bottom: 1rem;">📦</div>
                <h2 style="margin: 0 0 1rem 0;">Copia de Seguridad</h2>
                <p style="color: var(--text-secondary); margin-bottom: 2rem;">Haz clic abajo para descargar una copia completa de tu base de datos.</p>
                
                <a href="/api/backup" target="_blank" class="btn" style="background: #0ea5e9; color: white; display: inline-block; padding: 1rem 2rem; text-decoration: none; border-radius: var(--radius-md); font-weight: 600;">⬇️ Descargar .db</a>
            </div>
        </div>

        <!-- MODAL: Restore -->
        <div id="modal-restore" class="modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; justify-content: center; align-items: center;">
            <div style="background: white; padding: 2rem; border-radius: var(--radius-lg); width: 90%; max-width: 400px; text-align: center; position: relative; border-top: 4px solid #ef4444;">
                <button class="btn-close-modal" style="position: absolute; top: 1rem; right: 1rem; background: none; border: none; font-size: 1.5rem; cursor: pointer;">&times;</button>
                <div style="font-size: 3rem; margin-bottom: 1rem;">⚠️</div>
                <h2 style="margin: 0 0 1rem 0; color: #b91c1c;">Restaurar Datos</h2>
                <p style="color: var(--text-secondary); margin-bottom: 1.5rem; font-size: 0.9rem;">
                    Selecciona un archivo <code>.db</code>. <br>
                    <strong style="color: #ef4444;">ESTA ACCIÓN BORRARÁ TODOS LOS DATOS ACTUALES.</strong>
                </p>
                
                <input type="file" id="file-restore" accept=".db" style="margin-bottom: 1.5rem; width: 100%; padding: 0.5rem; border: 1px solid var(--border-color); border-radius: var(--radius-md);">
                <button id="btn-restore-action" class="btn" style="background: #ef4444; color: white; width: 100%; padding: 1rem; font-weight: 600;">🔄 Restaurar Copia</button>
            </div>
        </div>
    `;


    // Load initial data
    try {
        const response = await fetch('/api/config');
        const config = await response.json();

        // Helper to set values only if element exists
        const setVal = (selector, val) => {
            const el = div.querySelector(selector);
            if (el && val) el.value = val;
        };

        setVal('#conf-name', config.nombre_criador);
        setVal('#conf-cn', config.n_criador_nacional);
        setVal('#conf-dni', config.dni);
        setVal('#conf-phone', config.telefono);
        setVal('#conf-email', config.email);
        setVal('#conf-street', config.direccion_calle);
        setVal('#conf-cp', config.direccion_cp);
        setVal('#conf-town', config.direccion_poblacion);
        setVal('#conf-province', config.direccion_provincia);
        setVal('#conf-logo', config.logo_path);

    } catch (e) {
        console.error("Error loading config", e);
    }

    // Modal Handling Logic
    const openModal = (id) => {
        const modal = div.querySelector(id);
        if (modal) modal.style.display = 'flex';
    };

    const closeModal = (modal) => {
        modal.style.display = 'none';
    };

    // Open Modals
    div.querySelector('#btn-open-profile').onclick = () => openModal('#modal-profile');
    div.querySelector('#btn-open-backup').onclick = () => openModal('#modal-backup');
    div.querySelector('#btn-open-restore').onclick = () => openModal('#modal-restore');

    // Close Modals (Buttons & Background)
    div.querySelectorAll('.modal').forEach(modal => {
        modal.onclick = (e) => {
            if (e.target === modal) closeModal(modal);
        };
        modal.querySelector('.btn-close-modal').onclick = () => closeModal(modal);
    });

    // Profile Save Logic
    div.querySelector('#btn-save-config').onclick = async () => {
        const getVal = (selector) => {
            const el = div.querySelector(selector);
            return el ? el.value : '';
        };

        const data = {
            nombre_criador: getVal('#conf-name'),
            n_criador_nacional: getVal('#conf-cn'),
            dni: getVal('#conf-dni'),
            telefono: getVal('#conf-phone'),
            email: getVal('#conf-email'),
            direccion_calle: getVal('#conf-street'),
            direccion_cp: getVal('#conf-cp'),
            direccion_poblacion: getVal('#conf-town'),
            direccion_provincia: getVal('#conf-province'),
            direccion: `${getVal('#conf-street')}, ${getVal('#conf-cp')} ${getVal('#conf-town')} (${getVal('#conf-province')})`, // Fallback
            logo_path: getVal('#conf-logo')
        };

        try {
            const res = await fetch('/api/config', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            if (res.ok) {
                alert('✅ Configuración guardada correctamente.');
                closeModal(div.querySelector('#modal-profile'));
            } else {
                alert('❌ Error al guardar.');
            }
        } catch (e) {
            alert('Error: ' + e.message);
        }
    };

    // Restore Logic
    div.querySelector('#btn-restore-action').onclick = async () => {
        const fileInput = div.querySelector('#file-restore');
        if (fileInput.files.length === 0) return alert("Por favor seleccione un archivo .db primero.");

        if (!confirm("⚠️ ¿ESTÁS SEGURO?\n\nEsta acción borrará TODOS los datos actuales y los reemplazará por la copia de seguridad. NO SE PUEDE DESHACER.")) {
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        try {
            const res = await fetch('/api/restore', {
                method: 'POST',
                body: formData
            });

            if (res.ok) {
                alert("✅ Sistema restaurado correctamente. La página se recargará.");
                location.reload();
            } else {
                const err = await res.json();
                alert("❌ Error al restaurar: " + (err.error || 'Error desconocido'));
            }
        } catch (e) {
            alert('Error crítico: ' + e.message);
        }
    };

    return div;
};
