// settings.js
document.addEventListener("DOMContentLoaded", () => {
  window.toggleSettingsDropdown = function () {
    const dropdown = document.getElementById("settings-dropdown");
    const arrow = document.getElementById("settings-arrow");
    dropdown.classList.toggle("hidden");
    arrow.classList.toggle("rotate-180");
  };
});
