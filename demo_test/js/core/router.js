/**
 * Simple Hash Router
 */

export class Router {
    constructor(routes, outlet) {
        this.routes = routes; // Map of 'path' -> render function
        this.outlet = outlet; // DOM Element to render into

        window.addEventListener('hashchange', this._onHashChange.bind(this));

        // Trigger initial route match immediately
        // The router is initialized after DOM is ready in app.js
        this._onHashChange();
    }

    async _onHashChange() {
        const hash = window.location.hash.slice(1) || '/dashboard'; // Default to dashboard

        // Find matching route or default
        const routeHandler = this.routes[hash] || this.routes['/404'];

        if (routeHandler) {
            this.outlet.innerHTML = ''; // Clear current view
            try {
                const view = await routeHandler();
                this.outlet.appendChild(view);
            } catch (error) {
                console.error("Route error:", error);
                this.outlet.innerHTML = `<div style="padding: 2rem; color: red;">
                    <h3>Error loading view</h3>
                    <p>${error.message}</p>
                </div>`;
            }
        } else {
            console.warn(`Route not found: ${hash}`);
            this.outlet.innerHTML = '<h2>Página no encontrada</h2>';
        }
    }

    navigate(path) {
        window.location.hash = path;
    }
}
