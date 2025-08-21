export function initTabs() {
  const tabButtons = document.querySelectorAll(".tab-button");
  const tabContents = document.querySelectorAll(".tab-content");

  tabButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const tabId = btn.dataset.tab;

      // Remove active class from all tabs and contents
      tabButtons.forEach((b) => b.classList.remove("active"));
      tabContents.forEach((c) => c.classList.remove("active"));

      // Add active class to clicked tab and corresponding content
      btn.classList.add("active");
      const content = document.getElementById(tabId);
      if (content) {
        content.classList.add("active");
      }

      console.log("[TABS] Switched to tab:", tabId);
    });
  });

  // Set default active tab if none is active
  const activeTab = document.querySelector(".tab-button.active");
  if (!activeTab && tabButtons.length > 0) {
    tabButtons[0].click();
  }
}
