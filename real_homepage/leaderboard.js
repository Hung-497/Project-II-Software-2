fetch("http://127.0.0.1:5000/leaderboard")
  .then((res) => res.json())
  .then((data) => {
    const tbody = document.querySelector("#leaderboard tbody");

    data.forEach((row, index) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>#${index + 1}</td>
        <td>${row.player_name}</td>
        <td>${row.score}</td>
        <td>${new Date(row.created_at).toLocaleDateString()}</td>
      `;
      tbody.appendChild(tr);
    });
  })
  .catch((err) => console.error("Failed to load leaderboard:", err));
