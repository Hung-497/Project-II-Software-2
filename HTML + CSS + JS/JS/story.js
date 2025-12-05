// Get stored name
const playerName = localStorage.getItem("playerName");

// Insert into text box span
document.getElementById("playerNameHere").textContent = playerName;