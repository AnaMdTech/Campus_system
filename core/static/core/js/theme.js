// theme.js
document.addEventListener("DOMContentLoaded", () => {
  // Use document.documentElement to get the html element
  const html = document.documentElement;
  const toggle = document.getElementById("theme-toggle");
  const switchBox = document.getElementById("theme-switch");
  const ball = document.getElementById("theme-ball");

  if (!html || !toggle || !switchBox || !ball) {
    console.error("Theme toggle elements not found!");
    return; // Exit if elements are not available
  }

  // This function updates the visual state of the toggle switch (checkbox and ball position)
  // The background color of the switch is handled by CSS based on toggle.checked
  function updateToggleUI(isDark) {
    toggle.checked = isDark;
    // Ball position is now controlled by CSS based on the checkbox state
    // The CSS rule 'aside#sidebar #theme-toggle:checked + #theme-switch #theme-ball' handles the transform
  }

  // Initialize the toggle button state based on the *current* theme class
  // The early inline script already applied the theme class if needed.
  const currentThemeIsDark = html.classList.contains("dark");
  updateToggleUI(currentThemeIsDark);

  // Event listener for the toggle button (checkbox)
  toggle.addEventListener("change", () => {
    const isDark = toggle.checked;
    // Update localStorage
    localStorage.setItem("theme", isDark ? "dark" : "light");

    // Manually toggle the class on the current page for instant effect
    // (The early script handles the initial load on subsequent pages)
    if (isDark) {
      html.classList.add("dark");
      ball.style.transform = "translateX(20px)";
    } else {
      html.classList.remove("dark");
      ball.style.transform = "translateX(0px)";
    }

    // updateToggleUI(isDark); // Redundant call here, checkbox state is already set by the 'change' event
  });

  // Listen for OS theme changes while the page is open
  window
    .matchMedia("(prefers-color-scheme: dark)")
    .addEventListener("change", (e) => {
      const osPrefersDark = e.matches;
      const savedTheme = localStorage.getItem("theme");

      // Only update theme if the user hasn't explicitly saved a preference.
      // If savedTheme is null or undefined, we follow the OS preference.
      if (savedTheme === null) {
        const themeToApply = osPrefersDark ? "dark" : "light";
        localStorage.setItem("theme", themeToApply); // Save OS preference

        // Manually update class and UI instantly
        if (osPrefersDark) {
          html.classList.add("dark");
        } else {
          html.classList.remove("dark");
        }
        updateToggleUI(osPrefersDark); // Update the toggle UI to match OS preference
      }
      // If savedTheme is 'dark' or 'light', the user has a manual preference,
      // and we do NOT override it when the OS preference changes.
    });
});
