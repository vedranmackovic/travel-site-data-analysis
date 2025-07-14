document.getElementById("searchName").addEventListener("input", function () {
    const filter = this.value.toLowerCase();
    const rows = document.querySelectorAll("#usersTable tbody tr");

    rows.forEach(row => {
        const destinationName = row.children[1].textContent.toLowerCase();
        if (destinationName.includes(filter)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
});
