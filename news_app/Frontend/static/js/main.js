// NewsHub - Main JavaScript File

// Debug logging
console.log('Main.js loaded at:', new Date().toISOString());

// Theme Management
const ThemeManager = (function() {
    const THEME_KEY = 'news-management-system-theme';
    const DARK_CLASS = 'dark';

    function getSystemPreference() {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        return 'light';
    }

    function getSavedTheme() {
        const saved = localStorage.getItem(THEME_KEY);
        return saved || getSystemPreference();
    }

    function setTheme(theme) {
        const html = document.documentElement;
        if (theme === 'dark') {
            html.classList.add(DARK_CLASS);
        } else {
            html.classList.remove(DARK_CLASS);
        }
        localStorage.setItem(THEME_KEY, theme);
        updateThemeIcon(theme);
    }

    function toggleTheme() {
        const currentTheme = getSavedTheme();
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
        return newTheme;
    }

    function getCurrentTheme() {
        return document.documentElement.classList.contains(DARK_CLASS) ? 'dark' : 'light';
    }

    function updateThemeIcon(theme) {
        const themeIcons = document.querySelectorAll('.theme-icon');
        themeIcons.forEach(icon => {
            if (theme === 'dark') {
                icon.innerHTML = '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 100 2h1z" fill-rule="evenodd" clip-rule="evenodd"></path></svg>';
            } else {
                icon.innerHTML = '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path></svg>';
            }
        });
    }

    function init() {
        const theme = getSavedTheme();
        setTheme(theme);

        // Listen for system theme changes
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
                if (!localStorage.getItem(THEME_KEY)) {
                    setTheme(e.matches ? 'dark' : 'light');
                }
            });
        }
    }

    return {
        init: init,
        toggle: toggleTheme,
        set: setTheme,
        get: getCurrentTheme
    };
})();

// Global functions - Define these first
window.toggleSidebar = function() {
    console.log('toggleSidebar called');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    
    console.log('Sidebar element:', sidebar);
    console.log('Overlay element:', sidebarOverlay);
    
    if (sidebar && sidebarOverlay) {
        sidebar.classList.toggle('sidebar-open');
        sidebarOverlay.classList.toggle('overlay-visible');
        console.log('Sidebar toggled');
    } else {
        console.error('Sidebar or overlay element not found');
    }
};

window.toggleTheme = function() {
    console.log('toggleTheme called');
    const newTheme = ThemeManager.toggle();
    console.log('Theme switched to:', newTheme);
    if (window.showNotification) {
        showNotification(`Switched to ${newTheme} mode`, 'info');
    }
};

// Main initialization
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded');
    
    // Initialize theme first
    ThemeManager.init();

    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    console.log('Mobile menu button:', mobileMenuBtn);
    console.log('Sidebar:', sidebar);
    console.log('Sidebar overlay:', sidebarOverlay);

    // Mobile menu button click handler
    if (mobileMenuBtn) {
        console.log('Adding click listener to mobile menu button');
        mobileMenuBtn.addEventListener('click', function(e) {
            console.log('Mobile menu button clicked!');
            e.preventDefault();
            e.stopPropagation();
            window.toggleSidebar();
        });
    } else {
        console.error('Mobile menu button not found');
    }

    // Close sidebar when overlay is clicked
    if (sidebarOverlay) {
        console.log('Adding click listener to sidebar overlay');
        sidebarOverlay.addEventListener('click', function(e) {
            console.log('Sidebar overlay clicked!');
            e.preventDefault();
            e.stopPropagation();
            window.toggleSidebar();
        });
    }

    // Theme toggle buttons
    const mobileThemeToggle = document.getElementById('mobileThemeToggle');
    const sidebarThemeToggle = document.getElementById('sidebarThemeToggle');
    
    if (mobileThemeToggle) {
        console.log('Adding click listener to mobile theme toggle');
        mobileThemeToggle.addEventListener('click', function(e) {
            console.log('Mobile theme toggle clicked!');
            e.preventDefault();
            e.stopPropagation();
            window.toggleTheme();
        });
    }
    
    if (sidebarThemeToggle) {
        console.log('Adding click listener to sidebar theme toggle');
        sidebarThemeToggle.addEventListener('click', function(e) {
            console.log('Sidebar theme toggle clicked!');
            e.preventDefault();
            e.stopPropagation();
            window.toggleTheme();
        });
    }

    // Close sidebar when a link is clicked (mobile)
    if (sidebar) {
        const sidebarLinks = sidebar.querySelectorAll('a');
        sidebarLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth < 1024) {
                    sidebar.classList.remove('sidebar-open');
                    sidebarOverlay?.classList.remove('overlay-visible');
                }
            });
        });
    }
    
    console.log('All event listeners attached');
});

// Utility Functions

/**
 * Show notification toast
 */
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    const colors = {
        success: 'bg-green-600',
        error: 'bg-red-600',
        warning: 'bg-yellow-600',
        info: 'bg-blue-600'
    };

    notification.className = `fixed bottom-4 right-4 px-6 py-3 rounded-lg font-semibold text-white z-50 ${colors[type] || colors.info}`;
    notification.textContent = message;
    notification.style.animation = 'slideInUp 0.3s ease-out';
    
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateY(20px)';
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

/**
 * Format date to readable string
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

/**
 * Truncate text to specified length
 */
function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
}

/**
 * Count words in text
 */
function countWords(text) {
    return text.trim().split(/\s+/).filter(w => w.length > 0).length;
}

/**
 * Count characters in text
 */
function countCharacters(text) {
    return text.length;
}

/**
 * Debounce function for performance
 */
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}

/**
 * API Helper - GET request
 */
async function apiGet(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('API GET error:', error);
        throw error;
    }
}

/**
 * API Helper - POST request
 */
async function apiPost(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('API POST error:', error);
        throw error;
    }
}

/**
 * API Helper - PUT request
 */
async function apiPut(url, data) {
    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('API PUT error:', error);
        throw error;
    }
}

/**
 * API Helper - DELETE request
 */
async function apiDelete(url) {
    try {
        const response = await fetch(url, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.status === 204 ? null : await response.json();
    } catch (error) {
        console.error('API DELETE error:', error);
        throw error;
    }
}

// Export functions for global use
window.showNotification = showNotification;
window.formatDate = formatDate;
window.truncateText = truncateText;
window.countWords = countWords;
window.countCharacters = countCharacters;
window.apiGet = apiGet;
window.apiPost = apiPost;
window.apiPut = apiPut;
window.apiDelete = apiDelete;
