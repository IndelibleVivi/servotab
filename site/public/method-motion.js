document.querySelectorAll("[data-method-motion]").forEach((root) => {
  const button = root.querySelector("button");
  const status = root.querySelector(".motion-status");

  button?.addEventListener("click", () => {
    const active = root.classList.toggle("is-active");
    button.setAttribute("aria-pressed", String(active));
    button.textContent = active ? "Return to baseline" : "Invoke method";

    if (status) {
      status.textContent = active
        ? "Method applied. Fresh evidence closes the loop."
        : "Tab moves first. Work responds. Evidence settles.";
    }
  });
});
