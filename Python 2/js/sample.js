
const map = L.map("map").setView([54.5, 15.2],4);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 20
}).addTo(map);


