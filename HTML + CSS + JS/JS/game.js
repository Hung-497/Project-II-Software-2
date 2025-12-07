const modal = document.getElementById("nameModal");
const startBtn = document.getElementById("startBtn");
const confirmBtn = document.getElementById("confirmNameBtn");
const nameInput = document.getElementById("playerNameInput");
const againBtn = document.getElementById("againBtn");

// Open popup
startBtn.addEventListener("click", () => {
  modal.style.display = "flex";
  nameInput.value = "";
  nameInput.focus();
});

// Confirm name
confirmBtn.addEventListener("click", () => {
  const playerName = nameInput.value.trim();

  if (playerName === "") {
    alert("Please enter a valid name.");
    return;
  }

  alert("Welcome, " + playerName + "!");
  modal.style.display = "none";

  // Optionally redirect:
  // window.location.href = "game.html";
});

// Close popup by clicking outside
window.addEventListener("click", (event) => {
  if (event.target === modal) {
    modal.style.display = "none";
  }
});

againBtn.addEventListener("click", () => {
  window.location.href = "./Home.html";
});
