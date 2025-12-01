let airports = [
    { code: "BIKF", name: "Keflavik International Airport - Reykjavík", lat: 63.9850, lon: -22.6056 },
    { code: "EDDF", name: "Frankfurt am Main Airport - Frankfurt", lat: 50.0379, lon: 8.5622 },
    { code: "EDDL", name: "Düsseldorf Airport - Düsseldorf", lat: 51.2895, lon: 6.7668 },
    { code: "EDDN", name: "Nuremberg Airport - Nuremberg", lat: 49.4987, lon: 11.0669 },
    { code: "EGPF", name: "Glasgow International Airport - Paisley", lat: 55.8719, lon: -4.4331 },
    { code: "EHAM", name: "Amsterdam Schiphol Airport - Amsterdam", lat: 52.3105, lon: 4.7683 },
    { code: "EHEH", name: "Eindhoven Airport - Eindhoven", lat: 51.4501, lon: 5.3745 },
    { code: "EKBI", name: "Billund Airport - Billund", lat: 55.7403, lon: 9.1518 },
    { code: "ENBR", name: "Bergen Airport Flesland - Bergen", lat: 60.2934, lon: 5.2181 },
    { code: "ENTC", name: "Tromsø Airport - Tromsø", lat: 69.6833, lon: 18.9189 },
    { code: "GCFV", name: "Fuerteventura Airport - Fuerteventura", lat: 28.4527, lon: -13.8638 },
    { code: "GCTS", name: "Tenerife South Airport - Tenerife", lat: 28.0444, lon: -16.5725 },
    { code: "LBSF", name: "Sofia Airport - Sofia", lat: 42.6967, lon: 23.4114 },
    { code: "LBWN", name: "Varna Airport - Varna", lat: 43.2321, lon: 27.8251 },
    { code: "LDZA", name: "Zagreb Airport - Zagreb", lat: 45.7414, lon: 16.0675 },
    { code: "LEIB", name: "Ibiza Airport - Ibiza", lat: 38.8729, lon: 1.3731 },
    { code: "LEPA", name: "Palma de Mallorca Airport - Palma", lat: 39.5517, lon: 2.7388 },
    { code: "LFBD", name: "Bordeaux–Mérignac Airport - Bordeaux", lat: 44.8283, lon: -0.7156 },
    { code: "LFPG", name: "Charles de Gaulle Airport - Paris", lat: 49.0097, lon: 2.5479 },
    { code: "LFPO", name: "Paris-Orly Airport - Paris", lat: 48.7262, lon: 2.3652 },
    { code: "LGIR", name: "Heraklion International Airport - Heraklion", lat: 35.3397, lon: 25.1803 },
    { code: "LHBP", name: "Budapest Ferenc Liszt International Airport - Budapest", lat: 47.4399, lon: 19.2610 },
    { code: "LIRF", name: "Rome Fiumicino Airport - Rome", lat: 41.8003, lon: 12.2389 },
    { code: "LJLJ", name: "Ljubljana Jože Pučnik Airport - Ljubljana", lat: 46.2236, lon: 14.4576 },
    { code: "LPPR", name: "Porto Airport - Porto", lat: 41.2421, lon: -8.6781 },
    { code: "LSZH", name: "Zürich Airport - Zurich", lat: 47.4647, lon: 8.5492 },
    { code: "LYPG", name: "Podgorica Airport - Podgorica", lat: 42.3594, lon: 19.2519 },
    { code: "RU-4464", name: "Olenya Air Base - Olenegorsk", lat: 68.1500, lon: 33.3333 },
    { code: "UKLL", name: "Lviv International Airport - Lviv", lat: 49.8125, lon: 23.9561 },
    { code: "UNNT", name: "Novosibirsk Tolmachevo Airport - Novosibirsk", lat: 55.0126, lon: 82.6507 },
    { code: "URRP", name: "Platov International Airport - Rostov-on-Don", lat: 47.4939, lon: 39.9247 },
    { code: "UUEE", name: "Sheremetyevo International Airport - Moscow", lat: 55.9726, lon: 37.4146 },
    { code: "UWWW", name: "Kurumoch International Airport - Samara", lat: 53.5049, lon: 50.1643 }

];

let plane = null;
let chosenAirport = null;

function showAirportList() {
    const list = document.getElementById("airport-list");
    list.innerHTML = "";

    for (let i = 0; i < airports.length; i++) {
        const item = document.createElement("li");
        item.textContent = airports[i].code + " — " + airports[i].name;

        item.addEventListener("click", function () {
            chosenAirport = airports[i];
            highlightItem(item);
        });

        list.appendChild(item);
    }
}

showAirportList();

function highlightItem(item) {
    const items = document.querySelectorAll("#airport-list li");

    for (let i = 0; i < items.length; i++) {
        items[i].style.backgroundColor = "";
    }

    item.style.backgroundColor = "#cce0ff";
}

document.getElementById("go-button").addEventListener("click", function () {
    if (chosenAirport === null) {
        alert("Please pick an airport.");
        return;
    }

    movePlane(chosenAirport.lat, chosenAirport.lon);

    removeAirport(chosenAirport.code);

    chosenAirport = null;
});

// Move the plane to a new spot
function movePlane(lat, lon) {
    if (plane === null) {
        plane = L.marker([lat, lon], {
            icon: L.icon({
                iconUrl: "img/plane.png",
                iconSize: [40, 40]
            })
        }).addTo(map);
    } else {
        plane.setLatLng([lat, lon]);
    }

    map.setView([lat, lon], 6);
}

function removeAirport(code) {
    let newList = [];

    for (let i = 0; i < airports.length; i++) {
        if (airports[i].code !== code) {
            newList.push(airports[i]);
        }
    }

    airports = newList;
    showAirportList();

    let remaining = airports.length;
    let visited = 5 - remaining;

    document.getElementById("airport visited-count").textContent = visited;
}

