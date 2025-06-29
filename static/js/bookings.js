document.addEventListener("DOMContentLoaded", function () {
    const rawJson = document.getElementById("emailUserData").textContent;
    const emailToUserId = JSON.parse(rawJson);

    const searchInput = document.getElementById('searchName');
    const rows = document.querySelectorAll('#usersTable tbody tr');

    searchInput.addEventListener('input', function () {
        const searchValue = this.value.trim().toLowerCase();
        const matchingUserId = emailToUserId[searchValue];

        rows.forEach(row => {
            const travelerName = row.cells[5].textContent.toLowerCase();
            const travelerId = row.cells[13].textContent.trim();

            const nameMatch = travelerName.includes(searchValue);
            const emailMatch = matchingUserId !== undefined && travelerId === matchingUserId.toString();

            row.style.display = nameMatch || emailMatch ? '' : 'none';
        });
    });
});