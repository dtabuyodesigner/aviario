
import { db } from '../core/db.js';

export const HealthView = async () => {
    const div = document.createElement('div');
    div.className = 'module-health';

    // Header
    div.innerHTML = `
        <div class="module-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
            <div>
                <h1 style="font-size: 1.8rem; color: var(--primary-color); margin: 0;">🏥 Salud y Hospital</h1>
                <p style="color: var(--text-secondary); margin: 0.5rem 0 0 0;">Gestión sanitaria, tratamientos y botiquín.</p>
            </div>
            <div style="display: flex; gap: 1rem;">
                <button id="btn-new-recipe" class="btn" style="background: white; border: 1px solid var(--border-color);">💊 Nueva Receta</button>
                <button id="btn-new-treatment" class="btn btn-primary">+ Nuevo Tratamiento</button>
            </div>
        </div>

        <!-- Tabs -->
        <div class="tabs" style="display: flex; border-bottom: 2px solid var(--border-color); margin-bottom: 2rem;">
            <button class="tab-btn active" data-tab="active" style="padding: 1rem 2rem; border: none; background: none; font-weight: 600; color: var(--primary-color); border-bottom: 2px solid var(--primary-color); cursor: pointer;">Hospital (Activos)</button>
            <button class="tab-btn" data-tab="history" style="padding: 1rem 2rem; border: none; background: none; font-weight: 500; color: var(--text-secondary); cursor: pointer;">Historial Médico</button>
            <button class="tab-btn" data-tab="recipes" style="padding: 1rem 2rem; border: none; background: none; font-weight: 500; color: var(--text-secondary); cursor: pointer;">Botiquín (Recetas)</button>
        </div>

        <!-- Content Areas -->
        <div id="tab-content-active" class="tab-content">
            <div id="treatments-active-list" style="display: grid; gap: 1rem;">Cargando...</div>
        </div>
        
        <div id="tab-content-history" class="tab-content" style="display: none;">
            <div id="treatments-history-table">Cargando...</div>
        </div>
        
        <div id="tab-content-recipes" class="tab-content" style="display: none;">
            <div id="recipes-list" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem;">Cargando...</div>
        </div>
    `;

    // Data Fetching
    const loadData = async () => {
        try {
            const [active, all, recipes, birds] = await Promise.all([
                fetch('/api/treatments?active=true').then(r => r.json()),
                fetch('/api/treatments').then(r => r.json()),
                fetch('/api/recipes').then(r => r.json()),
                db.getAll('birds')
            ]);

            renderActiveTreatments(active);
            renderHistory(all);
            renderRecipes(recipes);

            // Setup Modal Logic with fresh data
            setupModals(birds, recipes);
        } catch (e) {
            console.error("Error loading health data", e);
            div.querySelector('#tab-content-active').innerHTML = `<p style="color: red;">Error cargando datos: ${e.message}</p>`;
        }
    };

    // Renderers
    const renderActiveTreatments = (list) => {
        const container = div.querySelector('#treatments-active-list');
        if (list.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; padding: 4rem; background: #f8fafc; border-radius: var(--radius-lg); border: 2px dashed var(--border-color);">
                    <p style="color: var(--text-secondary); font-size: 1.1rem;">No hay aves en tratamiento activo actualmente.</p>
                    <p style="color: #10b981; font-weight: 600;">¡Buena señal! 🌿</p>
                </div>
            `;
            return;
        }

        const today = new Date().toISOString().split('T')[0];

        container.innerHTML = list.map(t => {
            // Calculate alert status
            let alertHtml = '';
            if (t.fecha_fin) {
                if (t.fecha_fin < today) {
                    alertHtml = `<div style="margin-top:0.5rem; background: #fee2e2; color: #991b1b; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem; display: inline-block;">⚠️ Tratamiento caducado (Fin: ${t.fecha_fin})</div>`;
                } else if (t.fecha_fin === today) {
                    alertHtml = `<div style="margin-top:0.5rem; background: #fef3c7; color: #b45309; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem; display: inline-block;">🔔 Finaliza hoy</div>`;
                }
            }

            return `
            <div style="background: white; padding: 1.5rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border-left: 5px solid #ef4444; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                        <span style="font-weight: 700; font-size: 1.2rem; color: var(--text-primary);">${t.anilla || 'Ave desconocida'}</span>
                        <span style="background: #fecaca; color: #991b1b; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.8rem; font-weight: 600;">${t.tipo}</span>
                    </div>
                    <p style="margin: 0; color: var(--text-secondary);">
                        <strong>Tratamiento:</strong> ${t.nombre_receta || 'Personalizado'} • 
                        <strong>Inicio:</strong> ${t.fecha_inicio}
                        ${t.fecha_fin ? ` • <strong>Fin:</strong> ${t.fecha_fin}` : ''}
                    </p>
                    ${t.sintomas ? `<p style="margin: 0.5rem 0 0 0; color: var(--text-secondary); font-size: 0.9rem;">🤒 ${t.sintomas}</p>` : ''}
                    ${alertHtml}
                </div>
                <div>
                   <button class="btn-finish-treatment btn btn-sm" data-id="${t.id_tratamiento}" style="background: #10b981; color: white;">✅ Finalizar</button>
                   <button class="btn-edit-treatment btn btn-sm" data-id="${t.id_tratamiento}" style="background: white; border: 1px solid var(--border-color);">✏️</button>
                </div>
            </div>
        `}).join('');

        // Bind Finish buttons
        container.querySelectorAll('.btn-finish-treatment').forEach(btn => {
            btn.addEventListener('click', () => finishTreatment(btn.dataset.id));
        });
    };

    const renderHistory = (list) => {
        const container = div.querySelector('#treatments-history-table');
        if (list.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">Historial vacío.</p>';
            return;
        }

        const rows = list.map(t => `
            <tr style="border-bottom: 1px solid var(--border-color);">
                <td style="padding: 1rem;">${t.fecha_inicio}</td>
                <td style="padding: 1rem; font-weight: 600;">${t.anilla}</td>
                <td style="padding: 1rem;">${t.tipo}</td>
                <td style="padding: 1rem;">${t.nombre_receta || '-'}</td>
                <td style="padding: 1rem;">
                    <span style="padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.8rem; font-weight: 600; background: ${t.estado === 'Activo' ? '#fecaca' : '#d1fae5'}; color: ${t.estado === 'Activo' ? '#991b1b' : '#065f46'};">
                        ${t.estado}
                    </span>
                </td>
                <td style="padding: 1rem;">${t.resultado || '-'}</td>
            </tr>
        `).join('');

        container.innerHTML = `
            <table style="width: 100%; border-collapse: collapse; background: white; border-radius: var(--radius-lg); overflow: hidden;">
                <thead style="background: #f8fafc; color: var(--text-secondary); text-align: left;">
                    <tr>
                        <th style="padding: 1rem;">Fecha</th>
                        <th style="padding: 1rem;">Ave</th>
                        <th style="padding: 1rem;">Tipo</th>
                        <th style="padding: 1rem;">Receta</th>
                        <th style="padding: 1rem;">Estado</th>
                        <th style="padding: 1rem;">Resultado</th>
                    </tr>
                </thead>
                <tbody>${rows}</tbody>
            </table>
        `;
    };

    const renderRecipes = (list) => {
        const container = div.querySelector('#recipes-list');
        if (list.length === 0) {
            container.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--text-secondary);">No hay recetas definidas. Añade medicamentos comunes.</p>';
            return;
        }

        container.innerHTML = list.map(r => `
            <div style="background: white; padding: 1.5rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border: 1px solid var(--border-color); position: relative;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                    <h3 style="margin: 0; font-size: 1.1rem; color: var(--primary-color);">💊 ${r.nombre_receta}</h3>
                    <div style="display: flex; gap: 0.5rem;">
                        <button class="btn-edit-recipe" data-id="${r.id_receta}" style="border: none; background: none; cursor: pointer;">✏️</button>
                        <button class="btn-del-recipe" data-id="${r.id_receta}" style="border: none; background: none; color: #ef4444; cursor: pointer;">🗑️</button>
                    </div>
                </div>
                <p style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.5rem;"><strong>Dosis:</strong> ${r.dosis || 'N/A'}</p>
                <p style="font-size: 0.9rem; margin-bottom: 0.5rem;">${r.indicaciones || ''}</p>
                ${r.ingredientes ? `<div style="background: #f1f5f9; padding: 0.5rem; border-radius: 4px; font-size: 0.85rem; color: #475569;">${r.ingredientes}</div>` : ''}
            </div>
        `).join('');

        container.querySelectorAll('.btn-del-recipe').forEach(btn => {
            btn.addEventListener('click', async () => {
                if (confirm('¿Eliminar esta receta?')) {
                    await fetch(`/api/recipes/${btn.dataset.id}`, { method: 'DELETE' });
                    loadData();
                }
            });
        });

        container.querySelectorAll('.btn-edit-recipe').forEach(btn => {
            btn.addEventListener('click', () => {
                const recipe = list.find(r => r.id_receta == btn.dataset.id);
                openRecipeModal(recipe);
            });
        });
    };

    // Logic
    const finishTreatment = async (id) => {
        const result = prompt("¿Cuál fue el resultado del tratamiento? (Curado / Baja / Crónico)");
        if (!result) return;

        try {
            await db.update('treatments', id, {
                estado: 'Finalizado',
                resultado: result,
                fecha_fin: new Date().toISOString().split('T')[0]
            });
            loadData();
        } catch (e) {
            alert("Error al finalizar tratamiento: " + e.message);
        }
    };

    const openRecipeModal = (recipe = null) => {
        const isEdit = !!recipe;
        const modalHtml = `
            <div style="display: grid; gap: 1rem;">
                <div>
                    <label>Nombre Medicamento/Receta</label>
                    <input id="r-name" type="text" class="form-input" style="width: 100%;" placeholder="Ej: Vitamina AD3E" value="${isEdit ? recipe.nombre_receta : ''}">
                </div>
                <div>
                    <label>Dosis Recomendada</label>
                    <input id="r-dose" type="text" class="form-input" style="width: 100%;" placeholder="Ej: 5ml por litro de agua" value="${isEdit ? recipe.dosis : ''}">
                </div>
                <div>
                    <label>Indicaciones</label>
                    <textarea id="r-ind" class="form-input" style="width: 100%;">${isEdit ? recipe.indicaciones || '' : ''}</textarea>
                </div>
                    <div>
                    <label>Ingredientes activos</label>
                    <input id="r-ing" type="text" class="form-input" style="width: 100%;" value="${isEdit ? recipe.ingredientes || '' : ''}">
                </div>
            </div>
        `;

        showModal(isEdit ? 'Editar Receta' : 'Nueva Receta', modalHtml, async () => {
            const data = {
                nombre_receta: document.getElementById('r-name').value,
                dosis: document.getElementById('r-dose').value,
                indicaciones: document.getElementById('r-ind').value,
                ingredientes: document.getElementById('r-ing').value
            };
            if (!data.nombre_receta) return alert("Nombre obligatorio");

            const url = isEdit ? `/api/recipes/${recipe.id_receta}` : '/api/recipes';
            const method = isEdit ? 'PUT' : 'POST';

            await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            loadData();
        });
    };

    const setupModals = (birds, recipes) => {
        // Modal logic for "New Treatment"
        const btnNew = div.querySelector('#btn-new-treatment');
        btnNew.onclick = () => {
            const birdsOptions = birds.filter(b => b.estado === 'Activo').map(b => `<option value="${b.id_ave}">${b.anilla} (${b.especie})</option>`).join('');
            const recipesOptions = recipes.map(r => `<option value="${r.id_receta}">${r.nombre_receta}</option>`).join('');

            // Symptoms List
            const symptomsList = ['Diarrea', 'Embolado', 'Herida', 'Hongos', 'Ojos Hinchados', 'Parásitos', 'Picaje', 'Problemas Respiratorios', 'Pérdida de Peso'];
            const symptomsOptions = symptomsList.map(s => `<option value="${s}">${s}</option>`).join('');

            const modalHtml = `
                    <div style="display: grid; gap: 1rem;">
                        <div>
                            <label>Ave Afectada</label>
                            <select id="t-bird" class="form-input" style="width: 100%;">
                                <option value="">-- Seleccionar Ave --</option>
                                ${birdsOptions}
                            </select>
                        </div>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                             <div>
                                <label>Tipo</label>
                                <select id="t-type" class="form-input" style="width: 100%;">
                                    <option value="">-- Seleccionar --</option>
                                    <option>Curativo</option>
                                    <option>Preventivo</option>
                                    <option>Emergencia</option>
                                </select>
                            </div>
                            <div>
                                <label>Modo de Tratamiento</label>
                                <div style="display: flex; gap: 1rem; margin-top: 0.5rem;">
                                    <label style="font-weight: normal; font-size: 0.9rem;">
                                        <input type="radio" name="recipe-mode" value="saved" checked class="mode-radio"> Usar Receta
                                    </label>
                                    <label style="font-weight: normal; font-size: 0.9rem;">
                                        <input type="radio" name="recipe-mode" value="manual" class="mode-radio"> Manual
                                    </label>
                                </div>
                            </div>
                        </div>

                        <!-- Recipe Selection Block -->
                        <div id="block-saved-recipe">
                            <label>Seleccionar Receta</label>
                            <select id="t-recipe" class="form-input" style="width: 100%;">
                                <option value="">-- Seleccionar del Botiquín --</option>
                                ${recipesOptions}
                            </select>
                        </div>
                        
                        <!-- Manual Block (Hidden by default) -->
                        <div id="block-manual-recipe" style="display: none;">
                            <label>Detalles del Tratamiento Manual</label>
                            <input type="text" id="t-manual-detail" class="form-input" placeholder="Nombre medicina, etc." style="width: 100%;">
                        </div>

                        <!-- Symptoms Block -->
                        <div>
                            <label>Síntomas / Motivo</label>
                            <select id="t-symptoms-select" class="form-input" style="width: 100%;">
                                <option value="">-- Seleccionar Síntoma --</option>
                                ${symptomsOptions}
                                <option value="Otro">Otro...</option>
                            </select>
                            <input type="text" id="t-symptoms-other" class="form-input" style="width: 100%; margin-top: 0.5rem; display: none;" placeholder="Describa el síntoma...">
                        </div>

                        <!-- Posology / Dosage -->
                        <div>
                            <label>Posología / Dosis</label>
                            <input type="text" id="t-posology" class="form-input" placeholder="Ej: 1 gota cada 8 horas, 5ml/Litro..." style="width: 100%;">
                        </div>

                         <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                            <div>
                                <label>Fecha Inicio</label>
                                <input type="date" id="t-date" class="form-input" value="${new Date().toISOString().split('T')[0]}" style="width: 100%;">
                            </div>
                            <div>
                                <label>Duración (Días)</label>
                                <input type="number" id="t-duration" class="form-input" min="1" placeholder="Ej: 5" style="width: 100%;">
                                <p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 5px;">Se creará una alerta al finalizar.</p>
                            </div>
                        </div>
                    </div>
            `;

            showModal('Nuevo Tratamiento', modalHtml, async () => {
                const birdId = document.getElementById('t-bird').value;
                const type = document.getElementById('t-type').value;
                const startDateStr = document.getElementById('t-date').value;
                const duration = parseInt(document.getElementById('t-duration').value) || 0;
                const posology = document.getElementById('t-posology').value;

                // Recipe Logic
                const mode = document.querySelector('input[name="recipe-mode"]:checked').value;
                let recipeId = null;
                let manualDetails = "";

                if (mode === 'saved') {
                    recipeId = document.getElementById('t-recipe').value;
                } else {
                    manualDetails = document.getElementById('t-manual-detail').value;
                }

                // Symptom Logic
                const symptomSelect = document.getElementById('t-symptoms-select').value;
                const symptomOther = document.getElementById('t-symptoms-other').value;
                let finalSymptom = symptomSelect === 'Otro' ? symptomOther : symptomSelect;

                if (!birdId) return alert("Debes seleccionar un ave.");
                if (!type) return alert("Debes seleccionar el tipo de tratamiento.");
                if (!finalSymptom) return alert("Debes indicar un síntoma o motivo.");

                // Calculate end date
                let endDateStr = null;
                if (duration > 0 && startDateStr) {
                    const d = new Date(startDateStr);
                    d.setDate(d.getDate() + duration);
                    endDateStr = d.toISOString().split('T')[0];
                }

                // Append posology to remarks if present
                let finalObservations = manualDetails;
                if (posology) {
                    finalObservations += (finalObservations ? " | " : "") + "Dosis: " + posology;
                }

                const data = {
                    id_ave: birdId,
                    tipo: type,
                    id_receta: recipeId || null,
                    sintomas: finalSymptom,
                    observaciones: finalObservations,
                    fecha_inicio: startDateStr,
                    fecha_fin: endDateStr
                };

                await db.add('treatments', data);
                loadData();
            });

            // Delay to ensure DOM insertion
            setTimeout(() => {
                const radios = document.querySelectorAll('.mode-radio');
                radios.forEach(r => {
                    r.addEventListener('change', (e) => {
                        const val = e.target.value;
                        document.getElementById('block-saved-recipe').style.display = val === 'saved' ? 'block' : 'none';
                        document.getElementById('block-manual-recipe').style.display = val === 'manual' ? 'block' : 'none';
                    });
                });

                const sympSelect = document.getElementById('t-symptoms-select');
                if (sympSelect) {
                    sympSelect.addEventListener('change', (e) => {
                        document.getElementById('t-symptoms-other').style.display = e.target.value === 'Otro' ? 'block' : 'none';
                    });
                }
            }, 50);
        };

        // Modal logic for "New Recipe"
        const btnNewRecipe = div.querySelector('#btn-new-recipe');
        btnNewRecipe.onclick = () => {
            openRecipeModal();
        };
    };

    // Helper Modal Implementation (Inline for autonomy)
    const showModal = (title, content, onConfirm) => {
        const modalOverlay = document.createElement('div');
        modalOverlay.style.cssText = `
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.5); z-index: 1000;
            display: flex; align-items: center; justify-content: center;
        `;

        modalOverlay.innerHTML = `
            <div style="background: white; padding: 2rem; border-radius: var(--radius-lg); width: 100%; max-width: 500px; box-shadow: var(--shadow-xl);">
                <h2 style="margin-top: 0;">${title}</h2>
                <div style="margin: 1.5rem 0;">${content}</div>
                <div style="display: flex; justify-content: flex-end; gap: 1rem;">
                    <button class="btn-cancel btn" style="background: none; border: 1px solid var(--border-color);">Cancelar</button>
                    <button class="btn-confirm btn btn-primary">Guardar</button>
                </div>
            </div>
        `;

        document.body.appendChild(modalOverlay);

        modalOverlay.querySelector('.btn-cancel').onclick = () => modalOverlay.remove();
        modalOverlay.querySelector('.btn-confirm').onclick = async () => {
            try {
                await onConfirm();
                modalOverlay.remove();
            } catch (e) {
                alert("Error: " + e.message);
            }
        };
    };

    // Tab Switching
    div.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            div.querySelectorAll('.tab-btn').forEach(b => {
                b.style.color = 'var(--text-secondary)';
                b.style.borderBottom = 'none';
                b.classList.remove('active');
            });
            div.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');

            btn.style.color = 'var(--primary-color)';
            btn.style.borderBottom = '2px solid var(--primary-color)';
            btn.classList.add('active');

            div.querySelector(`#tab-content-${btn.dataset.tab}`).style.display = 'block';
        });
    });

    loadData();
    return div;
};
