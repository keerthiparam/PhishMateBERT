const processedEmails = new Set();
let alertShown = false;

function debounce(callback, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => callback(...args), delay);
  };
}

function showAlert() {
  if (alertShown) return;
  alertShown = true;
  alert(
    "WARNING\n\nThis email's content resembles phishing patterns. Be cautious before taking any action."
  );
}

async function checkEmailPhishing(emailText) {
  if (!emailText || !emailText.trim()) {
      console.warn("Skipping phishing check: email text is empty");
      return false;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: emailText }),
    });

    if (!response.ok) {
      throw new Error(`Prediction request failed: ${response.status}`);
    }

    const data = await response.json();
    return data.prediction === "Phishing Email";

  } catch (error) {
    console.error("PhishMate prediction error:", error);
    return false;
  }
}

function getEmailBody() {
  return document.querySelector(".a3s.aiL, .ii.gt, .mail-message-content");
}

async function extractEmailContent() {
  const emailBody = getEmailBody();
  if (!emailBody) return;

  const contentText = emailBody.innerText.trim();
  if (!contentText) {
    console.warn("Email body found but contains no text");
    return;
  }

  if (!contentText) return;

  const contentHash = btoa(unescape(encodeURIComponent(contentText)));
  if (processedEmails.has(contentHash)) return;

  processedEmails.add(contentHash);
  alertShown = false;

  const isPhishing = await checkEmailPhishing(contentText);

  chrome.storage.local.get(["emailCount", "maliciousCount"], (result) => {
    const emailCount = (result.emailCount || 0) + 1;
    const maliciousCount =
      (result.maliciousCount || 0) + (isPhishing ? 1 : 0);

    chrome.storage.local.set({ emailCount, maliciousCount });
  });

  if (isPhishing) showAlert();
}

const observer = new MutationObserver(debounce(extractEmailContent, 1000));
observer.observe(document.body, { childList: true, subtree: true });
extractEmailContent();
