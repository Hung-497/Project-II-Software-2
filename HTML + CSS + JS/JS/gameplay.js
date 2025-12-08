const map = L.map("map").setView([54.5, 15.2], 4);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 20,
}).addTo(map);

const planeIcon = L.icon({         //plane icon
    iconUrl: "../IMG/airplane2.png",
    iconSize: [80, 80],
    iconAnchor: [16, 16],
    popupAnchor: [0, -16],
});

'use strict';
let selectedAirportButton = null;
let selectedAirport = null;
let airportMarkers = {};
let airportButtons = {};
let currentAirportCode = null;
let currentPlaneMarker = null;

const airportlistContainer = document.getElementById("airport-list");
function renderAirportList(airports) {             //render airport list and markers for map
    airportlistContainer.innerHTML = "";
    selectedAirportButton = null;
    selectedAirport = null;
    for (const code in airportMarkers) {           //remove existing markers
        map.removeLayer(airportMarkers[code]);
    }
    airportMarkers = {};
    airportButtons = {};

    airports.forEach((airport) => {
        const btn = document.createElement("button");
        const name = airport["code"] + " - " + airport["name"];
        btn.textContent = name;
        airportlistContainer.appendChild(btn);
        btn.addEventListener("click", () => {           //select airport from list
            if (selectedAirportButton !== null) {
                selectedAirportButton.classList.remove("selected");      //access selected airport button
            }
            btn.classList.add("selected");
            btn.dataset.code = airport["code"];       //store airport code in data attribute of button
            selectedAirport = btn.dataset.code;
            selectedAirportButton = btn;
        });
        const marker = L.marker([airport["lat"], airport["lon"]]).addTo(map);           //add marker to map
        marker.bindPopup(name);
        airportMarkers[airport["code"]] = marker;
        airportButtons[airport["code"]] = btn;
        marker.on("click", () => { SelectedAirport(airport["code"]); })            //select airport from map marker to see information
        marker.on("dblclick", () => { goAirport(airport["code"]) });        //double click to go to airport
    });
}

function SelectedAirport(code) {
    const btn = airportButtons[code];
    if (selectedAirportButton !== null) {
        selectedAirportButton.classList.remove("selected");
    }
    btn.classList.add("selected");
    selectedAirport = code;
    selectedAirportButton = btn;
}

function renderDaysLeft(daysLeft) {                       //render days left
    const daysLeftElement = document.getElementById("airport visited-count");
    daysLeftElement.textContent = `Days Left: ${daysLeft}/21`;
}

function renderCodefound(code) {                          //render code found
    const codeFound = document.getElementById("codes encrypted-count");
    codeFound.textContent = `Code Found: ${code}/5`;
}

function renderMessages(messages) {            //render messages
    const messagesElement = document.querySelector(".messages");
    const msg = [...messages].reverse().join("\n");                //reverse the order of messages + [...messages] split messages parts into each line and group again with a new array
    messagesElement.innerHTML = msg.replace(/\n/g, "<br>");        //change new line to <br>
}

function updateCurrentPlaneMarker(lat, lon, code, name) {
    if (currentPlaneMarker) {
        map.removeLayer(currentPlaneMarker);
    }
    currentPlaneMarker = L.marker([lat, lon], { icon: planeIcon }).addTo(map);
    currentPlaneMarker.bindPopup(code + " - " + name).openPopup();
    map.setView([lat, lon], 6);
    currentAirportCode = code;
}

async function fetchAirport() {
    try {
        const response = await fetch("http://127.0.0.1:5000/state");
        const data = await response.json();
        const cur = data.current_airport_info;
        updateCurrentPlaneMarker(cur.lat, cur.lon, cur.code, cur.name);
        renderAirportList(data.remaining_airports);
        renderDaysLeft(data.days_left);
        renderCodefound(data.code_found)
        renderMessages(data.messages);
    } catch (error) {
        console.error("Error fetching airport data:", error);
    }
}

async function goAirport(selectedAirport) {
    const target = selectedAirport;
    if (!target) {
        alert("Please pick an airport.");
        return;
    }
    try {
        const response = await fetch(`http://127.0.0.1:5000/move/${selectedAirport}`);
        const data = await response.json();
        const cur = data.current_airport_info;
        updateCurrentPlaneMarker(cur.lat, cur.lon, cur.code, cur.name);
        renderAirportList(data.remaining_airports);
        renderDaysLeft(data.days_left);
        renderCodefound(data.code_found);
        renderMessages(data.messages);
        if (data.outcome === "lose" && data.game_over === true) {
            document.location.href = "badend.html"
        }
        if (data.outcome === "win" && data.game_over === true) {
            document.location.href = "goodend.html"
        }
    } catch (error) {
        console.error("Error moving to airport:", error);
    }
}

window.addEventListener("DOMContentLoaded", () => {
    fetchAirport();

    const goButton = document.getElementById("go-button");
    goButton.addEventListener("click", async () => {
        await goAirport(selectedAirport);
    });
});

// This JS is to show the name on player name text box //
window.addEventListener("load", function () {
    const playerName = localStorage.getItem("playerName");

    if (playerName) {
        document.getElementById("player-name").value = playerName;
    }
});