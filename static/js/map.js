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