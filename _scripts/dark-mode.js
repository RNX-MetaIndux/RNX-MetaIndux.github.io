/*
  manages light/dark mode.
*/

{
  const storageKey = "dark-mode";

  const applyDarkMode = (dark, save = false) => {
    const value = String(dark);
    document.documentElement.dataset.dark = value;
    document.documentElement.style.colorScheme = dark ? "dark" : "light";

    document.querySelectorAll(".dark-toggle").forEach((toggle) => {
      toggle.checked = dark;
    });

    if (save) window.localStorage.setItem(storageKey, value);
  };

  // Apply the saved mode before the page renders.
  const savedMode = window.localStorage.getItem(storageKey) === "true";
  applyDarkMode(savedMode);

  window.addEventListener("DOMContentLoaded", () => {
    applyDarkMode(document.documentElement.dataset.dark === "true");

    document.querySelectorAll(".dark-toggle").forEach((toggle) => {
      toggle.addEventListener("change", (event) => {
        applyDarkMode(event.currentTarget.checked, true);
      });
    });
  });
}
