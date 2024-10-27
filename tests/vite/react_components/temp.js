htmx.on("htmx:beforeHistorySave", () => {
  document.querySelectorAll("[data-lucide]").forEach((elt) => {
    elt.remove();
  });
});
