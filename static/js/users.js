document.getElementById("emailSearch").addEventListener("keyup", function () {
            const filter = this.value.toLowerCase();
            const rows = document.querySelectorAll("#usersTable tbody tr");

            rows.forEach(row => {
                const email = row.cells[1].textContent.toLowerCase();
                row.style.display = email.includes(filter) ? "" : "none";
            });
        });