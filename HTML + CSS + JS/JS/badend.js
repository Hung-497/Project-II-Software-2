window.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => {
        const planeCrashing = document.getElementById("plane-crashing");
        if (planeCrashing) {
            planeCrashing.classList.remove("hidden");

            setTimeout(() => {
                planeCrashing.classList.add("hidden");
            }, 4000);
        }
    }, 1000);

    setTimeout(() => {
        const storyText = document.getElementById("story-text");
        if (storyText) {
            storyText.classList.remove("hidden");
        }
    }, 5000);
    setTimeout(() => {
        const storyButtons = document.getElementById("story-buttons");
        if (storyButtons) {
            storyButtons.classList.remove("hidden");
        }
    }, 5000);
    setTimeout(() => {
        const storyButtons = document.getElementById("btn-continue");
        if (storyButtons) {
            storyButtons.classList.remove("hidden");
        }
    }, 5000);
    setTimeout(() => {
        const storyButtons = document.getElementById("btn-exit");
        if (storyButtons) {
            storyButtons.classList.remove("hidden");
        }
    }, 5000);

    const newGameButton = document.getElementById("btn-continue");
    if (!newGameButton) return;
    newGameButton.addEventListener("click", async () => {
        await fetch("http://127.0.0.1:5000/newgame")
        window.location.href = "gameplay.html";
    }
    )
    const homeButton = document.getElementById("btn-exit")
    if (!homeButton) return;
    homeButton.addEventListener("click", () => {
        window.location.href = "home.html"
    })
});