document.querySelectorAll("[data-method-motion]").forEach((root) => {
  const button = root.querySelector("button");
  const status = root.querySelector(".motion-status");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  button?.addEventListener("click", () => {
    const active = root.classList.toggle("is-active");
    button.setAttribute("aria-pressed", String(active));
    button.textContent = active ? "Return to baseline" : "Invoke method";

    if (status) {
      const text = active
        ? "Method applied. Fresh evidence closes the loop."
        : "Tab moves first. Work responds. Evidence settles.";

      if (reduceMotion.matches) {
        status.textContent = text;
        return;
      }

      status.classList.add("is-switching");
      window.setTimeout(() => {
        status.textContent = text;
        status.classList.remove("is-switching");
      }, 140);
    }
  });
});
