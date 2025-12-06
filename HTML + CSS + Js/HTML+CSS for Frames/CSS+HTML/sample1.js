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
});