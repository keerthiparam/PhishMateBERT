// Background service worker for PhishMateBERT.
// The extension stores only local usage statistics.

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.get(
    ["emailCount", "maliciousCount", "darkMode"],
    (result) => {
      const defaults = {};
      if (typeof result.emailCount !== "number") defaults.emailCount = 0;
      if (typeof result.maliciousCount !== "number") defaults.maliciousCount = 0;
      if (!result.darkMode) defaults.darkMode = "disabled";
      if (Object.keys(defaults).length) chrome.storage.local.set(defaults);
    }
  );
});
