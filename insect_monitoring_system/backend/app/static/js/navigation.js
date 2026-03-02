/*
 * Navigation handler for Smart Farming Dashboard
 * Handles consistent navigation across all pages
 */

document.addEventListener('DOMContentLoaded', function() {
    // Set up navigation for all pages
    setupNavigation();
    
    // Apply saved theme
    if (typeof themeManager !== 'undefined') {
        themeManager.applySavedTheme();
    }
    
    // Apply translations
    const savedLanguage = localStorage.getItem('language') || 'en';
    if (typeof translations !== 'undefined') {
        translations.applyTranslations(savedLanguage);
    }
});

// Set up navigation
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Get the page from data attribute
            const page = this.getAttribute('data-page');
            
            // Handle navigation
            if (page === 'profile') {
                window.location.href = '/profile';
            } else if (page === 'settings') {
                window.location.href = '/settings';
            } else if (page === 'dashboard') {
                window.location.href = '/';
            } else if (page === 'logout') {
                handleLogout();
            }
        });
    });
}

// Handle logout
async function handleLogout() {
    try {
        const response = await fetch('/api/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            window.location.href = '/login';
        }
    } catch (error) {
        console.error('Error logging out:', error);
        window.location.href = '/login';
    }
}

// Export for use in other scripts
window.navigation = {
    setupNavigation: setupNavigation
};