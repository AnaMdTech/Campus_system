// sidebar.js
document.addEventListener("DOMContentLoaded", () => {
  window.toggleSidebar = function () {
    const sidebar = document.getElementById("sidebar");
    const labels = sidebar.querySelectorAll(".label");
    const main = document.getElementById("main-content");

    sidebar.classList.toggle("w-64");
    sidebar.classList.toggle("w-20");

    labels.forEach((label) => label.classList.toggle("hidden"));
    document
      .getElementById("sidebar-header-expanded")
      .classList.toggle("hidden");
    document
      .getElementById("sidebar-header-collapsed")
      .classList.toggle("hidden");

    main.classList.toggle("ml-64");
    main.classList.toggle("ml-20");
  };
});
