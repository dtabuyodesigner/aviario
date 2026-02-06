
export const InventoryView = () => {
    const div = document.createElement('div');
    div.innerHTML = `
        <div style="padding: 2rem; text-align: center;">
            <h1 style="color: var(--primary-color);">📦 Almacén y Suministros</h1>
            <p style="color: var(--text-secondary);">Módulo en construcción</p>
            <p>Control de stock de anillas, medicinas, semillas y pastas de cría.</p>
        </div>
    `;
    return div;
};
