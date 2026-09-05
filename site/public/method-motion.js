document.querySelectorAll("[data-method-motion]").forEach((root) => {
  const button = root.querySelector("button");
  const status = root.querySelector(".motion-status");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let pendingUpdate = null;
  let updateGeneration = 0;

  const statusText = () => root.classList.contains("is-active")
    ? "Method applied. Fresh evidence closes the loop."
    : "Tab moves first. Work responds. Evidence settles.";

  const cancelPendingUpdate = () => {
    updateGeneration += 1;
    if (pendingUpdate !== null) {
      window.clearTimeout(pendingUpdate);
      pendingUpdate = null;
    }
    status?.classList.remove("is-switching");
  };

  reduceMotion.addEventListener("change", () => {
    if (!reduceMotion.matches || !status) return;

    const shouldSettle = pendingUpdate !== null
      || status.classList.contains("is-switching")
      || status.textContent !== statusText();
    cancelPendingUpdate();
    if (shouldSettle) status.textContent = statusText();
  });

  button?.addEventListener("click", () => {
    const active = root.classList.toggle("is-active");
    button.setAttribute("aria-pressed", String(active));
    button.textContent = active ? "Return to baseline" : "Invoke method";

    cancelPendingUpdate();
    if (!status) return;
    const text = statusText();
    if (reduceMotion.matches) {
      status.textContent = text;
      return;
    }

    const generation = updateGeneration;
    status.classList.add("is-switching");
    pendingUpdate = window.setTimeout(() => {
      if (generation !== updateGeneration) return;
      pendingUpdate = null;
      status.textContent = text;
      status.classList.remove("is-switching");
    }, 140);
  });
});
