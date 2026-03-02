/*
 * Theme Manager for Smart Farming Dashboard
 * Handles theme persistence across all pages
 */

document.addEventListener('DOMContentLoaded', function() {
    // Apply saved theme on page load
    applySavedTheme();
    
    // Add event listener for theme changes in settings
    const themeSelector = document.getElementById('theme');
    if (themeSelector) {
        themeSelector.addEventListener('change', function() {
            const selectedTheme = this.value;
            applyTheme(selectedTheme);
            saveThemePreference(selectedTheme);
        });
    }
});

// Apply the saved theme from localStorage
function applySavedTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        applyTheme(savedTheme);
    }
}

// Apply a specific theme to the page
function applyTheme(theme) {
    if (theme === 'dark') {
        document.body.classList.add('dark-theme');
    } else {
        document.body.classList.remove('dark-theme');
    }
}

// Save theme preference to localStorage
function saveThemePreference(theme) {
    localStorage.setItem('theme', theme);
}

// Export functions for use in other scripts
window.themeManager = {
    applySavedTheme: applySavedTheme,
    applyTheme: applyTheme,
    saveThemePreference: saveThemePreference
};