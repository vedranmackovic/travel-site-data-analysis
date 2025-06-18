//TREND
document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);
    const tab = params.get("tab");

    const tabMap = {
      "north-america": "#1a",
      "south-america": "#2a",
      "europe": "#3a",
      "asia": "#4a",
      "africa": "#5a",
      "australia": "#6a",
      "antartica": "#7a"
    };

    if (tab && tabMap[tab]) {
      const targetTabLink = document.querySelector(`a[href="${tabMap[tab]}"]`);
      if (targetTabLink) {
        $(targetTabLink).tab('show');
      }
    }
  });

//MAP
let map;
let center;

function initialize() {
    const mapOptions = {
        zoom: 16,
        center: new google.maps.LatLng(37.769725, -122.462154),
        scrollwheel: false,
    };

    map = new google.maps.Map(document.getElementById('google-map'), mapOptions);

    const marker = new google.maps.Marker({
    position: mapOptions.center,
    map: map,});

    google.maps.event.addListenerOnce(map, 'idle', function () {
        center = map.getCenter();
    });

    google.maps.event.addDomListener(window, 'resize', function () {
        if (map && center) map.setCenter(center);
    });
}

function loadGoogleMap() {
    const script = document.createElement('script');
    script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyDVWt4rJfibfsEDvcuaChUaZRS5NXey1Cs&v=3.exp&sensor=false&' + 'callback=initialize';
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);
}

document.addEventListener('DOMContentLoaded', function () {
    loadGoogleMap();
});

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

// Attach the handler to datepicker selection
$('#inputCheckIn').datepicker().on('changeDate', calculateDays);
$('#inputCheckOut').datepicker().on('changeDate', calculateDays);