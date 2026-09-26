document.addEventListener("DOMContentLoaded", () => {
  const emailCountElem = document.getElementById("emailCount");
  const maliciousCountElem = document.getElementById("maliciousCount");
  const darkModeToggle = document.getElementById("darkModeToggle");
  const clearBtn = document.getElementById("clearBtn");
  const successMessage = document.getElementById("popupSuccessMessage");
  const refreshBtn = document.getElementById("refreshBtn");

  function updateDarkMode(isDark) {
    document.body.classList.toggle("dark-mode", isDark);
  }

  function loadStats() {
    chrome.storage.local.get(["emailCount", "maliciousCount", "darkMode"], (result) => {
      emailCountElem.textContent = result.emailCount || 0;
      maliciousCountElem.textContent = result.maliciousCount || 0;
      updateDarkMode(result.darkMode === "enabled");
    });
  }

  darkModeToggle.addEventListener("click", () => {
    chrome.storage.local.get("darkMode", (result) => {
      const darkMode = result.darkMode !== "enabled" ? "enabled" : "disabled";
      chrome.storage.local.set({ darkMode });
      updateDarkMode(darkMode === "enabled");
    });
  });

  clearBtn.addEventListener("click", () => {
    chrome.storage.local.set({ emailCount: 0, maliciousCount: 0 }, () => {
      emailCountElem.textContent = "0";
      maliciousCountElem.textContent = "0";
      successMessage.style.display = "block";
      setTimeout(() => (successMessage.style.display = "none"), 2000);
    });
  });

  refreshBtn.addEventListener("click", () => {
    refreshBtn.disabled = true;

    const refreshIcon = document.getElementById("refreshIcon");

    chrome.storage.local.get(
        ["emailCount", "maliciousCount"],
        (result) => {
            emailCountElem.textContent = result.emailCount || 0;
            maliciousCountElem.textContent = result.maliciousCount || 0;

            // Visual feedback
            refreshIcon.style.transform = "rotate(360deg)";
            refreshIcon.style.transition = "transform 0.4s ease";

            setTimeout(() => {
                refreshIcon.style.transform = "rotate(0deg)";
                refreshBtn.disabled = false;
            }, 400);
          }
      );
  });

  loadStats();
});
