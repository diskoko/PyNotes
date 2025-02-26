document.addEventListener('DOMContentLoaded', () => {
    // Navigation buttons functionality
    const navButtons = document.querySelectorAll('.nav-arrow');
    navButtons.forEach(button => {
        button.addEventListener('click', () => {
            alert('Navigation button clicked!'); // Replace with actual functionality.
        });
    });

    // Dark/Light mode toggle functionality
    const toggleButton = document.querySelector('#dark-mode-toggle');
    const body = document.body;

    // Check saved mode in localStorage
    const savedMode = localStorage.getItem('theme');
    if (savedMode) {
        body.classList.add(savedMode);
        toggleButton.checked = savedMode === 'dark-mode';
    }

    toggleButton.addEventListener('change', () => {
        if (toggleButton.checked) {
            body.classList.remove('light-mode');
            body.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark-mode');
        } else {
            body.classList.remove('dark-mode');
            body.classList.add('light-mode');
            localStorage.setItem('theme', 'light-mode');
        }
    });

    // Entry panel toggle functionality
    const entryPanels = document.querySelectorAll('.entry-panel');
    entryPanels.forEach(panel => {
        panel.addEventListener('click', () => {
            panel.classList.toggle('active');
        });
    });

    function renderCalendar() {
        const monthYear = document.getElementById('monthYear');
        const daysContainer = document.querySelector('.days');
        daysContainer.innerHTML = '';

        const month = selectedDate.getMonth();
        const year = selectedDate.getFullYear();
        monthYear.innerHTML = `${selectedDate.toLocaleString('default', { month: 'long' })}<br><span style="font-size:18px">${year}</span>`;

        const firstDay = new Date(year, month, 1).getDay();
        const lastDate = new Date(year, month + 1, 0).getDate();

        for (let i = 1; i <= lastDate; i++) {
            const day = document.createElement('li');
            day.innerText = i;
            if (i === currentDate.getDate() && month === currentDate.getMonth() && year === currentDate.getFullYear()) {
                day.classList.add('current-day');
            }
            if (entryDays.includes(i)) {
                day.classList.add('entry-day');
            }
            day.onclick = () => selectDate(i);
            daysContainer.appendChild(day);
        }
    }
});