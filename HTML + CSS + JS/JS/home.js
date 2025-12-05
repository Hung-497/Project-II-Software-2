// Get elements
const startBtn = document.getElementById("startBtn");
const modal = document.getElementById("nameModal");
const confirmBtn = document.getElementById("confirmNameBtn");
const nameInput = document.getElementById("playerNameInput");

// Open popup
startBtn.addEventListener("click", () => {
    modal.style.display = "flex";
    nameInput.focus();
});

// Confirm name
confirmBtn.addEventListener("click", () => {
    const name = nameInput.value.trim();

    if (name === "") {
        alert("Please enter a name!");
        return;
    }

    // Save the name for next page
    localStorage.setItem("playerName", name);

    // Close modal
    modal.style.display = "none";

    // Redirect to story page and Game_Play page
    window.location.href = "story.html";
});

// Close popup when clicking outside
window.addEventListener("click", (e) => {
    if (e.target === modal) {
        modal.style.display = "none";
    }
});





document.getElementById("exitBtn").addEventListener("click", () => {
    window.location.href = "about:blank";
});




