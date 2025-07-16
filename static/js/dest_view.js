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

document.querySelectorAll('.close').forEach(button => {
  button.addEventListener('click', () => {
    const modal = button.closest('.custom-modal, .dest-modal-container');
    if (modal) {
      modal.style.display = 'none';
    }
  });
});

function handleImageChange(input, imgId, labelId) {
  const file = input.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      document.getElementById(imgId).src = e.target.result;
    };
    reader.readAsDataURL(file);
    document.getElementById(labelId).textContent = file.name;
  }
}

document.querySelectorAll(".add-accommodation-btn").forEach(button => {
  button.addEventListener("click", () => {
    const destId = button.dataset.id;
    const tableBody = document.querySelector(`#accommodation-body-${destId}`);
    if (tableBody) {
      const newRow = document.createElement("tr");
      newRow.innerHTML = `
        <td><input type="text" name="new_accommodation_type_${destId}[]" class="form-control" placeholder="Type"></td>
        <td><input type="number" name="new_accommodation_cost_${destId}[]" class="form-control" placeholder="Cost"></td>
      `;
      tableBody.appendChild(newRow);
    }
  });
});

document.querySelectorAll(".add-transport-btn").forEach(button => {
  button.addEventListener("click", () => {
    const destId = button.dataset.id;
    const tableBody = document.querySelector(`#transport-body-${destId}`);
    if (tableBody) {
      const newRow = document.createElement("tr");
      newRow.innerHTML = `
        <td><input type="text" name="new_transport_type_${destId}[]" class="form-control" placeholder="Type"></td>
        <td><input type="number" name="new_transport_cost_${destId}[]" class="form-control" placeholder="Cost"></td>
      `;
      tableBody.appendChild(newRow);
    }
  });
});

document.addEventListener('click', function(event) {
  if (event.target.classList.contains('remove-row-btn')) {
    const row = event.target.closest('tr');
    if (row) {
      row.remove();
    }
  }
});