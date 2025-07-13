const serviceCostInput = document.getElementById("inputServiceCost");
const rawValue = serviceCostInput.value;
const numericValue = parseFloat(rawValue.replace(/[^0-9.]/g, '')) || 0; 

const accommodationSelect = document.getElementById("inputAccommodation");
function getAccommodationCost() {
    const rawValue = accommodationSelect.value; 
    const cost = parseFloat(rawValue.replace(/[^0-9.]/g, '')) || 0;
    return cost;
}
let currentAccommodationCost = getAccommodationCost();
accommodationSelect.addEventListener("change", () => {
    currentAccommodationCost = getAccommodationCost();
});

const transportSelect = document.getElementById("inputTransport");
function getTransportCost() {
    const rawValue = transportSelect.value;
    const cost = parseFloat(rawValue.replace(/[^0-9.]/g, '')) || 0;
    return cost;
}
let currentTransportCost = getTransportCost();
transportSelect.addEventListener("change", () => {
    currentTransportCost = getTransportCost();
});

function updateTotalCost() {
    const serviceCost = numericValue;
    const total = serviceCost + currentAccommodationCost + currentTransportCost;
    const totalCostInput = document.getElementById("inputServiceCost");
    totalCostInput.value = `$${total.toFixed()}`;
}
updateTotalCost();
accommodationSelect.addEventListener("change", updateTotalCost);
transportSelect.addEventListener("change", updateTotalCost);

//DATEPICKER
$('#inputCheckIn').datepicker({
    format: 'mm/dd/yyyy',
    autoclose: true,
    todayHighlight: true
});
$('#inputCheckOut').datepicker({
    format: 'mm/dd/yyyy',
    autoclose: true,
    todayHighlight: true
});

function calculateDays() {
    const checkInVal = $('#inputCheckIn').val();
    const checkOutVal = $('#inputCheckOut').val();

    if (checkInVal && checkOutVal) {
        const checkInDate = new Date(checkInVal);
        const checkOutDate = new Date(checkOutVal);

        const diffTime = checkOutDate - checkInDate;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        $('#inputDays').val(diffDays > 0 ? diffDays : 0);
    } else {
        $('#inputDays').val('');
    }
}

$('#inputCheckIn').datepicker().on('changeDate', calculateDays);
$('#inputCheckOut').datepicker().on('changeDate', calculateDays);