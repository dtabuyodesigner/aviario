
import { db } from '../core/db.js';

export const GeneticsView = async () => {
    const container = document.createElement('div');
    container.className = 'module-genetics';

    container.innerHTML = `
        <div class="module-header" style="margin-bottom: 2rem;">
            <h1 style="font-size: 1.8rem; color: var(--primary-color);">Calculadora Genética</h1>
            <p style="color: var(--text-secondary);">Predicción de descendencia basada en genética de aves</p>
        </div>

        <div style="margin-bottom: 2rem;">
            <label style="font-weight: 500;">Especie:</label>
            <select id="gen-species" style="padding: 0.5rem; margin-left: 1rem; border: 1px solid var(--border-color); border-radius: var(--radius-sm); min-width: 200px;">
                <option value="">Seleccionar Especie...</option>
            </select>
        </div>

        <div class="calculator-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-bottom: 2rem;">
            <!-- Male Panel -->
            <div class="parent-panel" style="background: white; padding: 1.5rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border: 2px solid #e0e7ff;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; color: #1e40af;">
                    <h2 style="font-size: 1.25rem; margin: 0;">Macho (ZZ)</h2>
                    <span style="font-size: 1.5rem;">🐦</span>
                </div>
                
                <div style="display: flex; gap: 0.5rem; margin-bottom: 1rem;">
                    <select id="male-mut-select" class="mut-select" disabled style="flex: 1; padding: 0.5rem;">
                        <option value="">Añadir mutación...</option>
                    </select>
                    <button id="btn-add-male" disabled class="btn btn-sm" style="background: #1e40af; color: white;">+</button>
                </div>

                <div id="male-mut-list" class="mut-list" style="display: flex; flex-direction: column; gap: 0.5rem;">
                    <!-- Added mutations appear here -->
                </div>
            </div>

            <!-- Female Panel -->
            <div class="parent-panel" style="background: white; padding: 1.5rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); border: 2px solid #fce7f3;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; color: #be185d;">
                    <h2 style="font-size: 1.25rem; margin: 0;">Hembra (ZW)</h2>
                    <span style="font-size: 1.5rem;">🐦</span>
                </div>

                <div style="display: flex; gap: 0.5rem; margin-bottom: 1rem;">
                    <select id="female-mut-select" class="mut-select" disabled style="flex: 1; padding: 0.5rem;">
                        <option value="">Añadir mutación...</option>
                    </select>
                    <button id="btn-add-female" disabled class="btn btn-sm" style="background: #be185d; color: white;">+</button>
                </div>

                <div id="female-mut-list" class="mut-list" style="display: flex; flex-direction: column; gap: 0.5rem;">
                </div>
            </div>
        </div>

        <div style="text-align: center; margin-bottom: 2rem;">
            <button id="btn-calculate" class="btn btn-primary" disabled style="padding: 1rem 3rem; font-size: 1.1rem; box-shadow: var(--shadow-md);">
                🧬 Calcular Descendencia
            </button>
        </div>

        <!-- Results -->
        <div id="results-area" style="display: none; animation: fadeIn 0.5s ease;">
            <h3 style="margin-bottom: 1rem; border-bottom: 2px solid var(--border-color); padding-bottom: 0.5rem;">Resultados Probables</h3>
            <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; background: white; border-radius: var(--radius-md); overflow: hidden;">
                    <thead>
                        <tr style="background: #f8fafc; color: var(--text-secondary); text-align: left;">
                            <th style="padding: 1rem;">Sexo</th>
                            <th style="padding: 1rem;">Fenotipo (Visual)</th>
                            <th style="padding: 1rem;">Genotipo</th>
                            <th style="padding: 1rem; text-align: right;">Probabilidad</th>
                        </tr>
                    </thead>
                    <tbody id="results-body">
                    </tbody>
                </table>
            </div>
        </div>
    `;

    // State
    let selectedSpecies = null;
    let availableMutations = [];
    let maleSelection = [];
    let femaleSelection = [];

    // DOM Elements
    const speciesSelect = container.querySelector('#gen-species');
    const maleSelect = container.querySelector('#male-mut-select');
    const femaleSelect = container.querySelector('#female-mut-select');
    const btnAddMale = container.querySelector('#btn-add-male');
    const btnAddFemale = container.querySelector('#btn-add-female');
    const maleList = container.querySelector('#male-mut-list');
    const femaleList = container.querySelector('#female-mut-list');
    const btnCalculate = container.querySelector('#btn-calculate');
    const resultsArea = container.querySelector('#results-area');
    const resultsBody = container.querySelector('#results-body');

    // Init Logic
    const init = async () => {
        try {
            const res = await fetch('/api/genetics/species');
            const speciesList = await res.json();

            speciesList.forEach(sp => {
                const opt = document.createElement('option');
                opt.value = sp;
                opt.textContent = sp;
                speciesSelect.appendChild(opt);
            });
        } catch (e) {
            console.error("Error loading species", e);
        }
    };

    // Load Mutations for Species
    speciesSelect.addEventListener('change', async () => {
        selectedSpecies = speciesSelect.value;
        maleSelection = [];
        femaleSelection = [];
        updateLists();
        resultsArea.style.display = 'none';

        if (!selectedSpecies) {
            maleSelect.disabled = true;
            femaleSelect.disabled = true;
            btnAddMale.disabled = true;
            btnAddFemale.disabled = true;
            btnCalculate.disabled = true;
            return;
        }

        // Fetch Mutations
        try {
            availableMutations = await db.getMutations(selectedSpecies);
            populateMutationSelects();

            maleSelect.disabled = false;
            femaleSelect.disabled = false;
            btnAddMale.disabled = false;
            btnAddFemale.disabled = false;
            btnCalculate.disabled = false;
        } catch (e) {
            console.error(e);
        }
    });

    const populateMutationSelects = () => {
        const populate = (select, sex) => {
            select.innerHTML = '<option value="">Añadir mutación...</option>';
            // Group by inheritance?

            availableMutations.forEach(mut => {
                // Determine valid factors
                // Visual
                const optV = document.createElement('option');
                optV.value = JSON.stringify({ ...mut, factor: 'Visual' }); // Logic abstraction

                let label = mut.nombre;
                if (mut.tipo_herencia === 'Dominante') label += ' (SF)';
                optV.textContent = label;
                select.appendChild(optV);

                // If Dominant -> Allow DF
                if (mut.tipo_herencia === 'Dominante' || mut.tipo_herencia === 'Dominante Incompleta') {
                    const optDF = document.createElement('option');
                    optDF.value = JSON.stringify({ ...mut, factor: 'DF' });
                    optDF.textContent = `${mut.nombre} (DF)`;
                    select.appendChild(optDF);
                }

                // If Recessive or Sex-Linked (Male only) -> Allow Split (Portador)
                const canBeSplit = (mut.tipo_herencia === 'Recesiva Autosómica') ||
                    (mut.tipo_herencia === 'Ligada al Sexo' && sex === 'M');

                if (canBeSplit) {
                    const optS = document.createElement('option');
                    optS.value = JSON.stringify({ ...mut, factor: 'Portador' });
                    optS.textContent = `Portador de ${mut.nombre}`;
                    select.appendChild(optS);
                }
            });
        };

        populate(maleSelect, 'M');
        populate(femaleSelect, 'F');
    };

    // UX: Auto-add on select change
    maleSelect.addEventListener('change', () => {
        if (maleSelect.value) addMutation('M');
    });

    femaleSelect.addEventListener('change', () => {
        if (femaleSelect.value) addMutation('F');
    });

    // Add Mutation Handlers
    const addMutation = (sex) => {
        const select = sex === 'M' ? maleSelect : femaleSelect;
        const list = sex === 'M' ? maleSelection : femaleSelection;

        if (!select.value) return;

        const mut = JSON.parse(select.value);
        list.push(mut);
        updateLists();
        updateCalculateState(); // Trigger state check
        select.value = "";
    };

    btnAddMale.addEventListener('click', () => addMutation('M'));
    btnAddFemale.addEventListener('click', () => addMutation('F'));

    const updateCalculateState = () => {
        const hasSelection = maleSelection.length > 0 || femaleSelection.length > 0;
        // btnCalculate.disabled = !hasSelection; // Maybe too strict? 
        // Ancestral x Ancestral is a valid calculation...
        // But to avoid confusion of "I selected but didn't add", maybe better to allow empty?
        // User request says "Disable if no mutations". 
        // Actually, Ancestral x Ancestral is valid.
        // But the Problem "User selects in dropdown but forgets plus" is solved by Auto-Add.

        // Let's keep Calculate enabled always, but now Auto-Add solves the main issue.
        // If I disable it, how do they calculate Ancestral x Ancestral?
        // Maybe better to NOT disable, but trust Auto-Add.
        // OR: Only disable if species is not selected.
    };

    const updateLists = () => {
        const render = (arr, containerEl, sex) => {
            containerEl.innerHTML = '';
            arr.forEach((m, idx) => {
                const item = document.createElement('div');
                item.className = 'mut-item';
                item.style.cssText = `
                    display: flex; justify-content: space-between; align-items: center;
                    padding: 0.5rem; background: #f8fafc; border-radius: 4px; border: 1px solid var(--border-color);
                `;

                let text = m.nombre;
                if (m.factor === 'DF') text += ' (DF)';
                if (m.factor === 'Portador') text = `Portador de ${text}`;
                if (m.factor === 'Visual' && m.tipo_herencia === 'Dominante') text += ' (SF)';

                item.innerHTML = `
                    <span style="font-size: 0.9rem;">${text}</span>
                    <button style="border: none; background: none; color: #ef4444; cursor: pointer; font-size: 1.1rem;">&times;</button>
                `;

                item.querySelector('button').onclick = () => {
                    arr.splice(idx, 1);
                    updateLists();
                    updateCalculateState();
                };
                containerEl.appendChild(item);
            });
        };

        render(maleSelection, maleList, 'M');
        render(femaleSelection, femaleList, 'F');
    };

    // CALCULATE
    btnCalculate.addEventListener('click', async () => {
        // Warning if empty?
        if (maleSelection.length === 0 && femaleSelection.length === 0) {
            // Optional: alert/toast?
            // "Calculando cruce Ancestral x Ancestral..."
        }

        resultsArea.style.display = 'none';
        btnCalculate.textContent = "Calculando...";
        btnCalculate.disabled = true;

        try {
            const response = await fetch('/api/genetics/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    male: maleSelection,
                    female: femaleSelection,
                    species: selectedSpecies
                })
            });

            if (!response.ok) throw new Error('Error en el cálculo');

            const results = await response.json();
            renderResults(results);
        } catch (e) {
            alert("Error: " + e.message);
        } finally {
            btnCalculate.textContent = "🧬 Calcular Descendencia";
            btnCalculate.disabled = false;
        }
    });

    const renderResults = (data) => {
        resultsBody.innerHTML = '';
        if (data.length === 0) {
            resultsBody.innerHTML = '<tr><td colspan="4" style="padding: 1rem; text-align: center;">Sin resultados probables.</td></tr>';
            return;
        }

        data.forEach(row => {
            const tr = document.createElement('tr');
            tr.style.cssText = "border-bottom: 1px solid #f1f5f9; hover: background: #f8fafc;";

            // Sex Icon
            let sexHtml = '';
            if (row.sex === 'M') sexHtml = '<span style="color: #1e40af; font-weight: bold;">♂ Macho</span>';
            else if (row.sex === 'H') sexHtml = '<span style="color: #be185d; font-weight: bold;">♀ Hembra</span>';
            else sexHtml = '<span style="color: #64748b;">A. Sexos</span>';

            // Clean Genotype display
            // Replace 'Portador de' with ' / ' notation if preferred, or keep explicit text.
            // Let's highlight 'Portador' in italics.
            let genoHtml = row.genotype.replace(/Portador de /g, '<i>/ </i>');

            tr.innerHTML = `
                <td style="padding: 1rem;">${sexHtml}</td>
                <td style="padding: 1rem; font-weight: 500;">${row.phenotype}</td>
                <td style="padding: 1rem; color: var(--text-secondary); font-size: 0.9rem;">${genoHtml}</td>
                <td style="padding: 1rem; text-align: right; font-weight: bold;">${(row.probability || 0).toFixed(1)}%</td>
            `;
            resultsBody.appendChild(tr);
        });

        resultsArea.style.display = 'block';
        resultsArea.scrollIntoView({ behavior: 'smooth' });
    };

    // Helper: Animations
    const style = document.createElement('style');
    style.innerHTML = `
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .mut-item:hover { background: #e2e8f0 !important; }
    `;
    container.appendChild(style);

    init();
    return container;
};
