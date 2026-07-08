{
  const initializePagination = (root) => {
    const name = root.dataset.pagination;
    const controls = document.querySelector(
      `[data-pagination-controls="${name}"]`
    );
    const items = [...root.querySelectorAll("[data-pagination-item]")];
    const pageSize = Number(root.dataset.pageSize) || 10;

    if (!controls || !items.length) return;

    let currentPage = 1;

    const updateUrl = (page) => {
      const url = new URL(window.location);
      if (page > 1) url.searchParams.set("page", page);
      else url.searchParams.delete("page");
      window.history.replaceState(null, "", url);
    };

    const renderControls = (pageCount) => {
      controls.replaceChildren();
      controls.hidden = pageCount <= 1;
      if (pageCount <= 1) return;

      const makeButton = (label, page, icon, active = false) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "pagination-button";
        button.dataset.page = page;
        button.setAttribute("aria-label", label);
        button.title = label;
        if (active) button.setAttribute("aria-current", "page");
        button.innerHTML = icon
          ? `<i class="icon fa-solid ${icon}" aria-hidden="true"></i>`
          : page;
        return button;
      };

      const previous = makeButton(
        "Previous page",
        Math.max(1, currentPage - 1),
        "fa-chevron-left"
      );
      previous.disabled = currentPage === 1;
      controls.append(previous);

      for (let page = 1; page <= pageCount; page++) {
        controls.append(
          makeButton(`Page ${page}`, page, "", page === currentPage)
        );
      }

      const next = makeButton(
        "Next page",
        Math.min(pageCount, currentPage + 1),
        "fa-chevron-right"
      );
      next.disabled = currentPage === pageCount;
      controls.append(next);
    };

    const renderPage = (requestedPage = 1, syncUrl = true) => {
      const matchingItems = items.filter(
        (item) => item.dataset.searchMatch !== "false"
      );
      const pageCount = Math.max(1, Math.ceil(matchingItems.length / pageSize));
      currentPage = Math.min(Math.max(1, Number(requestedPage) || 1), pageCount);
      const start = (currentPage - 1) * pageSize;
      const visibleItems = new Set(
        matchingItems.slice(start, start + pageSize)
      );

      items.forEach((item) => {
        item.hidden = !visibleItems.has(item);
      });

      root.querySelectorAll("[data-pagination-group]").forEach((group) => {
        group.hidden = ![...group.querySelectorAll("[data-pagination-item]")]
          .some((item) => !item.hidden);
      });

      renderControls(pageCount);
      if (syncUrl) updateUrl(currentPage);
    };

    controls.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-page]");
      if (!button || button.disabled) return;
      renderPage(button.dataset.page);
      root.scrollIntoView({ behavior: "smooth", block: "start" });
    });

    window.addEventListener("searchupdated", (event) => {
      const preservePage = event.detail?.preservePage;
      const requestedPage = preservePage
        ? new URLSearchParams(window.location.search).get("page") || 1
        : 1;
      renderPage(requestedPage, !preservePage);
    });

    const initialPage = new URLSearchParams(window.location.search).get("page");
    renderPage(initialPage || 1, false);
  };

  window.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-pagination]").forEach(initializePagination);
  });
}
