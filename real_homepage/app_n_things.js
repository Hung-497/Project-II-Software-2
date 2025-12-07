function submitScore(playerName, triesUsed) {
  fetch("http://127.0.0.1:5000/submit-score", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ player_name: playerName, score: triesUsed }),
  })
    .then((res) => res.json())
    .then((data) => console.log(data))
    .catch((err) => console.error(err));
}

const logo = document.getElementById("playLogo");
const hint = document.getElementById("hoverHint");

// hint follows cursor when hovering over logo
logo.addEventListener("mousemove", (e) => {
  hint.style.opacity = "1";
  hint.style.left = e.pageX + "px";
  hint.style.top = e.pageY + "px";
});

// hide when leaving
logo.addEventListener("mouseleave", () => {
  hint.style.opacity = "0";
});

// CSS animates the fade, JS waits then redirects
document.getElementById("playLogo").addEventListener("click", () => {
  document.body.classList.add("fade-out");
  setTimeout(() => {
    window.location.href = "home.html";
  }, 700);
});

// same effect as with another game-page redirection
document.getElementById("navgame").addEventListener("click", (event) => {
  // prevents default behaviour in order to execute the fade-out
  event.preventDefault();
  document.body.classList.add("fade-out");
  setTimeout(() => {
    window.location.href = "home.html";
  }, 700);
});
