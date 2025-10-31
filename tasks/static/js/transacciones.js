// Ensure DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get tab elements
    const tabTodas = document.getElementById('tab-todas');
    const tabIngresos = document.getElementById('tab-ingresos');
    const tabEgresos = document.getElementById('tab-egresos');

    // Get content panes
    const todasPane = document.getElementById('todas');
    const ingresosPane = document.getElementById('ingresos');
    const egresosPane = document.getElementById('egresos');

    // Function to handle tab switching
    function switchTab(activeTab, activePane) {
        // Remove active class from all tabs and panes
        [tabTodas, tabIngresos, tabEgresos].forEach(tab => {
            tab.classList.remove('active');
            tab.setAttribute('aria-selected', 'false');
        });
        [todasPane, ingresosPane, egresosPane].forEach(pane => {
            pane.classList.remove('show', 'active');
        });

        // Add active class to selected tab and pane
        activeTab.classList.add('active');
        activeTab.setAttribute('aria-selected', 'true');
        activePane.classList.add('show', 'active');
    }

    // Add click event listeners
    tabTodas.addEventListener('click', function(e) {
        e.preventDefault();
        switchTab(tabTodas, todasPane);
    });

    tabIngresos.addEventListener('click', function(e) {
        e.preventDefault();
        switchTab(tabIngresos, ingresosPane);
    });

    tabEgresos.addEventListener('click', function(e) {
        e.preventDefault();
        switchTab(tabEgresos, egresosPane);
    });
});