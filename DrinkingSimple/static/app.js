/**
 * Journal Application JavaScript
 * Handles UI interactivity including calendar navigation,
 * dark/light mode toggling, and entry panel interactions.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize navigation buttons
    setupNavigationButtons();
    
    // Setup dark/light mode toggle
    setupDarkModeToggle();
    
    // Setup entry panel interactions
    setupEntryPanels();
    
    // Initialize the calendar (if present)
    if (document.querySelector('.calendar')) {
        renderCalendar();
    }
});

/**
 * Sets up the navigation buttons (prev/next)
 */
function setupNavigationButtons() {
    const navButtons = document.querySelectorAll('.nav-arrow');
    navButtons.forEach(button => {
        button.addEventListener('click', () => {
            // TODO: Replace this with actual date navigation
            alert('Navigation button clicked! This will navigate to the previous/next day.');
        });
    });
}

/**
 * Sets up the dark/light mode toggle functionality
 * Preserves user preference in localStorage
 */
function setupDarkModeToggle() {
    const darkModeToggle = document.querySelector('#dark-mode-toggle');
    const bodyElement = document.body;

    // Load saved preference from localStorage
    const savedThemePreference = localStorage.getItem('theme');
    if (savedThemePreference) {
        bodyElement.classList.add(savedThemePreference);
        darkModeToggle.checked = savedThemePreference === 'dark-mode';
    }

    // Toggle between dark and light mode
    darkModeToggle.addEventListener('change', () => {
        if (darkModeToggle.checked) {
            // Enable dark mode
            bodyElement.classList.remove('light-mode');
            bodyElement.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark-mode');
        } else {
            // Enable light mode
            bodyElement.classList.remove('dark-mode');
            bodyElement.classList.add('light-mode');
            localStorage.setItem('theme', 'light-mode');
        }
    });
}

/**
 * Sets up expandable/collapsible entry panels
 */
function setupEntryPanels() {
    const entryPanels = document.querySelectorAll('.entry-panel');
    entryPanels.forEach(panel => {
        panel.addEventListener('click', () => {
            panel.classList.toggle('active');
        });
    });
}

/**
 * Renders the calendar with the current month
 * Highlights today and days with journal entries
 */
function renderCalendar() {
    const monthYearDisplay = document.getElementById('monthYear');
    const daysContainer = document.querySelector('.days');
    
    // Clear previous days
    daysContainer.innerHTML = '';

    // Update month and year display
    const currentMonth = selectedDate.getMonth();
    const currentYear = selectedDate.getFullYear();
    monthYearDisplay.innerHTML = `${selectedDate.toLocaleString('default', { month: 'long' })}<br><span style="font-size:18px">${currentYear}</span>`;

    // Get first day of month and last date
    const firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay();
    const lastDateOfMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

    // Generate calendar days
    for (let dayNum = 1; dayNum <= lastDateOfMonth; dayNum++) {
        const dayElement = document.createElement('li');
        dayElement.innerText = dayNum;
        
        // Highlight current day
        if (dayNum === currentDate.getDate() && 
            currentMonth === currentDate.getMonth() && 
            currentYear === currentDate.getFullYear()) {
            dayElement.classList.add('current-day');
        }
        
        // Highlight days with entries
        if (entryDays.includes(dayNum)) {
            dayElement.classList.add('entry-day');
        }
        
        // Make days clickable
        dayElement.onclick = () => selectDate(dayNum);
        daysContainer.appendChild(dayElement);
    }
}

function showNotification(title, message) {
    // Create container if it doesn't exist
    let container = document.querySelector('.notification-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'notification-container';
        document.body.appendChild(container);
    }

    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.innerHTML = `
        <div class="notification-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="2"/>
                <path d="M8 12L11 15L16 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div class="notification-content">
            <div class="notification-title">${title}</div>
            <div class="notification-message">${message}</div>
        </div>
    `;

    // Add to container
    container.appendChild(notification);

    // Trigger animation
    setTimeout(() => notification.classList.add('show'), 100);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}