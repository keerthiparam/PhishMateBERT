from pathlib import Path
import os

from flask import Flask, jsonify, request
from flask_cors import CORS
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = Path(os.getenv("PhishMateBERT_MODEL_PATH", BASE_DIR / "model" / "phishing_deberta"))
MAX_LENGTH = 512
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

app = Flask(__name__)
CORS(app)

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model not found at: {MODEL_PATH}\n"
        "Place the model in model/phishing_deberta or set PhishMateBERT_MODEL_PATH."
    )

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.to(DEVICE)
model.eval()


def predict_email(text: str):
    inputs = tokenizer(
        text,
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    ).to(DEVICE)

    with torch.no_grad():
        logits = model(**inputs).logits
        probabilities = torch.softmax(logits.float(), dim=-1).squeeze()

    prediction_id = int(torch.argmax(probabilities).item())
    label = model.config.id2label[prediction_id]
    confidence = float(probabilities[prediction_id].item())
    return label, confidence


@app.post("/predict")
def predict():
    data = request.get_json(silent=True)
    text = data.get("text") if isinstance(data, dict) else None

    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "Missing or empty 'text' field"}), 400

    label, confidence = predict_email(text)
    return jsonify({"prediction": label, "confidence": round(confidence, 4)})


@app.get("/health")
def health():
    return jsonify({"status": "ok", "device": DEVICE})

BANNER = r"""
░█████████  ░██        ░██           ░██        ░███     ░███               ░██               
░██     ░██ ░██                      ░██        ░████   ░████               ░██               
░██     ░██ ░████████  ░██ ░███████  ░████████  ░██░██ ░██░██  ░██████   ░████████  ░███████  
░█████████  ░██    ░██ ░██░██        ░██    ░██ ░██ ░████ ░██       ░██     ░██    ░██    ░██ 
░██         ░██    ░██ ░██ ░███████  ░██    ░██ ░██  ░██  ░██  ░███████     ░██    ░█████████ 
░██         ░██    ░██ ░██       ░██ ░██    ░██ ░██       ░██ ░██   ░██     ░██    ░██        
░██         ░██    ░██ ░██ ░███████  ░██    ░██ ░██       ░██  ░█████░██     ░████  ░███████  
"""

if __name__ == "__main__":
    print(BANNER)
    print(f"PhishMateBERT API running on {DEVICE}")
    app.run(host="127.0.0.1", port=5000, debug=False)
