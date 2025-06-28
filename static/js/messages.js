function filterMessages(filter) {
    const rows = document.querySelectorAll('.contact-table tbody tr');
    rows.forEach(row => {
        if (filter === 'all') {
            row.style.display = '';
        } else if (row.classList.contains(filter)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}