// THEME TOGGLE

const themeToggle = document.getElementById("themeToggle");

function setThemeButton() {
  if (!themeToggle) return;

  if (document.body.classList.contains("dark-mode")) {
    themeToggle.innerHTML = "\u2600\uFE0F"; // ☀️
  } else {
    themeToggle.innerHTML = "\uD83C\uDF39"; // 🎹
  }
}

themeToggle?.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");
  setThemeButton();
});

// Initialize button state on load
setThemeButton();

// SEARCH FUNCTIONALITY

const searchInput = document.getElementById("searchInput");

function applySearch() {
  if (!searchInput) return;

  const filter = searchInput.value.trim().toLowerCase();
  const tasks = document.querySelectorAll(".task-item");

  tasks.forEach((task) => {
    const text = task.innerText.toLowerCase();

    if (!filter || text.includes(filter)) {
      task.style.display = "flex";
    } else {
      task.style.display = "none";
    }
  });
}

searchInput?.addEventListener("keyup", applySearch);
searchInput?.addEventListener("change", applySearch);

// Apply once on load (in case tasks are pre-rendered)
applySearch();

