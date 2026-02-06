export const CalendarView = async () => {
    const div = document.createElement('div');
    div.className = 'module-calendar';

    // Header & Controls
    div.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
            <div>
                <h1 style="color: var(--primary-color);">📅 Calendario de Cría</h1>
                <p style="color: var(--text-secondary);">Seguimiento de puestas, eclosiones y anillados.</p>
            </div>
            <div style="display: flex; gap: 0.5rem; align-items: center;">
                <button id="btn-prev-month" class="btn" style="background: white; border: 1px solid var(--border-color);">&lt;</button>
                <h2 id="current-month-label" style="margin: 0; min-width: 200px; text-align: center;"></h2>
                <button id="btn-next-month" class="btn" style="background: white; border: 1px solid var(--border-color);">&gt;</button>
                <button id="btn-today" class="btn btn-primary" style="margin-left: 1rem;">Hoy</button>
            </div>
        </div>

        <!-- Calendar Grid -->
        <div style="background: white; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); overflow: hidden;">
            <!-- Weekday Headers -->
            <div style="display: grid; grid-template-columns: repeat(7, 1fr); background: #f8fafc; border-bottom: 1px solid var(--border-color); text-align: center; font-weight: 600; padding: 1rem 0;">
                <div>Lun</div><div>Mar</div><div>Mié</div><div>Jue</div><div>Vie</div><div>Sáb</div><div>Dom</div>
            </div>
            <!-- Days Grid -->
            <div id="calendar-grid" style="display: grid; grid-template-columns: repeat(7, 1fr); min-height: 500px;">
                <!-- Days injected here -->
            </div>
        </div>

        <!-- Event Details Modal (Simple) -->
        <div id="events-legend" style="margin-top: 1.5rem; display: flex; gap: 1.5rem; justify-content: center; flex-wrap: wrap;">
            <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="width: 10px; height: 10px; background: #eab308; border-radius: 50%;"></span> Puesta</div>
            <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="width: 10px; height: 10px; background: #ef4444; border-radius: 50%;"></span> Incubación</div>
            <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="width: 10px; height: 10px; background: #22c55e; border-radius: 50%;"></span> Eclosión (Est.)</div>
            <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="width: 10px; height: 10px; background: #3b82f6; border-radius: 50%;"></span> Anillado (Est.)</div>
        </div>
    `;

    // State
    let currentDate = new Date();
    let events = [];
    let incubationParams = [];

    // Data Loading
    try {
        const [clutchesRes, paramsRes] = await Promise.all([
            fetch('/api/breeding'),
            fetch('/api/incubation-parameters')
        ]);

        const clutches = await clutchesRes.json();
        incubationParams = await paramsRes.json();

        // Process Events
        processEvents(clutches);

    } catch (e) {
        console.error("Error loading calendar data", e);
    }

    // Helper: Get Incubation Days for a species
    const getIncubationDays = (speciesName) => {
        if (!speciesName) return 13; // Default default
        const param = incubationParams.find(p => p.especie.toLowerCase().includes(speciesName.toLowerCase()) || speciesName.toLowerCase().includes(p.especie.toLowerCase()));

        if (param) {
            // Parses "13" or "13 - 15" -> returns average or first number
            const parts = param.dias_incubacion.split('-');
            return parseInt(parts[0].trim());
        }
        return 13; // Fallback
    };

    function processEvents(clutches) {
        events = [];
        clutches.forEach(clutch => {
            if (!clutch.fecha_inicio) return;
            // MANUAL PARSE to avoid UTC shift
            const [y, m, d] = clutch.fecha_inicio.split('-').map(Number);
            const startDate = new Date(y, m - 1, d);
            const species = clutch.pareja_id ? "Pareja " + clutch.pareja_id : "Nidada";

            // Use species from API or default
            const speciesName = clutch.especie || "Desconocida";
            const incDays = getIncubationDays(speciesName);

            // 1. Start (Puesta)
            events.push({
                date: new Date(startDate),
                type: 'puesta',
                title: `Puesta (Pareja ${clutch.pareja_id})`,
                color: '#eab308'
            });

            // 2. Hatching (Eclosión) - Estimated start of incubation + days
            // If incubation_start provided, use it, else assume clutch start + 4 days (approx for full clutch)
            let incubationStart;
            if (clutch.fecha_inicio_incubacion) {
                const [iy, im, id] = clutch.fecha_inicio_incubacion.split('-').map(Number);
                incubationStart = new Date(iy, im - 1, id);
            } else {
                incubationStart = new Date(startDate);
                incubationStart.setDate(incubationStart.getDate() + 4); // Heuristic
            }

            const hatchDate = new Date(incubationStart);
            hatchDate.setDate(hatchDate.getDate() + incDays);

            events.push({
                date: hatchDate,
                type: 'eclosion',
                title: `Eclosión est. (Pareja ${clutch.pareja_id})`,
                color: '#22c55e'
            });

            // 3. Banding (Anillado) - Hatch + 7 days
            const bandDate = new Date(hatchDate);
            bandDate.setDate(bandDate.getDate() + 7);
            events.push({
                date: bandDate,
                type: 'anillado',
                title: `Anillar est. (Pareja ${clutch.pareja_id})`,
                color: '#3b82f6'
            });
        });
        renderCalendar();
    }

    function renderCalendar() {
        const grid = div.querySelector('#calendar-grid');
        grid.innerHTML = '';

        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();

        // Update Label
        const monthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
        div.querySelector('#current-month-label').textContent = `${monthNames[month]} ${year}`;

        // Layout Logic
        const firstDayOfMonth = new Date(year, month, 1);
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        // Adjust for Monday start (0=Sun, 1=Mon...). JS getDay() is Sun=0.
        // We want Mon=0, Sun=6
        let startDay = firstDayOfMonth.getDay() - 1;
        if (startDay === -1) startDay = 6;

        // Empty cells for previous month
        for (let i = 0; i < startDay; i++) {
            const cell = document.createElement('div');
            cell.style.background = '#f9fafb';
            cell.style.border = '1px solid #f1f5f9';
            grid.appendChild(cell);
        }

        // Days
        for (let day = 1; day <= daysInMonth; day++) {
            const cell = document.createElement('div');
            cell.className = 'calendar-day';
            cell.style.border = '1px solid #f1f5f9';
            cell.style.minHeight = '100px';
            cell.style.padding = '0.5rem';
            cell.style.position = 'relative';

            // Check if Today
            const checkDate = new Date(year, month, day);
            const today = new Date();
            if (checkDate.toDateString() === today.toDateString()) {
                cell.style.background = '#eff6ff'; // Light blue highlight
            }

            cell.innerHTML = `<div style="font-weight: 600; margin-bottom: 0.5rem; font-size: 0.9rem; color: #64748b;">${day}</div>`;

            // Check Events for this Day
            const dayEvents = events.filter(e => e.date.toDateString() === checkDate.toDateString());

            if (dayEvents.length > 0) {
                const eventContainer = document.createElement('div');
                eventContainer.style.display = 'flex';
                eventContainer.style.flexDirection = 'column';
                eventContainer.style.gap = '2px';

                dayEvents.forEach(ev => {
                    const tag = document.createElement('div');
                    tag.style.fontSize = '0.75rem';
                    tag.style.padding = '2px 4px';
                    tag.style.borderRadius = '4px';
                    tag.style.background = ev.color;
                    tag.style.color = 'white';
                    tag.style.whiteSpace = 'nowrap';
                    tag.style.overflow = 'hidden';
                    tag.style.textOverflow = 'ellipsis';
                    tag.textContent = ev.title;
                    tag.title = ev.title; // Tooltip
                    eventContainer.appendChild(tag);
                });
                cell.appendChild(eventContainer);
            }

            grid.appendChild(cell);
        }
    }

    // Navigation Listeners
    div.querySelector('#btn-prev-month').onclick = () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar();
    };
    div.querySelector('#btn-next-month').onclick = () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar();
    };
    div.querySelector('#btn-today').onclick = () => {
        currentDate = new Date();
        renderCalendar();
    };

    renderCalendar();
    return div;
};
