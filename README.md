<div align="center">

  <h1>
    <img src="icons/fish.png" width="90" height="90" alt="PhishMate Logo"/><br/>
    PhishMate
  </h1>

PhishMate is a browser extension that uses AI with link extraction to check if an email is a phishing attempt, in <b>REAL TIME.</b> <br> 100% Open Source and on-device, meaning <u>we do not store your data anywhere.</u>

  <p>
    <a href="#why-phishmate">Why PhishMate?</a> •
    <a href="#tech-stack">Tech Stack</a> •
    <a href="#features">Features</a> •
    <a href="#getting-started">Getting Started</a> •
    <a href="#manifest-overview">Manifest Overview</a> •
    <a href="#privacy-concerns">Privacy Concerns</a>
  </p>
</div>

---

<a id="why-phishmate"></a>
## Why PhishMate 

![youve-won-meme-image](https://d3p8e1mvy30w84.cloudfront.net/assets/images/blog/phishing-memes/youve-won-meme-image.png)

According to current statistics, approximately 3.4 billion phishing emails are sent every day. This translates to roughly 1.2% of all emails being malicious phishing attempts. It is the most common form of cyberattack.

From fake CEO mails to convincing Social Engineering Attacks targeted towards employees in a company, having a tool installed locally on your device helps detect and block such emails, without exposing your data to third-party servers — and without the risk of a Man-in-the-Middle attack associated with inference from a cloud server, possibly compromising confidential information.

<a id="tech-stack"></a>
## Tech Stack 
- <b>Frontend</b>
  - HTML
  - CSS
  - JS
- <b>Backend/ Local API</b>
  - Python
  - Flask

These technologies ensure the extension is lightweight and fast while maintaining robust phishing detection.

<a id="features"></a>
## Features 
1. **Content Analysis**
   - A custom-trained DeBERTa Sequential model analyzes email text for common phishing red flags, such as urgency, poor grammar, and requests for personal info.
2. **Link Analysis**
    - Links sent as a part of the mail are extracted, and checked if they are malicious or legitimate. If it is malicious, the user is alerted.
    - Alerts the user real time when a malicious mail is detected.
    - Click on the extension to see how many emails/links/malicious links have been detected so far.
3. **Dataset**
    - 14k emails were used to train the model
      achieving 90% accuracy in the test set.
    - https://huggingface.co/datasets/zefang-liu/phishing-email-dataset
4. **Supported Browsers**
   - Chromium-based Browsers

## File Structure 
```
PhishMate
├── background.js
├── content.js
├── mail_checker.py
├── manifest.json
├── popup.css
├── popup.html
├── popup.js
├── icons/
├── model/ #place your model folder here after downloading from Google Drive
│   └── phishing_deberta/
```

<a id="getting-started"></a>
## Getting Started 
>(NOTE: Tested on Windows with Chromium-based browsers. Compatibility with Linux/macOS is unverified.)
### Prerequisites
Before installing PhishMate, ensure you have the following dependencies:
- [Python](https://www.python.org/downloads/) (v3.9+)

### Installation

To set up PhishMate locally, follow these steps:

1. **Download Model Files**
   - Download the phishing detection model files from Google Drive [here](https://drive.google.com/drive/folders/1jpxy4_mu5qb0oNtqljxtt0dzcrmOryQy?usp=drive_link).
   - Extract the zip folder `phishing_deberta` to `PhishMate/model/` directory.

2. **Set Up the Local API**
   - Clone the repository:
       ``` sh 
      git clone https://github.com/keerthiparam/PhishMateBERT
      cd PhishMate
       ```

   - Install Python and required dependencies from `requirements.txt`:
     ```sh
     pip install -r requirements.txt
     ```
   - Go to mail_checker.py and replace `MODEL_PATH` in `line 10` of the program with the path to the model folder you downloaded. 
   - Run the local API server:
     ```sh
     python mail_checker.py
     ```
   - Ensure the server is running at `http://127.0.0.1:5000/predict`.
   - Click on the key icon on the top left.
   - Enter your API key and save it.
3. **Install the Chrome Extension**
   - Open Chrome and navigate to `chrome://extensions/`.
   - Enable **Developer mode** (toggle in the top right).
   - Click **Load unpacked** and select the PhishMate extension folder.

4. **Test the Extension**
   - Open your email provider (e.g., Gmail).
   - The extension should analyze email content for phishing threats.

<a id="manifest-overview"></a>
## Manifest Overview 

This `manifest.json` file defines the configuration for the PhishMate Chrome extension.


### 1. Permissions
- `scripting` - Allows the extension to execute scripts in web pages.
- `activeTab` - Grants temporary access to the currently active tab when the extension is used.
- `storage` - Enables the extension to store and retrieve data using Chrome's storage API.

### 2. Host Permissions
The extension requires access to various webmail services and external APIs:
- Email Providers:
  - Gmail, Outlook, Yahoo Mail, Proton Mail, Zoho Mail, iCloud Mail, AOL Mail, GMX Mail, Yandex Mail
- Security & Verification Services:
  - `https://dns.google/*` - For DNS lookups

### 3. Content Scripts
- `content.js` is injected into supported email providers to extract and analyze email content.
- The script runs at `document_end` (after the page has fully loaded).

<a id="privacy-concerns"></a>
## Privacy Concerns 
PhishMate is designed with user privacy in mind. However, the following considerations should be noted:
1. **Data Collection**
   - The contents of the email extracted are processed by the model locally on your device upon downloading it. Hence, there is no worry about your email content being intercepted by third parties.
2. **Self-hosted Model**
    - The model, after being set up successfully, is run on a **Completely Local API**.
3. **Chrome-based Browsers**
    - The tool, since it is designed to be a chrome extension, works only on chrome based browsers. 

By keeping the phishing detection model self-hosted and minimizing external requests, PhishMate prioritizes both security and user privacy.

## Growing Factors 
1. Expand compatibility to browsers like Firefox as the user base grows.
2. Employing a more robust model for content detection.

## Future Plans 
1.   As the user base expands, it is necessary to make sure the model can detect any type of phishing email. This means training the model with a bigger dataset to ensure accuracy across all types of content.
2. Accommodating users from any browser; not just chromium based.
3. Expanded sources to check for malicious links.
4. As the model grows in size, self-hosting may eventually become impractical. Then, it would have to be hosted on the cloud for inference, with appropriate SSL integration to ensure content safety.

