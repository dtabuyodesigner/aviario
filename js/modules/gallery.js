
export const GalleryView = () => {
    const div = document.createElement('div');
    div.innerHTML = `
        <div style="padding: 2rem; text-align: center;">
            <h1 style="color: var(--primary-color);">📸 Galería Multimedia</h1>
            <p style="color: var(--text-secondary);">Módulo en construcción</p>
            <p>Repositorio centralizado de fotos y documentos de tus ejemplares.</p>
        </div>
    `;
    return div;
};
