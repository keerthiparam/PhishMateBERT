# PhishMateBERT

PhishMateBERT is a Chromium browser extension that detects potentially phishing emails using a locally running AI model. Email text is sent only to the local API at `127.0.0.1` for inference.

## Features

- On-device phishing classification with a fine-tuned DeBERTa model
- Real-time email content detection
- Local Flask inference API
- Email and detection counters
- Light and dark popup modes
- No third-party threat-intelligence API or API key required

## Project Structure

```text
PhishMateBERT/
├── background.js
├── content.js
├── mail_checker.py
├── manifest.json
├── popup.html
├── popup.css
├── popup.js
├── requirements.txt
├── icons/
└── model/
    └── phishing_deberta/
```

## Requirements

- Python 3.9+
- A Chromium-based browser
- The trained `phishing_deberta` model files

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Model Setup

Place the model in:

```text
model/phishing_deberta/
```

The model directory is intentionally ignored by Git because model weights are large.

Alternatively, set `PhishMateBERT_MODEL_PATH` to the full path of the model directory.

## Run the Local API

```bash
python mail_checker.py
```

The API starts at `http://127.0.0.1:5000`.

Health check:

```text
GET /health
```

Prediction endpoint:

```text
POST /predict
Content-Type: application/json

{
  "text": "Email content goes here"
}
```

## Install the Extension

1. Open `chrome://extensions/`.
2. Enable **Developer mode**.
3. Click **Load unpacked**.
4. Select the PhishMateBERT project folder.
5. Start the local API with `python mail_checker.py`.
6. Open a supported webmail provider and view an email.

## Privacy

PhishMateBERT is designed for local inference. The extension sends extracted email text to the Flask server running on `127.0.0.1`. No external threat-intelligence API, API key, or cloud inference endpoint is required by the cleaned project.

## Supported Webmail Providers

The manifest currently includes Gmail, Outlook, Yahoo Mail, Proton Mail, Zoho Mail, iCloud Mail, AOL Mail, GMX Mail, and Yandex Mail. Email DOM structures differ between providers, so content extraction should be tested and refined per provider.
