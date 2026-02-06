
export const FinanceView = () => {
    const div = document.createElement('div');
    div.innerHTML = `
        <div style="padding: 2rem; text-align: center;">
            <h1 style="color: var(--primary-color);">💰 Economía</h1>
            <p style="color: var(--text-secondary);">Módulo en construcción</p>
            <p>Registro de gastos, ventas, cesiones y balance económico global.</p>
        </div>
    `;
    return div;
};
