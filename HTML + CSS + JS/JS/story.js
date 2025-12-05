// We are using this to get our variable 'Player Name'
// This variable we have created in the home page
// At the moment only linked with story page and game_play page
const playerName = localStorage.getItem("playerName");

// Insert into text box span, our text story place
document.getElementById("playerNameHere").textContent = playerName;